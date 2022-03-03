import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
#创建驱动对象
#注册环境变量的
# driver=webdriver.Edge()
#没有注册的executable_path中放驱动所在的路径
driver=webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')
driver.get('http://baidu.com')
WebDriverWait(driver,20,0.5).until(
    ec.presence_of_element_located((By.LINK_TEXT,'hao123'))
)
print(driver.find_element_by_link_text('hao123').get_attribute('href'))
driver.quit()