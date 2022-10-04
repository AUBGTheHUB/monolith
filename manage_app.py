#!/usr/bin/env python3
import subprocess
import requests
import time
import os

BUILD_RUNNING = False

EMAIL_USERNAME = os.getenv("HUB_MAIL_USERNAME")
EMAIL_PWD = os.getenv("HUB_MAIL_APP_PWD")

class bcolors:
    YELLOW_IN = '\033[33m'
    YELLOW_OUT = '\033[43m' 
    RED_IN = '\033[31m'
    CYAN_IN = '\033[93m'
    RED_OUT = '\033[41m'
    OKGREEN = '\033[92m'
    CEND = '\033[0m'

def start_docker_compose():
    # --abort-on-container-exit is not compatible with detached mode
    # therefore check up should be done with requests
    global BUILD_RUNNING

    if BUILD_RUNNING:
        stop_docker_compose()
        BUILD_RUNNING = False

    dc_start = subprocess.run(["sudo", "docker-compose", "up", "--build", "-d" ])
    if dc_start.returncode == 0:
        print()    

        print(bcolors.CYAN_IN + "WEB HEALTH CHECK:" + bcolors.CEND)
        get_web = requests.get("http://127.0.0.1:80")
        print(bcolors.YELLOW_IN + str(get_web) + bcolors.CEND)
        
        # "connection reset by peer"
        print()
        time.sleep(2) 

        print(bcolors.CYAN_IN+ "API HEALTH CHECK:" + bcolors.CEND)
        get_api = requests.post("http://127.0.0.1:8000/api/validate")
        print(bcolors.YELLOW_IN + str(get_api) + bcolors.CEND)

        if(get_web.status_code == 200 and get_api.status_code == 400):
            print(bcolors.OKGREEN + "BUILD SUCCESSFUL" + bcolors.CEND)
            BUILD_RUNNING = True
            # send email
            return
        else:
            # docker-compose keeps running when there is a failed container
            stop_docker_compose()

    # send email that build failed
    print(bcolors.RED_IN + "BUILD FAILED" + bcolors.CEND)

def stop_docker_compose():
    dc_stop = subprocess.run(["sudo", "docker-compose", "down"])
    if dc_stop.returncode == 0:
        BUILD_RUNNING = False

start_docker_compose()
