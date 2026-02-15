import os
from time import sleep
import pytesseract
import openpyxl
import pytest
import selenium
from ddt import ddt, data, unpack
from PIL import Image
import pytesseract
from selenium.webdriver.common.by import By
import allure  # 新增：导入allure库

from excel_util import read_excel

pytesseract.pytesseract.tesseract_cmd = r'D:\tessera\tesseract.exe'

test_data = read_excel(r"C:\Users\Administrator\PycharmProjects\PythonProject\data\data.xlsx", sheet_name="Sheet1")


# 新增：类级别Allure注解（分类管理）
@allure.feature("后台系统登录自动化测试")
@allure.story("Excel数据驱动+验证码识别登录")
@pytest.mark.parametrize("data_json", test_data)
class TestExcel():
    # 新增：用例1 - 读取Excel数据（标记优先级+步骤+附件）
    @allure.title("读取Excel测试数据")
    @allure.severity(allure.severity_level.NORMAL)  # 普通优先级，对应报告normal柱
    @allure.description("测试读取Excel中的账号密码数据，打印并验证数据读取正常")
    def test_read_excel(self, data_json):
        with allure.step("步骤1：从Excel数据中提取账号和密码"):
            # 原有逻辑保留
            username = data_json.get("username")
            password = data_json.get("password")
            # 新增：记录读取到的数据（脱敏密码）到Allure报告
            safe_data = {"username": username, "password": "******"}
            allure.attach(str(safe_data), name="Excel读取的测试数据（脱敏）", attachment_type=allure.attachment_type.TEXT)

            # 原有打印逻辑保留
            print(f"测试账号{username},密码{password}")

    # 新增：用例2 - 后台登录（带验证码识别）（标记优先级+步骤+附件）
    @allure.title("后台登录-验证码识别自动填充")
    @allure.severity(allure.severity_level.CRITICAL)  # 核心登录流程，对应报告critical柱
    @allure.description("""
    ### 测试场景：
    1. 复用登录夹具的driver
    2. 读取Excel账号密码 → 输入账号密码 → 截图验证码并识别 → 填充验证码 → 点击登录
    ### 预期结果：
    验证码识别并填充，登录按钮点击成功
    """)
    def test_登陆后台存在验证码(self, test_login2, data_json):
        try:
            with allure.step("步骤1：获取driver并输入账号密码"):
                driver = test_login2
                # 原有账号输入逻辑保留
                username = driver.find_element(By.XPATH, '//*[@id="pd-form-username"]')
                username.clear()
                username.send_keys(data_json.get("username"))
                sleep(2)
                pwd = driver.find_element(By.XPATH, '//*[@id="pd-form-password"]')
                pwd.clear()
                pwd.send_keys(data_json.get("password"))
                sleep(2)
                # 新增：账号密码输入后截图
                allure.attach(driver.get_screenshot_as_png(), name="账号密码输入后截图",
                              attachment_type=allure.attachment_type.PNG)

            with allure.step("步骤2：截图验证码并识别文字"):
                # 原有验证码截图逻辑保留
                captcha_img = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/span/img')
                captcha_img.screenshot("./captcha.jpg")
                # 新增：将验证码图片附加到Allure报告
                allure.attach.file("./captcha.jpg", name="验证码截图", attachment_type=allure.attachment_type.IMAGE)

                # 原有验证码识别逻辑保留
                captcha_text = pytesseract.image_to_string(Image.open("captcha.jpg").convert("L")).strip()
                print(f"识别到的验证码: {captcha_text}")
                # 新增：记录识别到的验证码到报告
                allure.attach(captcha_text, name="识别到的验证码", attachment_type=allure.attachment_type.TEXT)

            with allure.step("步骤3：填充验证码并点击登录按钮"):
                # 原有验证码输入逻辑保留
                yzn_send = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/input')
                yzn_send.clear()
                yzn_send.send_keys(captcha_text)
                sleep(10)
                # 新增：验证码填充后截图
                allure.attach(driver.get_screenshot_as_png(), name="验证码填充后截图",
                              attachment_type=allure.attachment_type.PNG)

                # 原有登录按钮点击逻辑保留
                btn = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[6]/button')
                btn.click()
                sleep(10)
                # 新增：点击登录后截图
                allure.attach(driver.get_screenshot_as_png(), name="点击登录按钮后截图",
                              attachment_type=allure.attachment_type.PNG)

        # 新增：异常捕获，记录异常信息和截图
        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="登录异常截图",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="异常信息", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"后台登录操作失败：{str(e)}")

# （可选）pytest主函数（便于直接运行）
if __name__ == "__main__":
    # 执行用例并生成Allure报告（需安装allure-pytest：pip install allure-pytest）
    pytest.main([
        __file__,
        "-v",  # 详细输出
        "--alluredir=./allure-results",  # 报告输出目录
        "--clean-alluredir"  # 清空旧报告
    ])
    # 本地运行 python .\testcase\test_api\test_posts.py
    # allure serve ./allure-results