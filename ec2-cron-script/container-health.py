import docker
import requests
import json
from datetime import datetime, timedelta
import sys
DOCKER_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')
RUNNING = 'running'

def is_running(container_name):
    """
    verify the status of a sniffer container by it's name
    :param container_name: the name of the container
    :return: Boolean if the status is ok
    """
    container = DOCKER_CLIENT.containers.get(container_name)
    container_state = container.attrs['State']
    container_is_running = container_state['Status'] == RUNNING
    return container_is_running

def main():
    my_container_name = "festive_benz"
    url = "https://hooks.slack.com/services/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"
    slack_data = {
        "username": "BitcoinPredictorBot",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": "Container Unavailable",
                        "value": "Bitcoin Predictor container hosted at http://3.144.206.118:5000/ is not running.",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    
    if not is_running(my_container_name):
        with open('ContainerHealthLog.txt') as f:
            for line in f:
                pass
            last_line = line
        
        if last_line == "InService":
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
            
            file = open("ContainerHealthLog.txt", "w+")
            file.write("\n" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        elif datetime.now() > (datetime.strptime(last_line, "%m/%d/%Y, %H:%M:%S") + timedelta(hours=24)):
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
        else:
            return
    else:
        with open('ContainerHealthLog.txt') as f:
            for line in f:
                pass
            last_line = line
        if(last_line != "InService"):
            file = open("ContainerHealthLog.txt", "w+")
            file.write("\nInService")
            

if __name__ == "__main__":
    main()