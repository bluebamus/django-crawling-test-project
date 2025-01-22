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
        self.proxy_list = [
            {'ip': '121.161.79.38', 'port': '3128', 'type': 'http'},
        ]
        self.ua = UserAgent()
        
    def get_random_proxy(self):
        """
        HTTP 프록시 중 하나를 랜덤하게 선택하여 반환합니다.
        :return: 선택된 프록시 정보 (딕셔너리)
        """
        return random.choice(self.proxy_list)

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
            proxy_addr = f"{proxy_info['ip']}:{proxy_info['port']}"
            logging.info(f"Setting up HTTP proxy: {proxy_addr}")
            options.add_argument(f'--proxy-server={proxy_addr}')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # 자동화 감지 방지 스크립트
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # DNS Leak Test 페이지로 이동
        driver.get("https://dnsleaktest.com/")  # DNS Leak Test 페이지 요청
        logging.info("Accessing DNS Leak Test page.")  # 페이지 접근 로그

        # "Standard test" 버튼이 로드될 때까지 대기
        wait = WebDriverWait(driver, 20)  # 최대 20초 대기
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @class='standard' and @name='type' and @value='Standard test']")))  # 특정 요소가 로드될 때까지 대기
        
        return driver  # 설정된 드라이버 반환
        

    def visit_and_click(self, url):
        """
        주어진 URL에 접근하여 페이지를 크롤링하고,
        페이지 내의 이미지 요소를 찾아 클릭합니다.
        
        :param url: 크롤링할 URL
        """
        driver = None  # 드라이버 변수를 초기화
        try:
            proxy_info = self.get_random_proxy()
            logging.info(f"Selected proxy: {proxy_info}")
            
            driver = self.setup_driver(proxy_info)
            
            # 페이지 로드 시간 랜덤화
            load_wait = random.uniform(3, 7)
            time.sleep(load_wait)
            
            # 목표 URL 접속
            driver.get(url)
            logging.info(f"Accessing URL: {url} with proxy: {proxy_info}")
            
            # 자바스크립트 로드 완료 대기
            wait = form_element = WebDriverWait(driver, 10)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 이미지 요소들이 로드될 때까지 대기
            images = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img-fluid")))
            
            # 발견된 모든 이미지 로깅
            for idx, img in enumerate(images):
                src = img.get_attribute('src')
                logging.info(f"Found image {idx + 1}: {src}")
            
            view_wait = random.uniform(1, 3)
            time.sleep(view_wait)
            
            # 랜덤 이미지 선택 및 클릭
            while True:
                try:
                    random_image = random.choice(images)  # 요소를 다시 검색
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", random_image)
                    time.sleep(random.uniform(0.5, 1.5))
                    random_image.click()
                    logging.info(f"Clicked image: {random_image.get_attribute('src')}")
                    break  # 클릭 성공 시 루프 종료
                except StaleElementReferenceException:
                    # 요소가 더 이상 유효하지 않으면 다시 검색
                    logging.warning("Stale element reference, re-fetching images.")
                    images = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img-fluid")))
            
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
        
        finally:
            if driver is not None:  # driver가 None이 아닐 때만 quit 호출
                driver.quit()
    
    
    # 여러 번 실행하기 위한 루프 (주석 처리됨)
    """
    for i in range(10):  # 10회 반복
        crawler.visit_and_click(base_url)
        # 요청 간격 랜덤화
        time.sleep(random.uniform(5, 15))
    """

def main():
    """
    프로그램의 진입점입니다.
    BannerCrawler 인스턴스를 생성하고, 지정된 URL에 대해 크롤링을 수행합니다.
    """
    crawler = BannerCrawler()
    base_url = "http://localhost:8000"
    crawler.visit_and_click(base_url)

if __name__ == "__main__":
    main() 