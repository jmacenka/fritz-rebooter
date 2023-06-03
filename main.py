# fritz-rebooter Web-Service to restart a Fritz!BOX 6690
# Created by Jan Macenka @ 27 Arp 2023

# Library imports
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzstatus import FritzStatus
from datetime import datetime, timedelta

# Initialize the variables. Make sure you have the .env file configured.
load_dotenv()
FRITZ_IP_ADDRESS = os.environ.get('FRITZ_IP_ADDRESS', '')
FRITZ_USERNAME = os.environ.get('FRITZ_USERNAME', '')
FRITZ_PASSWORD = os.environ.get('FRITZ_PASSWORD', '')

# Parameters
reconnect_deadband_minutes = 30

# Instantiate the Flask App
app = FastAPI()

# Configure logging
logging.basicConfig(filename='/var/log/fritz-rebooter.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S UTC+0')

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logging.info(f"Request: {request.method} {request.url} | Response: {response.status_code}")
    return response

@app.get('/reconnect')
def handle_reconnect_GET():
    # Connection error handling
    status, uptime = None, 0
    now = datetime.now()
    try:
        fc = FritzConnection(address=FRITZ_IP_ADDRESS,
                             user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
        fs = FritzStatus(address=FRITZ_IP_ADDRESS,
                         user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
        status = fc.device_description
        uptime = fs.connection_uptime
    except:
        pass
    if not status:
        return f'Unable to connect to {FRITZ_IP_ADDRESS}'
    return f'You are connected to {fc.device_description} @ {FRITZ_IP_ADDRESS}. Connection-Uptime is {uptime}s.'


@app.post('/reconnect')
def handle_reconnect_POST():
    # Connection error handling
    status, uptime = None, 0
    now = datetime.now()
    try:
        fc = FritzConnection(address=FRITZ_IP_ADDRESS,
                             user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
        fs = FritzStatus(address=FRITZ_IP_ADDRESS,
                         user=FRITZ_USERNAME, password=FRITZ_PASSWORD)
        status = fc.device_description
        uptime = fs.connection_uptime
    except:
        pass
    if not status:
        return f'Unable to connect to {FRITZ_IP_ADDRESS}'

    if int(uptime) / 60 > reconnect_deadband_minutes:
        fc.call_action('WANIPConn1', "ForceTermination")
        return 'reconnected'
    else:
        return 'currently in reconnect deadband'
