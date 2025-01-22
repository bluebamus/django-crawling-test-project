import requests
import logging

# 프록시 리스트
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

# 로깅 설정
logging.basicConfig(
    filename='proxy_test_chatgpt.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 성공한 프록시 저장 파일명
success_log_file = "success_proxies_chatgpt.log"

def test_proxy(proxy_info):
    """
    개별 프록시 테스트 함수
    """
    proxy_url = f"{proxy_info['type']}://{proxy_info['ip']}:{proxy_info['port']}"
    proxies = {"http": proxy_url, "https": proxy_url}

    try:
        response = requests.get('http://api.ipify.org', proxies=proxies, timeout=5)
        response.raise_for_status()

        # 프록시 테스트 성공 로그
        logging.info(f"✅ Proxy succeeded: {proxy_url}")
        print(f"✅ Proxy succeeded: {proxy_url}")

        # 성공한 프록시 정보를 파일에 저장
        with open(success_log_file, "a") as success_file:
            success_file.write(f"{{'ip': '{proxy_info['ip']}', 'port': '{proxy_info['port']}', 'type': '{proxy_info['type']}'}}\n")

    except requests.RequestException as e:
        # 프록시 테스트 실패 로그
        logging.error(f"❌ Proxy failed: {proxy_url} | Error: {e}")
        print(f"❌ Proxy failed: {proxy_url} | Error: {e}")

def test_all_proxies():
    """
    전체 프록시 테스트
    """
    print("Testing all proxies...\n")
    for proxy in proxy_list['http']:
        test_proxy(proxy)
    print("\nProxy testing completed.")

if __name__ == "__main__":
    test_all_proxies()
