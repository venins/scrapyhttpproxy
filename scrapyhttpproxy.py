import base64
from six.moves.urllib.request import getproxies, proxy_bypass
from six.moves.urllib.parse import unquote
try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy
from six.moves.urllib.parse import urlunparse

from scrapy.utils.httpobj import urlparse_cached
from scrapy.exceptions import NotConfigured


class ScrapyHttpProxyMiddleware(object):
    """
    This is custom scrapy http proxy middleware
    you can set custom proxy in the settings.

    to enable in settings.py set
    SCRAPY_HTTP_ENABLED = True
    SCRAPY_HTTP_PROXY = "proxy address"
    and add this in 
    DOWNLOADER_MIDDLEWARES

    
    """
    def __init__(self, scrapy_http_enabled, scrapy_http_proxy):
        self.scrapy_http_enabled = scrapy_http_enabled
        self.scrapy_http_proxy = scrapy_http_proxy
        if not self.scrapy_http_enabled:
            raise NotConfigured

    @classmethod
    def from_crawler(cls, crawler):
        scrapy_http_enabled = crawler.settings.getbool('SCRAPY_HTTP_ENABLED', default = False)
        scrapy_http_proxy = crawler.settings.get('SCRAPY_HTTP_PROXY', default = None)
        return cls(scrapy_http_enabled, scrapy_http_proxy)

    def process_request(self, request, spider):
        # ignore if proxy is already seted
        if 'proxy' in request.meta:
            print "not setting proxy ==>",request.meta["proxy"]
            return


        #set proxy for crawling
        request.meta['proxy'] = self.scrapy_http_proxy
        #print "it was not there i will setup==>>",request.meta["proxy"]