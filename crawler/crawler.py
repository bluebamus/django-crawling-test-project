from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import os
from fake_useragent import UserAgent
import logging
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
import requests
from requests.exceptions import Timeout, ProxyError, ConnectionError, HTTPError, RequestException


# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crawler.log'
)

class BannerCrawler:
    """
    BannerCrawler 클래스는 웹 크롤링을 수행하는 클래스입니다.
    이 클래스는 프록시 서버를 사용하여 웹 페이지에 접근하고,
    페이지에서 특정 요소를 찾고 상호작용하는 기능을 제공합니다.
    """

    def __init__(self):
        # HTTP 프록시 서버 리스트
        # self.proxy_list = [
        #     {'ip': '211.225.214.241', 'port': '80', 'type': 'http'},
        #     {'ip': '211.202.167.56', 'port': '80', 'type': 'http'},
        #     {'ip': '211.34.105.33', 'port': '80', 'type': 'http'},
        #     {'ip': '154.90.63.164', 'port': '3128', 'type': 'http'},
        #     {'ip': '193.123.252.70', 'port': '35973', 'type': 'socks5'},
        #     {'ip': '45.64.173.109', 'port': '80', 'type': 'http'},
        # ]
        self.proxy_list = [
            '49.254.147.104:5320',
            '49.254.145.27:6562',
            '49.254.40.98:6915',
            '115.144.117.241:5018',
            '49.254.60.40:6953',
            '49.254.205.189:6746',
            '121.126.129.151:5255',
            '183.78.134.78:6371',
            '49.254.24.198:6825',
            '183.78.134.76:6369',
            '121.126.106.175:5471',
            '121.126.139.175:5644',
            '124.198.21.50:6017',
            '121.126.47.35:5835',
            '49.254.126.142:5606',
            '121.126.28.216:5128',
            '124.198.73.220:5264',
            '49.254.186.134:6660',
            '124.198.29.14:6037',
            '49.254.114.2:6475',
            '115.144.239.224:5160',
            '115.144.250.223:5327',
            '49.254.32.143:6904',
            '121.126.64.105:5481',
            '49.254.190.27:6680',
            '49.254.127.126:6518',
            '115.144.44.74:5409',
            '121.126.182.208:5376',
            '121.126.177.245:5393',
            '121.126.204.242:5710',
            '49.254.206.12:6753',
            '115.144.201.15:5263',
            '49.254.191.72:6685',
            '49.254.33.85:5341',
            '124.198.12.11:5994',
            '124.198.10.75:5954',
            '49.254.117.250:5027',
            '115.144.225.79:5159',
            '49.254.127.121:6513',
            '121.126.52.166:5854',
            '115.144.4.77:5388',
            '49.254.9.25:7017',
            '49.254.24.194:6821',
            '49.254.189.121:6663',
            '49.254.127.123:6515',
            '124.198.43.139:6082',
            '49.254.23.118:6801',
            '49.254.224.178:5027',
            '49.254.24.197:6824',
            '115.144.234.138:5370',
            '121.126.86.140:5908',
            '121.126.175.237:5221',
            '115.144.251.2:5329',
            '183.78.129.90:6351',
            '49.254.126.141:5605',
            '124.198.36.200:5432',
            '49.254.138.186:6545',
            '115.144.7.161:5487',
            '125.7.134.146:6272',
            '115.144.143.31:5088',
            '49.254.28.55:6881',
            '49.254.251.79:6866',
            '49.254.251.73:6860',
            '115.144.30.34:5353',
            '121.126.95.1:5936',
            '121.126.64.110:5486',
            '203.109.26.236:5676',
            '115.144.254.118:5341',
            '121.126.183.221:5101',
            '202.126.114.18:6391',
            '49.254.124.7:6511',
            '121.126.137.148:5633',
            '115.144.22.39:5287',
            '124.198.125.150:5318',
            '121.126.4.109:5493',
            '115.144.79.29:5507',
            '115.144.61.193:5455',
            '49.254.16.15:6606',
            '115.144.79.31:5509',
            '202.126.114.23:6396',
            '125.7.137.106:5418',
            '121.126.148.115:5060',
            '115.144.221.202:5290',
            '121.126.23.233:5553',
            '121.126.199.81:5705',
            '121.126.137.146:5631',
            '49.254.21.98:5298',
            '115.144.170.20:5141',
            '124.198.101.103:5966',
            '115.144.30.38:5357',
            '124.198.37.141:6068',
            '121.126.95.6:5941',
            '124.198.72.26:6161',
            '115.144.52.121:5432',
            '124.198.16.40:6007',
            '121.126.88.99:5683',
            '49.254.224.176:5025',
            '49.254.206.213:5125',
            '124.198.125.149:5317',
            '121.126.221.197:5721',
        ]
        self.ua = UserAgent()
        
    def get_proxy(self, current_proxy):
        """
        현재 프록시를 기준으로 다음 프록시 정보를 반환합니다.
        :param current_proxy: 현재 프록시 정보 (딕셔너리)
        :return: 다음 프록시 정보 (딕셔너리)
        """
        current_index = self.proxy_list.index(current_proxy)  # 현재 프록시의 인덱스 찾기
        next_index = (current_index + 1) % len(self.proxy_list)  # 다음 인덱스 계산 (순환)
        return self.proxy_list[next_index]  # 다음 프록시 반환

    def get_user_agent(self, index=None):
        """
        User Agent를 가져오는 함수
        
        fake-useragent 라이브러리는 다음과 같은 브라우저 User Agent를 제공합니다:
        
        인덱스별 User Agent 종류:
        - 'chrome': 크롬 브라우저 (예: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36)
        - 'firefox': 파이어폭스 브라우저 (예: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0)
        - 'safari': 사파리 브라우저 (예: Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15)
        - 'edge': 엣지 브라우저 (예: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0)
        - 'opera': 오페라 브라우저 (예: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0)
        
        사용 예시:
        - get_user_agent('chrome'): 크롬 브라우저의 User Agent 반환
        - get_user_agent('firefox'): 파이어폭스 브라우저의 User Agent 반환
        - get_user_agent(None): 랜덤한 브라우저의 User Agent 반환
        
        :param index: 특정 브라우저의 User Agent를 선택하기 위한 인덱스 (None이면 랜덤)
        :return: User Agent 문자열
        """
        if index is None:
            return self.ua.random
        return self.ua[index]
    
    def setup_driver(self, proxy_info):
        """
        Selenium 웹 드라이버를 설정합니다.
        주어진 프록시 정보를 사용하여 Chrome 드라이버를 설정하고,
        자동화 감지 방지 스크립트를 추가합니다.
        
        :param proxy_info: 사용할 프록시 정보 (딕셔너리)
        :return: 설정된 Selenium 웹 드라이버
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'user-agent={self.get_user_agent()}')
        
        # 브라우저 창 크기 랜덤화
        window_sizes = [(1366, 768), (1920, 1080), (1440, 900), (1536, 864)]
        window_size = random.choice(window_sizes)
        options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        
        # HTTP 프록시 설정
        # if proxy_info:
        #     proxy_addr = f"{proxy_info['ip']}:{proxy_info['port']}"
        #     logging.info(f"Setting up HTTP proxy: {proxy_addr}")
        #     options.add_argument(f'--proxy-server={proxy_addr}')
        if proxy_info:
            logging.info(f"Setting up HTTP proxy: {proxy_info}")
            options.add_argument(f'--proxy-server={proxy_info}')
   
        # Chrome 드라이버 설정
        service = Service(ChromeDriverManager().install())
        service.log_path = 'chromedriver.log'  # 로그 파일 경로
        service.log_level = 'DEBUG'  # 로그 레벨 설정

        driver = webdriver.Chrome(service=service, options=options)
        
        # 자동화 감지 방지 스크립트
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # DNS Leak Test 페이지로 이동
        driver.set_page_load_timeout(10)
        # driver.get("https://dnsleaktest.com/")  # DNS Leak Test 페이지 요청
        # logging.info("Accessing DNS Leak Test page.")  # 페이지 접근 로그

        # # "Standard test" 버튼이 로드될 때까지 대기
        # wait = WebDriverWait(driver, 10)  # 최대 20초 대기
        # wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @class='standard' and @name='type' and @value='Standard test']")))  # 특정 요소가 로드될 때까지 대기
        
        return driver  # 설정된 드라이버 반환
        

    def visit_and_click(self, url):
        """
        주어진 URL에 접근하여 페이지를 크롤링하고,
        페이지 내의 이미지 요소를 찾아 클릭합니다.
        
        :param url: 크롤링할 URL
        """
        current_index = 0  # 현재 프록시 인덱스 초기화
        total_proxies = len(self.proxy_list)  # 총 프록시 수

        while current_index < total_proxies:  # 무한 루프를 통해 프록시를 순환
            # proxy_info = self.get_proxy(self.proxy_list[current_index])  # 현재 프록시 가져오기
            # proxy_url = f"{proxy_info['type']}://{proxy_info['ip']}:{proxy_info['port']}"
            # proxies = {
            #     'http': proxy_url,
            #     'https': proxy_url
            # }
            proxy_info = self.proxy_list[current_index]  # 현재 프록시 가져오기
            proxy_url = f"http://{proxy_info}"
            proxies = {
                'http': proxy_info,
                'https': proxy_info
            }

            try:
                
                try:
                    response = requests.get('http://api.ipify.org', proxies=proxies, timeout=5)
                    response.raise_for_status()  # HTTP 에러 상태 코드가 있으면 예외 발생
                except (Timeout, ProxyError, ConnectionError, HTTPError) as e:
                    logging.error(f"❌ Proxy failed: {proxy_url} | Error: {e}")
                    current_index += 1
                    continue
                except RequestException as e:
                    logging.info(f"An error occurred: {e}")
                    current_index += 1
                    continue
                    
                logging.info(f"Using proxy: {proxy_url}")
                
                # 프록시 IP의 위치 정보 확인
                ip_info_response = requests.get(f'https://ipinfo.io/{proxy_info.split(":")[0]}/json', proxies=proxies)
                ip_info_response.raise_for_status()  # HTTP 에러 상태 코드가 있으면 예외 발생
                ip_info = ip_info_response.json()
                country = ip_info.get('country', 'Unknown')
                city = ip_info.get('city', 'Unknown')

                # 특정 로그를 별도의 파일에 저장하기 위한 설정
                specific_logger = logging.getLogger('specific_logger')
                specific_handler = logging.FileHandler('crawler_hl_ipl_list.txt')
                specific_handler.setLevel(logging.INFO)
                specific_formatter = logging.Formatter('%(asctime)s - %(message)s')
                specific_handler.setFormatter(specific_formatter)
                specific_logger.addHandler(specific_handler)

                specific_logger.info(f"Proxy IP {proxy_info} is located in {city}, {country}")

                
                # Selenium 드라이버 설정
                driver = self.setup_driver(proxy_info)
                driver.get(url)  # 주어진 URL로 이동

                # 페이지 로드 완료 대기
                wait = WebDriverWait(driver, 10)
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

                # 이미지 요소들이 로드될 때까지 대기
                images = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img-fluid")))

                # 발견된 모든 이미지 로깅
                for idx, img in enumerate(images):
                    src = img.get_attribute('src')
                    logging.info(f"Found image {idx + 1}: {src}")

                # 랜덤 이미지 선택 및 클릭
                random_image = random.choice(images)
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_image)
                time.sleep(random.uniform(0.5, 1.5))
                
                # 이미지 요소의 XPath를 사용하여 다시 찾기
                image_xpath = f"//img[@alt='Test {images.index(random_image) + 1}']"  # 이미지 인덱스에 따라 XPath 설정
                try:
                    # 요소가 나타날 때까지 최대 10초 대기
                    random_image = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, image_xpath))
                    )
                    logging.info(f"Clicked image: {random_image.get_attribute('src')}")
                    random_image.click()  # 클릭 동작
                except NoSuchElementException:
                    logging.warning("NoSuchElementException: 요소를 찾을 수 없습니다.")
                except StaleElementReferenceException:
                    logging.warning("StaleElementReferenceException: 요소가 더 이상 유효하지 않습니다. 다시 시도합니다.")
                    # 필요시 다시 시도하는 로직 추가

                driver.quit()  # 작업 완료 후 드라이버 종료
                
                 # 다음 프록시로 인덱스 증가
                current_index += 1

                # 다음 프록시가 있는지 확인
                if current_index >= total_proxies:
                    logging.error("All proxies have been tested and failed.")
                    print("All proxies have been tested and failed.")
                    break  # 모든 프록시를 테스트한 경우 루프 종료
                else:
                    continue  # 다음 프록시로 계속 진행


            except requests.RequestException as e:
                logging.error(f"❌ Proxy failed: {proxy_url} | Error: {e}")
                print(f"❌ Proxy failed: {proxy_url} | Error: {e}")


def main():
    """
    프로그램의 진입점입니다.
    BannerCrawler 인스턴스를 생성하고, 지정된 URL에 대해 크롤링을 수행합니다.
    """
    crawler = BannerCrawler()
    base_url = "https://bluebamus.pythonanywhere.com/"
    # base_url = "http://127.0.0.1:8000"
    crawler.visit_and_click(base_url)

if __name__ == "__main__":
    main() 