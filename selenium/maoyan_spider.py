import time
from selenium.webdriver.common.by import By
from selenium import webdriver
class MaoYanSpider(object):
    def __init__(self):
        self.url='https://www.maoyan.com/'
        options=webdriver.EdgeOptions()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        self.driver=webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe',options=options)

    def go_to(self):
        # 进入榜单
        self.driver.get(url=self.url)
        self.driver.refresh()
        self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/ul/li[5]/a').click()
        time.sleep(3)
        self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/ul/li[5]/a').click()

    def parse_data(self):
        data_list=[]
        # time.sleep(10)
        #遍历每页
        for i in range(1,11):
            temp={}
            temp['title']=self.driver.find_element(by=By.XPATH,value='/html/body/div[4]/div/div/div[1]/dl/dd['+str(i)+']'+'/div/div/div[1]/p[1]/a').get_attribute('title').strip()
            temp['star']=self.driver.find_element(by=By.XPATH,value='/html/body/div[4]/div/div/div[1]/dl/dd['+str(i)+']'+'/div/div/div[1]/p[2]').text.strip()
            temp['time']=self.driver.find_element(by=By.XPATH,value='/html/body/div[4]/div/div/div[1]/dl/dd['+str(i)+']'+'/div/div/div[1]/p[3]').text[5:15].strip()
            data_list.append(temp)
        return  data_list

    def save_data(self,data_list):
        for data in data_list:
            print(data)

    def main(self):
        # 页数
        self.go_to()
        time.sleep(2)
        number=0
        while True:
            try:
                print('*'*50)
                number += 1
                print(f'第{number}页')
                data_list=self.parse_data()
                self.save_data(data_list)
                self.driver.execute_script('scrollTo(0,1000000)')
                el_text = self.driver.find_element(by=By.XPATH, value='//*[contains(text(),"下一页")]')
                el_text.click()
                # 找不到按钮就退出
                if  not el_text:
                    break
            except Exception as e:
                print(e)
                break
        self.driver.quit()
if __name__ == '__main__':
    spider=MaoYanSpider()
    spider.main()