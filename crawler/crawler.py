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
        self.proxy_list = [
            '211.34.105.33:80',
            '211.34.105.33:80',
            '211.34.105.33:80',
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
        
        # DevTools Protocol로 네트워크 요청 제어 활성화
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {
            "urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.css", "*.js", "*.woff", "*.svg"]
        })
        
        driver.set_page_load_timeout(10)

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