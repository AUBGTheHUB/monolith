#!/usr/bin/env python3
import subprocess
import requests
import time
import os
import smtplib as smtp, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import typing

BUILD_RUNNING = False

class bcolors:
    YELLOW_IN = '\033[33m'
    YELLOW_OUT = '\033[43m' 
    RED_IN = '\033[31m'
    CYAN_IN = '\033[93m'
    RED_OUT = '\033[41m'
    OKGREEN = '\033[92m'
    CEND = '\033[0m'

def send_mail(msg):
    port = 465 # SSL
    email = os.environ['HUB_MAIL_USERNAME']
    password = os.environ['HUB_MAIL_PASSWORD']

    server = smtp.SMTP_SSL('smtp.gmail.com', port)
    server.login(email, password)
    server.sendmail(email, "thehubaubg@gmail.com", msg.as_string())
    server.close()

    print(bcolors.OKGREEN + "An email has been sent!" + bcolors.CEND)

def start_docker_compose():
    # --abort-on-container-exit is not compatible with detached mode
    # therefore check up should be done with requests
    global BUILD_RUNNING

    msg = MIMEMultipart('alternative')
    
    errors = []

    if BUILD_RUNNING:
        stop_docker_compose()
        BUILD_RUNNING = False

    dc_start = subprocess.run(["sudo", "docker-compose", "up", "--build", "-d" ])
    if dc_start.returncode == 0:
        print()    

        ###### WEB ######
        print(bcolors.CYAN_IN + "WEB HEALTH CHECK:" + bcolors.CEND)

        get_web = None

        try:
            get_web = requests.get("http://127.0.0.1:80")
            print(bcolors.YELLOW_IN + str(get_web) + bcolors.CEND)
        except Exception as e:
            
            errors.append(e)
            print(bcolors.RED_IN + str(e) + bcolors.CEND)


        
        # "connection reset by peer"
        print()
        time.sleep(3) 
        
        ###### API ######
        print(bcolors.CYAN_IN+ "API HEALTH CHECK:" + bcolors.CEND)
        
        get_api = None

        try:
            get_api = requests.post("http://127.0.0.1:8000/api/validate")
            print(bcolors.YELLOW_IN + str(get_api) + bcolors.CEND)
        except Exception as e:

            errors.append(e)
            print(bcolors.RED_IN + str(e) + bcolors.CEND)


        
        if(not errors and get_web and get_web.status_code == 200 and get_api.status_code == 400):
            print(bcolors.OKGREEN + "BUILD SUCCESSFUL" + bcolors.CEND)
            BUILD_RUNNING = True

            msg['Subject'] = 'SPA BUILD SUCCESSFUL'
            msg.attach(MIMEText('<h3>All services are working!</h3>', 'html'))
            send_mail(msg)

            return

        else:
            # docker-compose keeps running when there is a failed container
            stop_docker_compose()
    
    
    print(bcolors.RED_IN + "BUILD FAILED" + bcolors.CEND)
    msg['Subject'] = 'SPA BUILD FAILED'
    msg.attach(MIMEText('<p>' + str(errors) + '</p>', 'html'))
    send_mail(msg)
    # send email that build failed

def stop_docker_compose():
    dc_stop = subprocess.run(["sudo", "docker-compose", "down"])
    if dc_stop.returncode == 0:
        BUILD_RUNNING = False

def check_service_up(url: str, service: str):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{} - SERVICE IS DOWN!'.format(service)
    
    web_request = None

    """

    This could be heavily restructured if there are more services to be checked
    As of now, the replicated code is not an issue - it's easy to read

    """

    print(bcolors.YELLOW_IN + "CHECKING SERVICE {} ".format(service) + bcolors.CEND)
    
    if service == "WEB":
        try:
            web_request = requests.get(url)
        except Exception as e:
            msg.attach(MIMEText('<h3> GET Request to {} failed with the following exception: </h3> </p> {}'.format(url, str(e)) + '</p>', 'html'))
            send_mail(msg)
            print(bcolors.RED_IN + "{} IS DOWN - {}".format(service, str(url)) + bcolors.CEND)
            return 

        if web_request.status_code != 200:
            # send email that the website is down
            msg.attach(MIMEText('<h3> GET Request to {} failed with status code {}'.format(url, str(web_request.status_code)) + '</h3>', 'html'))
            send_mail(msg)
            print(bcolors.RED_IN + "{} IS DOWN - {}".format(service, str(url)) + bcolors.CEND)
            return
    
    elif service == "API":
        
        BEARER_TOKEN = None
        try: 
            api_env_file = open("./packages/api/.env", "r")
        except Exception as e:
            print(bcolors.RED_IN + "Problem reading .env!" + bcolors.CEND)

        for line in api_env_file.readlines():
            if "AUTH_TOKEN" in line:
                BEARER_TOKEN = line.replace("AUTH_TOKEN=", "").replace("\n", "").replace("\"", "")

        if not BEARER_TOKEN:
            print(bcolors.RED_IN + "BEARER IS NOT SET!" + bcolors.CEND)
            return

        try:
            web_request = requests.post(url=url, headers={"BEARER_TOKEN": BEARER_TOKEN})
        except Exception as e:
            msg.attach(MIMEText('<h3> POST Request to {} failed with the following exception: </h3> </p> {}'.format(url, str(e)) + '</p>', 'html'))
            send_mail(msg)
            print(bcolors.RED_IN + "{} IS DOWN - {}".format(service, str(url)) + bcolors.CEND)
            return 

        if web_request.status_code != 200:
            # send email that the website is down
            msg.attach(MIMEText('<h3> POST Request to {} failed with status code {}'.format(url, str(web_request.status_code)) + '</h3>', 'html'))
            send_mail(msg)
            print(bcolors.RED_IN + "{} IS DOWN - {}".format(service, str(url)) + bcolors.CEND)
            return


    print(bcolors.OKGREEN + "Nothing unusual!" + bcolors.CEND)

"""
    TO DO:

5 minutes CRON job checking check_web_up(local), check_web_up(dev) and check_web_up(prod)
5 minutes CRON job checking check_api_up(local) and check_api_up(dev)

if locals are down -> redeploy app

"""

check_service_up("http://127.0.0.1:3000", "WEB")
check_service_up("http://127.0.0.1:8000/api/validate", "API")
