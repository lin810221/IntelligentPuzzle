import requests
import warnings

warnings.filterwarnings('ignore')

class Api:
    def __init__(self, url, method='get', max_retries=1, timeout=3):
        self.url = url
        self.max_retries = max_retries
        self.retry_count = 0
        self.method = method
        self.timeout = timeout
    
    def fetch_data(self, method, timeout):
        try:
            if self.method.lower() == 'get':
                response = requests.get(self.url, verify=False, timeout = self.timeout)
            elif self.method.lower() == 'post':
                response = requests.post(self.url)
            else:
                raise ValueError('Invalid HTTP method. Only "GET" and "POST" are supported.')
            
            if response.status_code != 200:
                self.retry_count += 1
                print(f'連線失敗 {self.retry_count} 次，HTTP 狀態碼: {response.status_code}')
                return None, response.status_code

            return response.text, response.status_code

        except:
            self.retry_count += 1
            print(f'連線失敗{self.retry_count}次')
            return None, None

    def crawl(self):
        while self.retry_count < self.max_retries:
            content, status_code = self.fetch_data(self.method, self.timeout)
            if content is not None:
                print(f'連線成功！HTTP 狀態碼: {status_code}')
                return content
        print('連線失敗，已達最大重試次數。')
        return None

url = 'https://example.com'
result = Api(url=url, max_retries=3).crawl()
