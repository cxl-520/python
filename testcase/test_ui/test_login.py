import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import allure
# 给整个测试类加全局Allure标记，所有用例继承这个模块/功能标识
@allure.feature("Web自动化测试")  # 大模块：Web自动化
@allure.story("Saucedemo平台登录功能")  # 子功能：登录功能
class TestLogin:
    #后面用公共夹具了
    # def setup_class(self):
    #     self.driver = webdriver.Chrome()
    #     self.driver.get("https://www.saucedemo.com/")
    #     self.driver.maximize_window()
    #     self.driver.implicitly_wait(10)
    # def setup_method(self):
    #     self.driver.refresh()
    # def teardown(self):
    #     self.driver.quit()
    #给每个用例加专属标题+优先级，参数化数据会自动显示在报告中
    @allure.title("正常账号密码登录-推出登录校验")#定义用例标题
    @allure.severity(allure.severity_level.CRITICAL)  #定义用例优先级
    # 核心：参数化装饰器
    # 参数名：username, password, expected_msg（账号、密码、预期错误提示）
    @pytest.mark.parametrize("username,password,expected_msg", [
        # ("standard_user", "secret_sauce", "https://www.saucedemo.com/")  # 移除多余单引号
        ("standard_user", "secret_sauce", "")
    ])
    def test_login_001(self,username,password,expected_msg,test_login1):
        # 登录正确账号
        driver=test_login1
        login_name=driver.find_element(By.XPATH,'//*[@id="user-name"]')
        login_name.send_keys(username)
        login_pwd=driver.find_element(By.XPATH,'//*[@id="password"]')
        login_pwd.send_keys(password)
        driver.find_element(By.XPATH,'//*[@id="login-button"]').click()
        driver.find_element(By.XPATH,'//*[@id="react-burger-menu-btn"]').click()
        sleep(5)
        driver.find_element(By.XPATH,'//*[@id="logout_sidebar_link"]').click()
        # 获取当前页面的url，做断言，判断是不是已经退出登录
        current_url=driver.current_url
        assert current_url==expected_msg

    @pytest.mark.parametrize("username,password,expected_msg", [
        ("ocked_out", "secret_sauce", "Epic sadface: Username and password do not match any user in this service")
        # 移除多余单引号
    ])
    @allure.title("错误账号-密码正确：校验错误提示")
    @allure.severity(allure.severity_level.NORMAL)  # 优先级：重要用例
    def test_login_002(self,username,password,expected_msg,test_login1):
        # 登录账号错误
        driver=test_login1
        login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        login_name.send_keys(username)
        login_pwd =driver.find_element(By.XPATH, '//*[@id="password"]')
        login_pwd.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        text=driver.find_element(By.XPATH,'//*[@id="login_button_container"]/div/form/div[3]/h3').text
        print(text)
        assert text ==expected_msg
    @pytest.mark.parametrize("username,password,expected_msg", [
        ("standard_user","123456","Epic sadface: Username and password do not match any user in this service")
        # 移除多余单引号
    ])

    @allure.title("正确账号-错误密码：校验错误提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_003(self,username,password,expected_msg,test_login1):
        # 登录密码错误
        driver=test_login1
        login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        login_name.clear()
        login_name.send_keys(username)
        login_pwd = driver.find_element(By.XPATH, '//*[@id="password"]')
        login_pwd.clear()
        login_pwd.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        text =driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3').text
        print(text)
        assert text == expected_msg

    @allure.title("账号为空-密码非空：校验必填提示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password,expected_msg", [
        ("", "123456", "Epic sadface: Username is required")
    ])
    def test_login_004(self,username,password,expected_msg,test_login1):
        # 账号为空
        driver=test_login1
        login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        login_name.clear()
        login_name.send_keys(username)
        login_pwd = driver.find_element(By.XPATH, '//*[@id="password"]')
        login_pwd.clear()
        login_pwd.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        text = driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3').text
        print(text)
        assert text == expected_msg

    @allure.title("账号非空-密码为空：校验必填提示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password,expected_msg", [
        ("standard_user","","Epic sadface: Password is required")
    ])
    def test_login_005(self,username,password,expected_msg,test_login1):
        # 密码为空
        driver=test_login1
        login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        login_name.clear()
        login_name.send_keys(username)
        login_pwd = driver.find_element(By.XPATH, '//*[@id="password"]')
        login_pwd.clear()
        login_pwd.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        text = driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3').text
        print(text)
        assert text == expected_msg
if  __name__ == "__main__":
    pytest.main('-s',"test_login.py")
    #生成结果命令1.pytest test_login.py -v --alluredir=testcase/allure-results
    #生成静态HTML报告 2.allure generate testcase\allure-results -o testcase\allure-report --clean
    #打开静态报告 3.allure open testcase/allure-report