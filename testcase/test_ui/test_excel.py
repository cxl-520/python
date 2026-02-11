import os
from time import sleep
import pytesseract
import openpyxl
import pytest
import selenium
# from Demos.win32ts_logoff_disconnected import username
# from adodbapi.examples.xls_read import driver
from ddt import ddt,data,unpack
from PIL import Image
import pytesseract
from selenium.webdriver.common.by import By

from excel_util import read_excel
pytesseract.pytesseract.tesseract_cmd = r'D:\tessera\tesseract.exe'

test_data = read_excel(r"C:\Users\Administrator\PycharmProjects\PythonProject\data\data.xlsx", sheet_name="Sheet1")


@pytest.mark.parametrize("data_json", test_data)
class TestExcel():
    # @data(*test_data)
    def test_read_excel(self,data_json):
        # 接收字典数据
        username = data_json.get("username")
        password = data_json.get("password")
        print(f"测试账号{username},密码{password}")
    def test_登陆后台存在验证码(self,test_login2,data_json):
        driver=test_login2
        username=driver.find_element(By.XPATH,'//*[@id="pd-form-username"]')
        username.clear()
        username.send_keys(data_json.get("username"))
        sleep(2)
        pwd=driver.find_element(By.XPATH,'//*[@id="pd-form-password"]')
        pwd.clear()
        pwd.send_keys(data_json.get("password"))
        sleep(2)
        # 定位验证码图片元素并截图
        captcha_img=driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/span/img')
        captcha_img.screenshot("./captcha.jpg")
        # 3. 使用 Tesseract 识别图片中的文字
        # 预处理图片（二值化、去噪，提高识别率）
        # 极简版：打开图片→转灰度→直接识别（去掉手动二值化，用默认阈值）
        captcha_text = pytesseract.image_to_string(Image.open("captcha.jpg").convert("L")).strip()
        print(f"识别到的验证码: {captcha_text}")
        yzn_send=driver.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/input')
        yzn_send.clear()
        yzn_send.send_keys(captcha_text)
        sleep(10)
        btn=driver.find_element(By.XPATH,'//*[@id="login-form"]/div[6]/button')
        btn.click()
        sleep(10)


if __name__ == "__main__":
    # 运行测试用例
    pytest.main(["-v", __file__])