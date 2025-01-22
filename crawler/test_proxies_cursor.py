import requests
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='proxy_test_cursor.log'
)

# 성공한 프록시 정보를 저장할 파일
success_log_file = 'success_proxies_cursor.log'

# https://spys.one/free-proxy-list/KR/
# 프록시 서버 리스트
proxy_list = {
    'http': [
        {'ip': '1.237.239.168', 'port': '80', 'type': 'http'},
        {'ip': '203.243.63.16', 'port': '80', 'type': 'http'},
        {'ip': '211.234.125.5', 'port': '443', 'type': 'http'},
        {'ip': '152.67.221.233', 'port': '8008', 'type': 'http'},
        {'ip': '121.161.79.38', 'port': '3128', 'type': 'http'},
        {'ip': '220.85.12.28', 'port': '8080', 'type': 'http'},
        {'ip': '211.225.214.241', 'port': '80', 'type': 'http'},
        {'ip': '211.202.167.56', 'port': '80', 'type': 'http'},
        {'ip': '175.213.76.24', 'port': '80', 'type': 'http'},
        {'ip': '116.42.218.110', 'port': '3128', 'type': 'http'},
        {'ip': '152.69.227.216', 'port': '3128', 'type': 'http'},
        {'ip': '211.109.199.99', 'port': '80', 'type': 'http'},
        {'ip': '3.37.243.105', 'port': '3128', 'type': 'http'},
        {'ip': '218.145.131.182', 'port': '443', 'type': 'http'},
        {'ip': '125.141.133.49', 'port': '5566', 'type': 'http'},
        {'ip': '220.73.144.83', 'port': '10808', 'type': 'http'},
        {'ip': '121.136.189.231', 'port': '60001', 'type': 'http'},
        {'ip': '154.193.40.173', 'port': '808', 'type': 'http'},
        {'ip': '146.56.96.179', 'port': '14280', 'type': 'http'},
        {'ip': '14.34.180.21', 'port': '38157', 'type': 'http'},
        {'ip': '211.38.54.85', 'port': '3008', 'type': 'http'},
        {'ip': '146.56.101.184', 'port': '21681', 'type': 'http'},
        {'ip': '146.56.98.157', 'port': '13128', 'type': 'http'},
        {'ip': '129.154.54.26', 'port': '3128', 'type': 'http'},
        {'ip': '146.56.191.98', 'port': '14785', 'type': 'http'},
        {'ip': '15.164.83.234', 'port': '8080', 'type': 'http'},
        {'ip': '211.38.54.85', 'port': '3010', 'type': 'http'},
        {'ip': '121.126.68.66', 'port': '22551', 'type': 'http'},
        {'ip': '124.198.103.81', 'port': '28124', 'type': 'http'}
    ]
}

def test_proxy(proxy):
    proxy_type = proxy['type']
    proxy_address = f"{proxy_type}://{proxy['ip']}:{proxy['port']}"
    proxies = {
        'http': proxy_address,
        'https': proxy_address
    }
    
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code == 200:
            logging.info(f"Proxy {proxy_address} is working. Response: {response.json()}")
            print(f"Proxy {proxy_address} is working. Response: {response.json()}")
            # 성공한 프록시 정보를 파일에 저장
            with open(success_log_file, 'a') as f:
                f.write(f"{proxy}\n")  # {'ip': '1.237.239.168', 'port': '80', 'type': 'http'} 형식으로 저장
        else:
            logging.error(f"Proxy {proxy_address} returned status code: {response.status_code}")
            print(f"Proxy {proxy_address} returned status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Proxy {proxy_address} failed: {str(e)}")
        print(f"Proxy {proxy_address} failed: {str(e)}")

def main():
    for proxy_type, proxies in proxy_list.items():
        for proxy in proxies:
            test_proxy(proxy)

if __name__ == "__main__":
    main() 