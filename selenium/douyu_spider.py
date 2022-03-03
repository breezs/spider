import time
from selenium.webdriver.common.by import By
from selenium import webdriver

#用控件实现无界面
# driver=webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')
# # driver.get('https://www.douyu.com/directory/all')
# # time.sleep(1)
# # xp_dbs='//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[2]/div[1]/span'
# # driver.find_element_by_xpath(xp_dbs)
class DouYuSpider(object):
    def __init__(self):
        self.url='https://www.douyu.com/directory/all'
        # self.opt=webdriver.EdgeOptions().add_argument('--headless')
        self.driver=webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')

    def parse_data(self):
        time.sleep(10)
        #取直播间的列表
        room_list=self.driver.find_elements_by_xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div')
        print(len(room_list))
        data_list=[]#存放所有数据的列表

        #遍历room_list抓取每个直播间的数据
        for r in room_list:
            temp={}
            temp['title']=r.find_element_by_xpath('./a/div[2]/div[1]/h3').text
            temp['type']=r.find_element_by_xpath('./a/div[2]/div[1]/span').text
            temp['owner']=r.find_element_by_xpath('./a/div[2]/div[2]/h2/div').text
            temp['num']=r.find_element_by_xpath('./a/div[2]/div[2]/span').text
            #这里有问题
            temp['image']=self.driver.find_element_by_xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a/div[1]/div[1]/picture/img').get_attribute('src')
            # temp['image'] = r.find_element_by_xpath('./a/div[1]/div[1]/picture/img').get_attribute('src')
            data_list.append(temp)
        return  data_list,len(room_list)

    def save_data(self,data_list):
        for data in data_list:
            print(data)

    def main(self):
        # 页数
        number=0
        self.driver.get(self.url)
        while True:
            data_list,num=self.parse_data()
            self.save_data(data_list)
            if num<120:
                break
            try:
                self.driver.execute_script('scrollTo(0,1000000)')
                # el_text=self.driver.find_element_by_xpath('//*[@id="listAll"]/section[2]/div[2]/div/ul/li[9]/span')
                #也可以这样写
                el_text=self.driver.find_element(by=By.XPATH,value='//*[contains(text(),"下一页")]')
                el_text.click()
                number+=1
                print(f'第{number}页')
            except Exception as e:
                print(e)
                break
        self.driver.quit()
if __name__ == '__main__':
    spider=DouYuSpider()
    spider.main()