import pytest
import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
class TestBro():
    def test_bro(self,test_login1):
        driver=test_login1  #接下login返回的驱动，公共夹具
        # 核心：参数化装饰器
        login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        login_name.send_keys("standard_user")
        login_pwd = driver.find_element(By.XPATH, '//*[@id="password"]')
        login_pwd.send_keys("secret_sauce")
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        # select=self.driver.find_element(By.XPATH,'//*[@id="header_container"]/div[2]/div/span/select').click()
        # select.click()
        # 直接定位select下拉框，选择Name (A to Z)
        Select(driver.find_element(By.XPATH, "//select[@class='product_sort_container']")).select_by_visible_text(
            "Name (Z to A)")
        # self.driver.execute_script("window.scrollBy(0,200);")  #模拟浏览器滚动200个像素
        sleep(10)
        cart_btn = driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]')
        cart_btn.click()
        shop_cart_btn = driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a')
        shop_cart_btn.click()
        driver.execute_script("window.scrollBy(0,200);")  # 模拟浏览器滚动200个像素
        driver.find_element(By.XPATH, '//*[@id="checkout"]').click()  # 点击checkout按钮
        driver.execute_script("window.scrollBy(0,200);")  # 模拟浏览器滚动200个像素
        driver.find_element(By.XPATH, '//*[@id="cancel"]').click()
        driver.execute_script("window.scrollBy(0,200);")
        driver.find_element(By.XPATH, '//*[@id="continue-shopping"]').click()