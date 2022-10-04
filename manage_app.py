#!/usr/bin/env python3
import subprocess

def start_docker_compose():
    dc_start = subprocess.run(["sudo", "docker-compose", "up", "-d"])
    if dc_start.returncode == 0:
        # send email 
        print("BUILD SUCCESSFUL")
    else:
        # send email
        print("BUILD FAILED")

def stop_docker_compose():
    dc_stop = subprocess.run(["sudo", "docker-compose", "down"])

stop_docker_compose()
