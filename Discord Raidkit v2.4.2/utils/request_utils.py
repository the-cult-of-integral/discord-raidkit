"""
Discord Raidkit v2.4.2
the-cult-of-integral

Last modified: 2023-04-29 19:01
"""

import typing

import conf.config as conf
import requests
import requests.exceptions as reqex

import utils.log_utils as lu

PROXY_FAIL = 'All proxies failed. Please check your proxy configuration.'


class AllProxiesFailedException(Exception):
    """Exception raised when all proxies fail."""


class RequestHandler:

    def __init__(self, proxy_config: conf.ProxyConfig):
        self.proxy_config = proxy_config

    def get(self, url: str, headers: typing.Dict[str, str], timeout: int = 15) -> requests.Response:
        """Send a GET request to the given URL using proxies if enabled.

        If a proxy times out or fails, the next proxy is used. If all proxies fail, an AllProxiesFailedException is raised.
        """
        if not self.proxy_config.is_using_proxies():
            response = requests.get(url, headers=headers)
            return response
        
        proxies = self.proxy_config.__read_from_proxy_file()
        for protocol in self.proxy_config.PROTOCOLS:
            for proxy in proxies[protocol]:
                try:
                    response = requests.get(url, headers=headers, proxies={protocol: proxy}, timeout=timeout)
                    response.raise_for_status()
                    return response
                except (reqex.Timeout, reqex.RequestException):
                    print(f"Proxy {proxy} failed. Trying next one...")
                    lu.swarning(f"Proxy {proxy} failed. Trying next one...")
        print(PROXY_FAIL)
        lu.swarning(PROXY_FAIL)
        raise AllProxiesFailedException(PROXY_FAIL)
    
    def post(self, url: str, headers: typing.Dict[str, str], 
                json: typing.Union[typing.Dict[str, typing.Any], str], timeout: int = 15) -> requests.Response:
        """Send a POST request to the given URL using proxies if enabled.

        If a proxy times out or fails, the next proxy is used. If all proxies fail, an AllProxiesFailedException is raised.
        """
        if not self.proxy_config.is_using_proxies():
            response = requests.post(url, headers=headers, json=json)
            return response

        proxies = self.proxy_config.__read_from_proxy_file()
        for protocol in self.proxy_config.PROTOCOLS:
            for proxy in proxies[protocol]:
                try:
                    response = requests.post(url, headers=headers, json=json, proxies={protocol: proxy}, timeout=timeout)
                    response.raise_for_status()
                    return response
                except (reqex.Timeout, reqex.RequestException):
                    print(f"Proxy {proxy} failed. Trying next one...")
                    lu.swarning(f"Proxy {proxy} failed. Trying next one...")
        print(PROXY_FAIL)
        lu.swarning(PROXY_FAIL)
        raise AllProxiesFailedException(PROXY_FAIL)
    
    def patch(self, url: str, headers: typing.Dict[str, str], 
                json: typing.Union[typing.Dict[str, typing.Any], str], timeout: int = 15) -> requests.Response:
        """Send a PATCH request to the given URL using proxies if enabled.

        If a proxy times out or fails, the next proxy is used. If all proxies fail, an AllProxiesFailedException is raised.
        """
        if not self.proxy_config.is_using_proxies():
            response = requests.patch(url, headers=headers, json=json)
            return response

        proxies = self.proxy_config.__read_from_proxy_file()
        for protocol in self.proxy_config.PROTOCOLS:
            for proxy in proxies[protocol]:
                try:
                    response = requests.patch(url, headers=headers, json=json, proxies={protocol: proxy}, timeout=timeout)
                    response.raise_for_status()
                    return response
                except (reqex.Timeout, reqex.RequestException):
                    print(f"Proxy {proxy} failed. Trying next one...")
                    lu.swarning(f"Proxy {proxy} failed. Trying next one...")
        print(PROXY_FAIL)
        lu.swarning(PROXY_FAIL)
        raise AllProxiesFailedException(PROXY_FAIL)
    
    def delete(self, url: str, headers: typing.Dict[str, str], timeout: int = 15) -> requests.Response:
        """Send a DELETE request to the given URL using proxies if enabled.

        If a proxy times out or fails, the next proxy is used. If all proxies fail, an AllProxiesFailedException is raised.
        """
        if not self.proxy_config.is_using_proxies():
            response = requests.delete(url, headers=headers)
            return response
        
        proxies = self.proxy_config.__read_from_proxy_file()
        for protocol in self.proxy_config.PROTOCOLS:
            for proxy in proxies[protocol]:
                try:
                    response = requests.delete(url, headers=headers, proxies={protocol: proxy}, timeout=timeout)
                    response.raise_for_status()
                    return response
                except (reqex.Timeout, reqex.RequestException):
                    print(f"Proxy {proxy} failed. Trying next one...")
                    lu.swarning(f"Proxy {proxy} failed. Trying next one...")
        print(PROXY_FAIL)
        lu.swarning(PROXY_FAIL)
        raise AllProxiesFailedException(PROXY_FAIL)
