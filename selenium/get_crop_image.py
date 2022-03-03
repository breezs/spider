from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
import time
url='https://tiku.ekgc.cn/testing/klogin'
driver=webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')
driver.get(url)
time.sleep(2)
#保存整个页面
driver.save_screenshot('index.png')
# 定位到验证码对象
xpath_dbs='//*[@id="kaptcha"]'
#定位节点的x,y坐标
localtion=driver.find_element(by=By.XPATH,value=xpath_dbs).location
#取验证码大小
size=driver.find_element(by=By.XPATH,value=xpath_dbs).size
#左上角坐标
print(size)
left_s_x=localtion['x']
left_s_y=localtion['y']
#右下角坐标
right_x_x=left_s_x+size['width']
right_x_y=left_s_y+size['height']

#截取验证码图片
img=Image.open('index.png').crop((left_s_x,left_s_y,right_x_x,right_x_y))
img.save('yzm.png')
driver.quit()