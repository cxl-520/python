import pytest
import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import allure  # 新增：导入allure库


# 新增：类级别Allure注解（分类管理）
@allure.feature("电商平台UI自动化测试")
@allure.story("商品购买流程（登录-筛选-加购-结算取消）")
class TestBro:
    # 新增：用例级别Allure注解
    @allure.title("商品购买流程-登录后筛选商品并取消结算")
    @allure.severity(allure.severity_level.CRITICAL)  # UI核心流程，标记为CRITICAL（对应报告critical柱）
    @allure.description("""
    ### 测试场景：
    1. 复用登录夹具的driver
    2. 登录电商平台 → 按名称倒序筛选商品 → 加入购物车 → 进入结算页 → 取消结算
    ### 预期结果：
    所有页面操作正常执行，无元素定位失败
    """)
    def test_bro(self, test_login1):
        with allure.step("步骤1：获取登录夹具的driver并登录平台"):
            driver = test_login1  # 接下login返回的驱动，公共夹具
            # 原有登录操作保留
            login_name = driver.find_element(By.XPATH, '//*[@id="user-name"]')
            login_name.send_keys("standard_user")
            login_pwd = driver.find_element(By.XPATH, '//*[@id="password"]')
            login_pwd.send_keys("secret_sauce")
            driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
            # 新增：登录成功后截图，附加到Allure报告
            allure.attach(driver.get_screenshot_as_png(), name="登录成功截图",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("步骤2：按名称Z-A排序筛选商品"):
            # 原有下拉框操作保留
            Select(driver.find_element(By.XPATH, "//select[@class='product_sort_container']")).select_by_visible_text(
                "Name (Z to A)")
            sleep(10)
            # 新增：筛选后截图
            allure.attach(driver.get_screenshot_as_png(), name="商品排序后截图",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("步骤3：添加商品到购物车并进入购物车页面"):
            # 原有加购操作保留
            cart_btn = driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]')
            cart_btn.click()
            shop_cart_btn = driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a')
            shop_cart_btn.click()
            driver.execute_script("window.scrollBy(0,200);")  # 模拟浏览器滚动200个像素
            # 新增：购物车页面截图
            allure.attach(driver.get_screenshot_as_png(), name="购物车页面截图",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("步骤4：进入结算页并取消结算"):
            # 原有结算/取消操作保留
            driver.find_element(By.XPATH, '//*[@id="checkout"]').click()  # 点击checkout按钮
            driver.execute_script("window.scrollBy(0,200);")  # 模拟浏览器滚动200个像素
            driver.find_element(By.XPATH, '//*[@id="cancel"]').click()
            driver.execute_script("window.scrollBy(0,200);")
            driver.find_element(By.XPATH, '//*[@id="continue-shopping"]').click()
            # 新增：取消结算后截图
            allure.attach(driver.get_screenshot_as_png(), name="取消结算后截图",
                          attachment_type=allure.attachment_type.PNG)

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