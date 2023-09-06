#!/usr/bin/env python3
# mypy: ignore-errors
import os
import smtplib as smtp
import ssl
import subprocess
import threading
import time
import typing
from argparse import ArgumentParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger

import requests
import schedule
from dotenv import load_dotenv

BUILD_RUNNING = threading.Event()
CURRENTLY_BUILDING = threading.Event()
BUILD_FAILED = threading.Event()
lock = threading.Lock()
BUILD_TRY = 0
logger = getLogger("manage-app-logger")

args_parser = ArgumentParser(description="CLI args for the script")

args_parser.add_argument(
    '--load_env', action='store_true',
    help='Load environment variables from a dotenv file',
)
args_parser.add_argument(
    "--no_cd", action='store_true',
    help="Disable checking for new changes in the git repo",
)
args_parser.add_argument(
    "--no_renewal", action='store_true',
    help="Disable the renewal of certificates",
)
args_parser.add_argument(
    "--no_health_checks", action="store_true", help="Disables all health checks",
)
args = args_parser.parse_args()

if args.load_env:
    load_dotenv()

# DEV, PROD, STAGING - this is the identifier of the environment in the emails
ENV = os.environ["DOCK_ENV"]
# e.g. dev.thehub-aubg.com/api/validate or localhost:3000/api/validate
API_URL = os.environ["HUB_API_URL"]
# e.g. dev.thehub-aubg.com or localhost:3000
WEB_URL = os.environ["HUB_WEB_URL"]
PY_API = os.environ["HUB_PY_API_URL"]
# dev.thehub-aubg.com (without http) --> used for cert renewal
CERT_DOMAIN = os.environ["HUB_DOMAIN"]
DISCORD_WH = os.environ["DISCORD_WH"]  # url of webhook (discord channel)

REPO_URL = "https://github.com/AUBGTheHUB/monolith"  # remove last backlash


class bcolors:
    YELLOW_IN = '\033[33m'
    YELLOW_OUT = '\033[43m'
    RED_IN = '\033[31m'
    CYAN_IN = '\033[93m'
    RED_OUT = '\033[41m'
    OKGREEN = '\033[92m'
    CEND = '\033[0m'


def send_mail(msg):
    port = 465  # SSL
    email = os.environ['HUB_MAIL_USERNAME']
    password = os.environ['HUB_MAIL_PASSWORD']

    server = smtp.SMTP_SSL('smtp.gmail.com', port)
    server.login(email, password)
    server.sendmail(email, os.environ['HUB_MAIL_RECEIVER'], msg.as_string())
    server.close()

    print(bcolors.OKGREEN + "An email has been sent!" + bcolors.CEND)


def handle_exception(msg: MIMEMultipart, method: str, url: str, service: str, e: Exception, discord: bool):
    if not discord:
        msg.attach(
            MIMEText(
                '<h3>{}: {} Request to {} failed with the following exception: </h3> </p> {}'.format(
                    os.getenv("DOCK_ENV"), method, url,
                    str(e),
                ) + '</p>',
                'html',
            ),
        )
        send_mail(msg)
    else:
        requests.post(
            os.getenv("DISCORD_WH"), headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
                "content": f"🏗️: **{os.getenv('DOCK_ENV')}**\n❌: @here {method} Request to {url} failed with the following exception:\n```text\n{str(e)}\n```",
            },
        )
    print(
        bcolors.RED_IN + "{}:{} IS DOWN - {}".format(
            os.getenv("DOCK_ENV"),
            service, str(url),
        ) + bcolors.CEND,
    )
    return e


def handle_status_code_exception(
        msg: MIMEMultipart, method: str, url: str, service: str, status_code: int,
        discord: bool,
):
    if not discord:
        # send email that the website is down
        msg.attach(
            MIMEText(
                '<h3>{}: {} Request to {} failed with status code {}'.format(
                    os.getenv("DOCK_ENV"), method, url, str(status_code),
                ) + '</h3>', 'html',
            ),
        )
        send_mail(msg)
    else:
        # send discord notification that the website is down
        requests.post(
            os.getenv("DISCORD_WH"), headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
                "content": f"🏗️: **{os.getenv('DOCK_ENV')}**\n❌: @here {method} Request to {url} failed with status code: **{str(status_code)}**",
            },
        )

    print(
        bcolors.RED_IN + "{}:{} IS DOWN - {}".format(
            os.getenv("DOCK_ENV"),
            service, str(url),
        ) + bcolors.CEND,
    )

    return status_code


def start_docker_compose():
    # --abort-on-container-exit is not compatible with detached mode
    # therefore check up should be done with requests

    global BUILD_TRY
    msg = MIMEMultipart('alternative')

    # Do not allow new builds to start
    # if a building process is currently running
    if CURRENTLY_BUILDING.is_set():
        return

    CURRENTLY_BUILDING.set()
    with lock:
        if BUILD_TRY == 0:
            BUILD_FAILED.clear()

        BUILD_TRY = BUILD_TRY + 1

    errors = {}

    def get_current_commit():
        current_commit = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"], check=True, capture_output=True,
        )

        current_commit = subprocess.run(
            ["sed", "1q"], input=current_commit.stdout, capture_output=True,
        )

        return current_commit.stdout.decode('utf-8').strip()

    def get_commit_url():

        hash = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True, text=True,
        )
        return f"{REPO_URL}/commit/{hash.stdout}"

    dc_start = subprocess.run(
        [
            "sudo", "COMPOSE_DOCKER_CLI_BUILD=1", "DOCKER_BUILDKIT=1",
            "docker-compose", "up", "--build", "-d",
        ],
    )

    if dc_start.returncode == 0:
        print()

        time.sleep(10)
        print(bcolors.CYAN_IN + "BUILD HEALTH CHECK:" + bcolors.CEND)

        ###### WEB ######
        get_web = check_service_up(os.getenv("HUB_WEB_URL"), "WEB", False)

        # "connection reset by peer"
        print()
        time.sleep(10)

        ###### API ######
        get_api = check_service_up(os.getenv("HUB_API_URL"), "API", False)

        ##### PY-API #####
        get_py_api = check_service_up(
            os.getenv("HUB_PY_API_URL"), "PY-API", False,
        )

        # URL-SHORTENER
        get_url_shortener = check_service_up(
            os.getenv("HUB_URL_SHORTENER"), "URL-SHORTENER", False,
        )

        print()
        if (get_web == 200 and get_api == 400 and get_py_api == 200 and get_url_shortener == 200):
            print(
                bcolors.OKGREEN +
                f"{os.getenv('DOCK_ENV')} BUILD SUCCESSFUL" + bcolors.CEND,
            )
            BUILD_RUNNING.set()

            msg['Subject'] = f'{os.getenv("DOCK_ENV")}:SPA BUILD SUCCESSFUL'
            msg.attach(
                MIMEText('<h3>All services are working!</h3>', 'html'),
            )
            send_mail(msg)

            requests.post(
                os.getenv("DISCORD_WH"), headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                }, data={
                    "content": f"🏗️: **{os.getenv('DOCK_ENV')}**\n🔔: [{get_current_commit()}]({get_commit_url()})\n✅: Successfully Deployed ",
                },
            )

            # THIS SIGNIFIES THAT A NEW BUILD CAN BE STARTED IF THERE IS AN ERROR
            CURRENTLY_BUILDING.clear()

            # THIS INDICATES THAT THE BUILD HAS BEEN SUCCESSFUL
            BUILD_RUNNING.set()

            with lock:
                BUILD_TRY = 0
            return

        else:
            # docker-compose keeps running when there is a failed container
            errors['WEB'] = get_web
            errors['API'] = get_api
            errors['PY-API'] = get_py_api
            errors['URL-SHORTENER'] = get_url_shortener

    build_err = subprocess.run(
        [
            "sudo", "COMPOSE_DOCKER_CLI_BUILD=1", "DOCKER_BUILDKIT=1",
            "docker-compose", "up", "--build", "-d",
        ],
        capture_output=True,
    )

    errors["BUILD"] = build_err.stderr.decode('utf-8')

    print(bcolors.RED_IN + "BUILD FAILED" + bcolors.CEND)

    msg['Subject'] = f'{os.getenv("DOCK_ENV")}:SPA BUILD FAILED'
    msg.attach(MIMEText('<p>' + str(errors) + '</p>', 'html'))
    send_mail(msg)

    errors["BUILD"] = errors["BUILD"].splitlines()[-10:]

    if BUILD_TRY <= 1:
        requests.post(
            os.getenv("DISCORD_WH"), headers={
                "Content-Type": "application/x-www-form-urlencoded",
            }, data={
                "content": f"🏗️: **{os.getenv('DOCK_ENV')}**\n🔔: [{get_current_commit()}]({get_commit_url()})\n❌: @here Build Failed\n```python\n{beautify_errors(errors)}```",
            },
        )

    CURRENTLY_BUILDING.clear()

    with lock:
        if BUILD_TRY >= 2:
            os._exit(1)

    return


def beautify_errors(errors: dict) -> str:
    try:
        output_string = ""

        if (build_errors := errors.get("BUILD", None)):
            output_string += "BUILD:\n\t"
            output_string += '\n\t'.join(build_errors)

        if (build_errors := errors.get("WEB", None)):
            output_string += "WEB:\n\t"
            output_string += '\n\t'.join(build_errors)

        if (build_errors := errors.get("API", None)):
            output_string += "API:\n\t"
            output_string += '\n\t'.join(build_errors)

    except Exception as e:
        return str(e)

    return output_string


def stop_docker_compose():
    dc_stop = subprocess.run(["sudo", "docker-compose", "down"])
    BUILD_RUNNING.clear()


def check_service_up(url: str, service: str, discord=False):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{}:{} - SERVICE IS DOWN!'.format(
        os.getenv("DOCK_ENV"), service,
    )

    web_request = None

    """
    This could be heavily restructured if there are more services to be checked
    As of now, the replicated code is not an issue - it's easy to read
    """

    print()
    print(
        bcolors.YELLOW_IN +
        "CHECKING SERVICE {}:{} ".format(
            os.getenv("DOCK_ENV"), service,
        ) + bcolors.CEND,
    )

    req_method = ""

    if service == "WEB":
        try:
            web_request = requests.get(url)
            req_method = "GET"

        except Exception as e:
            if not args.no_health_checks:
                return handle_exception(msg, req_method, url, service, e, discord)
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, \nExc: {e}",
                )

        if web_request.status_code != 200:
            if not args.no_health_checks:
                return handle_status_code_exception(
                    msg, req_method, url, service, web_request.status_code, discord,
                )
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, "
                    f"\nStatus code: {web_request.status_code}",
                )

    elif service == "API":
        try:
            web_request = requests.post(url=url)
            req_method = "POST"

        except Exception as e:
            if not args.no_health_checks:
                return handle_exception(msg, req_method, url, service, e, discord)
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, \nExc: {e}",
                )

        if web_request.status_code != 400:
            if not args.no_health_checks:
                return handle_status_code_exception(
                    msg, req_method, url, service, web_request.status_code, discord,
                )
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, "
                    f"\nStatus code: {web_request.status_code}",
                )

    elif service == "PY-API":
        try:
            web_request = requests.get(url=url)

        except Exception as e:
            if not args.no_health_checks:
                return handle_exception(msg, req_method, url, service, e, discord)
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, \nExc: {e}",
                )

        if web_request.status_code != 200:
            if not args.no_health_checks:
                return handle_status_code_exception(
                    msg, req_method, url, service, web_request.status_code, discord,
                )
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, "
                    f"\nStatus code: {web_request.status_code}",
                )

    elif service == "URL-SHORTENER":
        try:
            web_request = requests.get(url=url)
        except Exception as e:
            if not args.no_health_checks:
                return handle_exception(msg, req_method, url, service, e, discord)
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, \nExc: {e}",
                )
        if web_request.status_code != 200:
            if not args.no_health_checks:
                return handle_status_code_exception(
                    msg, req_method, url, service, web_request.status_code, discord,
                )
            else:
                logger.error(
                    f"Message: {msg}, \nRequest method: {req_method}, \nURL: {url}, \nService: {service}, "
                    f"\nStatus code: {web_request.status_code}",
                )
    print(bcolors.OKGREEN + "Nothing unusual!" + bcolors.CEND)

    return web_request.status_code


""" definitions of cron jobs """


def cron_local_test():
    # exit if services are currently building
    if CURRENTLY_BUILDING.is_set() or BUILD_FAILED.is_set():
        return

    local_web = check_service_up(os.getenv("HUB_WEB_URL"), "WEB", True)
    local_api = check_service_up(os.getenv("HUB_API_URL"), "API", True)
    local_py_api = check_service_up(os.getenv("HUB_PY_API_URL"), "API", True)
    local_url_shortener = check_service_up(
        os.getenv("HUB_URL_SHORTENER"), "API", True,
    )
    # build is not running
    if local_web != 200 or local_api != 400 or local_py_api != 200 or local_url_shortener != 200:
        BUILD_RUNNING.clear()


def cron_git_check_for_updates():
    # only >= 3.7
    remote_update = subprocess.run(
        ['git', 'remote', 'update'], capture_output=True, text=True,
    )
    if remote_update.returncode != 0:
        print("GIT REMOTE UPDATE FAILED: \n{}".format(remote_update.stdout))
        return

    print(remote_update.stdout)

    # only >= 3.7
    status_uno = subprocess.run(
        ['git', 'status'], capture_output=True, text=True,
    )
    if status_uno.returncode != 0:
        print("GIT STATE FAILED: \n{}".format(status_uno.stdout))
        return

    if "Your branch is behind" in status_uno.stdoutq or "Your branch is ahead" in status_uno.stdout or "diverged" in status_uno.stdout:
        print("BRANCH IS BEHIND!")
        subprocess.run(
            ['git', 'fetch'], capture_output=True, text=True,
        )
        branch_name = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True,
        )
        subprocess.run(
            ['git', 'reset', '--hard', f'origin/{branch_name.stdout}'],
        )
        subprocess.run(
            ['git', 'pull'], capture_output=True, text=True,
        )

        print("STARTING BUILD")
        start_docker_compose()


def cron_self_healing():
    print("BUILD IS RUNNING: {}".format(str(BUILD_RUNNING.is_set())))
    if not BUILD_RUNNING.is_set() and not CURRENTLY_BUILDING.is_set():
        print(bcolors.RED_IN + "WILL TRY TO RECOVER BUILD!" + bcolors.CEND)
        start_docker_compose()


def cron_start_with_new_certs():
    print(
        bcolors.YELLOW_IN +
        "RESTARTING SERVICES SO THAT THE NEW CERTS COULD BE APPLIED" + bcolors.CEND,
    )
    # BUILD_RUNNING.clear()

    # MAKE SURE NEW CERTS ARE INSTALLED
    # Could be done with symbolic links
    pwd = subprocess.check_output(['pwd'])
    pwd = pwd.decode('utf-8').replace('\n', '')
    pwd += '/data/certs/'

    print(bcolors.RED_IN + pwd + bcolors.CEND)

    subprocess.run(['mv', '-f', pwd + 'devenv.crt', pwd + 'devenv_old.crt'])
    subprocess.run(['mv', '-f', pwd + 'devenv.key', pwd + 'devenv_old.key'])

    # we need to unbind the port
    stop_docker_compose()
    CURRENTLY_BUILDING.set()
    subprocess.run(['certbot', 'renew', '--force-renewal'])

    subprocess.run([
        'cp', '/etc/letsencrypt/live/' +
              os.getenv("HUB_DOMAIN") + "/fullchain.pem", pwd + 'devenv.crt',
    ])
    subprocess.run([
        'cp', '/etc/letsencrypt/live/' +
              os.getenv("HUB_DOMAIN") + "/privkey.pem", pwd + 'devenv.key',
    ])

    CURRENTLY_BUILDING.clear()
    start_docker_compose()


""" threading for cron jobs """


def run_thread(job):
    print("\nSTARTING CRON JOB - {}".format(job.__name__))
    thread = threading.Thread(target=job)
    thread.start()


if args.no_renewal:
    start_docker_compose()
else:
    cron_start_with_new_certs()

schedule.every(1).minutes.do(run_thread, cron_local_test)

schedule.every(200).seconds.do(run_thread, cron_self_healing)
if not args.no_cd:
    schedule.every(60).seconds.do(run_thread, cron_git_check_for_updates)
if not args.no_renewal:
    schedule.every(75).days.do(run_thread, cron_start_with_new_certs)

while True:
    schedule.run_pending()
    time.sleep(1)
