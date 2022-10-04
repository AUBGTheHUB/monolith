#!/usr/bin/env python3
import subprocess
import requests
import time
import os
import smtplib as smtp, ssl, os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    server.sendmail(email, email, msg.as_string())
    server.close()

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

start_docker_compose()
