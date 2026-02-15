from cmath import exp
from time import sleep

from PIL import Image, ImageEnhance
import pytesseract
from exceptiongroup import catch
from selenium.webdriver.support import expected_conditions as EC  # 等待条件库
import pytest
import allure
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
pytesseract.pytesseract.tesseract_cmd = r'D:\tessera\tesseract.exe'


class TestShop:
    def test_shop(self,test_login3):
        # 初始化浏览器
        driver = test_login3
        # 获取登陆按钮元素，点击登陆按钮
        login=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[5]/div/div[1]/div[2]/a[1]')
        login.click()
        sleep(1)
        #跳转到登陆页面，切换登陆账号密码页面进行登陆
        login_tab=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/ul/li[1]/a')
        login_tab.click()
        #使用显式等待，等待元素可见，等待账号可见
        zh=WebDriverWait(driver,10,0.5).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/div[1]/input'))
        )
        #点击账号并输入18819781752
        zh.click()
        zh.send_keys("18819781752")

        #获取密码元素并输入密码
        pwd=WebDriverWait(driver,10,0.5).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/input'))
        )
        pwd.click()
        pwd.send_keys("123456")
        driver.execute_script("window.scrollBy(0,180);")
        #获取图像位置，并提取图像文字，识别到的
        captch_img=driver.find_element(By.XPATH,'//*[@id="form-verify-img"]')
        captch_img.screenshot("./captcha_shop.jpg")
        # ========== 以下是新增/修改的验证码识别逻辑 ==========
        # 1. 打开图片并做预处理（灰度+二值化+增强对比度）
        img = Image.open("./captcha_shop.jpg")
        img = img.convert("L")  # 转灰度图
        threshold = 110  # 二值化阈值，可根据实际验证码调整
        img = img.point(lambda x: 255 if x > threshold else 0)  # 二值化
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  # 增强对比度

        # 2. 配置Tesseract仅识别数字，指定模式
        config = r'-l eng --psm 8 -c tessedit_char_whitelist=0123456789'
        captcha_text = pytesseract.image_to_string(img, config=config).strip()
        # 以上是新增/修改的验证码识别逻辑
        sleep(5)
        print(f"识别到的验证码: {captcha_text}")
        #定位验证码输入框
        yzm_input=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/div[3]/input')
        #输入验证码
        yzm_input.send_keys(captcha_text)
        btn_click=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/form/div[4]/button')
        sleep(2)
        #点击按钮
        # 文字弹窗定位一下子就消失了，所有只定位地址
        # expectes_msg=driver.
        btn_click.click()
        sleep(10)
        current_url=driver.current_url
        assert current_url=="http://127.0.0.1:8000/"
        action=ActionChains(driver)
        leval1=WebDriverWait(driver,10,0.5).until(
            EC.element_to_be_clickable((By.XPATH,'//*[text()="数码办公"]'))
        )
        action.move_to_element(leval1).perform()
        leval2=WebDriverWait(driver,10,0.5).until(
            EC.element_to_be_clickable((By.XPATH,'//*[text()="蓝牙耳机"]'))
        )
        leval2.click()




