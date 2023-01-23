from .models import Endpoint, Request
from datetime import datetime
import threading
import requests

def request_endpoint(endpoint, lock):

    print(f"Sending requests to {endpoint.endpoint} at: {datetime.now()}")
    status = 200
    try:
        print(f'Request sent to {endpoint.endpoint}')
        response = requests.get(endpoint.endpoint)
        status = response.status_code
    except Exception:
        status = 503
    Request.objects.create(endpoint=endpoint, result=status)

    if status < 200 or status >= 300:
        with lock:
            endpoint.fail_times += 1
            endpoint.save()


def cron_func():

    print('in cron_func function...')
    endpoints = Endpoint.objects.all()
    lock = threading.Lock()

    for endpoint in endpoints:
        t = threading.Thread(target=request_endpoint, args=[endpoint, lock], daemon=True)
        t.start()
