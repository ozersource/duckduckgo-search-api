import requests
from bs4 import BeautifulSoup
import random


class Duckduckgo:

    def __init__(self, proxies=None):

        if proxies is not None:
            self.proxies_direct_list = self.__load_proxies(proxies)
        else:
            self.proxies_direct_list = None
        self.endpoint = 'https://html.duckduckgo.com/html/'
        self.headers = {
            'Cache-Control': 'no-cache',
            'Content-Length': '11',
            'Origin': 'https://html.duckduckgo.com',
            'Pragma': 'no-cache',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

    def __load_proxies(self, input):
        if isinstance(input, str):
            with open(input, 'r') as file:
                proxies = file.readlines()
            proxy_list = [proxy.strip() for proxy in proxies]
        elif isinstance(input, list):
            proxy_list = input
        else:
            raise ValueError("Error format input")

        formatted_proxies = self.__format_proxies(proxy_list)
        if len(formatted_proxies) == 0:
            raise ValueError("Error format proxies input")
        return formatted_proxies

    def __format_proxies(self,proxies):
        formatted_proxy_list = []
        for proxy in proxies:
            try:
                ip_port, user_pass = proxy.split('@')
                formatted_proxy = f"{user_pass}@{ip_port}"
                formatted_proxy_list.append(formatted_proxy)
            except ValueError:
                continue
        return formatted_proxy_list

    def __get_random_proxy(self,proxy_list):

        if not proxy_list:
            raise ValueError("Empty list")

        random_proxy = random.choice(proxy_list)
        proxy_dict = {
            'http': f"http://{random_proxy}",
            'https': f"http://{random_proxy}"
        }
        return proxy_dict

    def __parse_response(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        results = soup.find_all("div", class_="result")
        parsed_results = []
        for result in results:
            title = result.find("h2", class_="result__title").get_text(strip=True)
            url = result.find("a", class_="result__a")['href']
            description = result.find("a", class_="result__snippet")
            description = description.get_text(strip=True) if description else "No description available"
            parsed_results.append({"title": title, "url": url, "description": description})
        return {"success": True, "data": parsed_results}

    def search(self, query):
        params = {'q': query, "b": ""}
        try:
            if self.proxies_direct_list is not None:
                response = requests.post(self.endpoint, data=params, headers=self.headers,proxies=self.__get_random_proxy(self.proxies_direct_list), timeout=5)
                #print(response.content)
            else:
                response = requests.post(self.endpoint, data=params, headers=self.headers, timeout=5)
            #print(response.content)
            response.raise_for_status()  # This will raise an HTTPError if the status is 4xx, 5xx
            return self.__parse_response(response.content)
        except requests.exceptions.RequestException as e:
            return {"success": False, "statusCode": e.response.status_code if e.response else None,
                    "message": f"Error making request: {e}"}
        except Exception as e:
            return {"success": False, "statusCode": None, "message": f"Error parsing response: {e}"}



