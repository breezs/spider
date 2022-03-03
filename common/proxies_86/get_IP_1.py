import csv
import time, random
import requests
from fake_useragent import UserAgent
from lxml import etree


class GetProxyIP(object):
    # 初始化URL
    def __init__(self):
        self.url = 'https://www.89ip.cn/index_{}.html'

    # 获取代理IP
    def get_IP(self, url):
        html = requests.get(
            url=url,
            headers={
                'User-Agent': UserAgent().random
            },
            timeout=5
        ).text
        # 转换为xpath可解析格式
        parse_html = etree.HTML(html)
        # 解析得到所有tr列表
        tr_list = parse_html.xpath('//tr')
        # 遍历每个tr，获取每个tr中的IP
        for tr in tr_list[1:]:
            ip = tr.xpath('.//td[1]/text()')[0].strip()
            port = tr.xpath('./td[2]/text()')[0].strip()
            # 测试IP可用性
            self.mtest_ip(ip, port)

    def mtest_ip(self, ip, port):
        url = 'http://httpbin.org/get'
        # 设置headers
        headers = {
            'User-Agent': UserAgent().random
        }
        # 设置proxies代理参数
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'https://{ip}:{port}'
        }
        try:
            # 发起请求
            res = requests.get(url=url, proxies=proxies, headers=headers, timeout=8)
            print(res.status_code)
            # 得到状态码就说明IP可用
            if res.status_code:
                print(ip, port, 'Sucess')
                # 存到列表中
                L = [ip + ':' + port]
                # 写到csv中
                with open('proxies.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(L)
        # IP不可用则抛出异常
        except Exception as e:
            print(ip, port, 'Failed', e)

    # 运行方法
    def main(self):
        # 爬取1000页
        for i in range(1, 1001):
            url = self.url.format(i)
            # 解析得到IP
            self.get_IP(url)
            time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    spider = GetProxyIP()
    spider.main()