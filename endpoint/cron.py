from .models import Endpoint, Request
import concurrent.futures
import datetime
import threading
import requests

def request_endpoint(endpoint, lock):

    print(f"Sending requests to {endpoint.endpoint} at: {datetime.now()}"):
    status = 200
    try:
        response = requests.get(endpoint.endpoint, verify=False)
        status = response.status_code
    except Exception:
        status = 503
    Request.objects.create(endpoint=endpoint, result=status)

    if status < 200 or status >= 300:
        with lock:
            endpoint.fail_times += 1
            endpoint.save()


def cron_func():

    endpoints = Endpoint.objects.all()
    lock = threading.Lock()
    lock_list = [lock for _ in endpoints]
    args_list = list(zip(endpoints, lock_list))

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(request_endpoint, args_list)
