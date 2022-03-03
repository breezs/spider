# 获取开放代理接口
import csv

import requests
import re
from fake_useragent import UserAgent
# 获取代理IP列表
def get_ip_list():
    url='http://api.89ip.cn/tqdl.html?api=1&num=60&port=&address=&isp='
    html=requests.get(url=url,headers={'User-Agent':UserAgent().random}).text
    #按<br>分组
    t_arr=html.split('<br>')
    # 第一个特殊，需要先按</script>\n分组
    t_0=t_arr[1].split('</script>\n')[1].strip
    ip_list=[]
    ip_list.append(t_0)
    # 第二个及后面直接遍历就行
    for i in range(2,len(t_arr)-1):
        ip_list.append(t_arr[i])
    print(ip_list)
    #测试所有的IP可用性
    for ip in ip_list:
        mtest_ip(ip)
def mtest_ip(ip):
    url='http://baidu.com/'
    headers={
        'User-Agent':UserAgent().random
    }
    proxies={
        'http': f'http://{ip}',
        'https': f'https://{ip}'
    }
    try:
        res=requests.get(url=url,proxies=proxies,headers=headers,timeout=8)
        print(res.status_code)
        #一般状态码返回200就说明可用
        if res.status_code==200:
            print(ip,'Sucess')
            L=[ip]
            with open('proxies2.csv', 'a', encoding='utf-8', newline='') as f:
                writer=csv.writer(f)
                writer.writerow(L)
    except Exception as e:
        print(ip,'Failed',e)

if __name__ == '__main__':
    get_ip_list()