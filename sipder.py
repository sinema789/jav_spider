import requests
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from utils.log_config import Log
from utils.settings import USER_AGENT, URL, MAX_WORKERS, MAX_PAGE
from pprint import pprint

# 日志配置
log = Log()


class JavBusSpider(object):
    """javbus爬虫"""

    def __init__(self):
        self.headers = {"user-agent": USER_AGENT}
        self.base_url = URL + 'page/{}'
        self.executor_1 = ThreadPoolExecutor(MAX_WORKERS)
        self.executor_2 = ThreadPoolExecutor(MAX_WORKERS)

    def get_detail_urls(self, url):
        """获取电影详情页面"""
        # 解析网页
        response = requests.get(url, headers=self.headers)
        # 获取电影详情页面a链接
        eroot = etree.HTML(response.text)
        detail_urls = eroot.xpath('//a[@class="movie-box"]/@href')
        if not detail_urls:
            log.warning('解析路径错误:详情链接为%s' % detail_urls)

        return detail_urls

    def threadpool_to_get_detail_urls(self):
        # 电影详情链接列表
        detail_urls = []
        # 创建线程池

        with self.executor_1 as pool:
            results = list(pool.map(self.get_detail_urls, [self.base_url.format(i) for i in range(1, MAX_PAGE + 1)]))

        for result in results:
            for detail_url in result:
                detail_urls.append(detail_url)

        if not detail_urls:
            log.warning("详情链接为空")

        return detail_urls

    def parse_detail(self, url):
        """解析详情页"""
        # 电影详情字典
        info_dict = {}
        response = requests.get(url, headers=self.headers)
        eroot = etree.HTML(response.text)

        # 标题
        title = eroot.xpath('//h3/text()')[0]
        # 番号
        code = eroot.xpath('//div[@class="col-md-3 info"]/p[1]/span[2]/text()')[0]
        # 时长
        length = eroot.xpath('//div[@class="col-md-3 info"]/p[3]/text()')[0]
        # 制作商
        producter = eroot.xpath(
            '//div[@class="col-md-3 info"]/p/span[text()="製作商:"]/following-sibling::*[1]/text()')[0]
        # 封面链接
        pic_url = eroot.xpath('//a[@class="bigImage"]/img/@src')[0]
        # 出版日期
        pub_date = eroot.xpath('//div[@class="col-md-3 info"]/p[2]/text()')[0]
        # 类别
        category = eroot.xpath(
            '//div[@class="col-md-3 info"]/p[text()="類別:"]/following-sibling::*[1]/span/a/text()')
        category = ','.join(category)
        # 演员
        actress = eroot.xpath('//p[@class="star-show"]/following-sibling::*[2]/span/a/text()')
        actress = ','.join(actress)
        if actress == '':
            actress = '暂无演员信息'

        info_dict['title'] = title
        info_dict['code'] = code
        info_dict['length'] = length
        info_dict['producter'] = producter
        info_dict['pic_url'] = pic_url
        info_dict['pub_date'] = pub_date
        info_dict['category'] = category
        info_dict['actress'] = actress

        return info_dict

    def threadpool_to_parse_detail(self, url_list):
        a_list = []
        # 创建线程池
        with self.executor_2 as pool:
            results = list(pool.map(self.parse_detail, url_list))
        for result in results:
            a_list.append(result)

        return a_list

    def main(self):
        log.info("文件信息-" + os.path.basename(__file__))
        try:
            urls_list = self.threadpool_to_get_detail_urls()
            pprint(urls_list)

            a_list = self.threadpool_to_parse_detail(urls_list)
            pprint(a_list)
            return a_list
        except Exception as e:
            print(e)
            log.error("获取信息出错")


if __name__ == '__main__':
    spider = JavBusSpider()
    spider.main()