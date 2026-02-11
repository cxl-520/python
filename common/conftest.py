# pytest核心配置：夹具、钩子函数（全局共享，关键文件）
# 浏览器驱动
import sys
import time

import allure
import requests
from selenium import webdriver
import pytest

from logs import logs
from setting import ENV

@pytest.fixture
def test_login2():
    driver = webdriver.Chrome()
    logs.debug("打开浏览器")
    logs.error("webdriver ready")
    driver.get(ENV.url2)
    driver.maximize_window()
    driver.implicitly_wait(10)
    print("浏览器已启动，驱动初始化完成")
    yield driver    # 返回驱动给用例，暂停函数执行（等待用例全部完成）,跟return差不多，但是这个有后置操作
    # 后置清理操作：关闭浏览器（所有用例执行完后，自动执行）
    driver.quit()
@pytest.fixture #每个用例都执行一遍浏览器打开跟关闭，
# @pytest.fixture(scope='class')  # 类级作用域，每个用例共用一个浏览器打开跟关闭
def test_login1():
    driver = webdriver.Chrome()
    logs.debug("打开浏览器")
    logs.error("webdriver ready")
    driver.get(ENV.url1)
    driver.maximize_window()
    driver.implicitly_wait(10)
    print("浏览器已启动，驱动初始化完成")
    yield driver    # 返回驱动给用例，暂停函数执行（等待用例全部完成）,跟return差不多，但是这个有后置操作
    # 后置清理操作：关闭浏览器（所有用例执行完后，自动执行）
    driver.quit()
# 2. 核心钩子函数：pytest用例失败时，自动截图并附加到Allure报告
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 获取用例执行结果
    outcome = yield
    rep = outcome.get_result()
    # 仅当用例执行（call阶段）失败时，执行截图逻辑
    if rep.when == "call" and rep.failed:
        # 尝试获取夹具中的driver对象（浏览器驱动）
        try:
            driver = item.funcargs["test_login1"]  # 和你的夹具名保持一致！
        except KeyError:
            driver = None

        # 截图并附加到Allure报告
        if driver:
            # 截图命名：用例名+时间戳，避免重复
            screenshot_name = f"失败截图_{item.name}_{int(time.time())}.png"
            # 执行截图（Selenium自带方法）
            screenshot = driver.get_screenshot_as_png()
            # 将截图附加到Allure报告，类型为PNG图片
            allure.attach(
                screenshot,
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )
        # 无论是否截图成功，都附加异常堆栈信息到报告
        allure.attach(
            str(sys.exc_info()),
            name="用例失败异常信息",
            attachment_type=allure.attachment_type.TEXT
        )