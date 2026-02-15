import sys

import requests
import json
import pytest
import allure  # 新增：导入allure库


# 新增：类级别Allure注解（分类管理）
@allure.feature("IDRC赛事系统接口测试")
@allure.story("手机验证码发送&校验接口")
@allure.epic("IDRC赛事系统自动化测试")  # 可选：史诗级分类，便于大模块管理
class Test_phone():
    # 原有逻辑完全保留
    phone = "18819781752"
    post_url = "http://idrc.iflight-rc.com/api/smsgeet/sendsms"
    assert phone is not None and len(phone) == 11
    print("输出的11位手机号码为：", phone)

    # 新增：用例1的Allure注解（发送验证码）
    @allure.title("发送手机验证码接口")  # 用例标题
    @allure.severity(allure.severity_level.CRITICAL)  # 优先级：验证码接口为核心流程，设为CRITICAL
    @allure.description("测试手机验证码发送接口，向指定手机号发送验证码，校验HTTP状态码为200")  # 用例描述
    @pytest.mark.run(order=1)  # 原有执行顺序保留
    def test_发送手机验证码(self):
        with allure.step("步骤1：准备请求URL和手机号参数"):  # 新增：步骤注解
            # 原有逻辑保留
            phone = self.phone
            paeams_data = {"phone": phone}
            # 新增：记录请求信息到Allure报告（脱敏手机号）
            allure.attach(str(self.post_url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            safe_phone = phone[:-4] + "****"  # 脱敏手机号后4位
            allure.attach(f"phone: {safe_phone}", name="请求参数（脱敏）", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求并校验响应"):  # 新增：步骤注解
            try:
                # 原有请求逻辑保留
                res1 = requests.post(self.post_url, data=paeams_data, timeout=10)
                assert res1.status_code == 200

                # 新增：记录响应信息到Allure报告
                allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

                # 原有打印逻辑保留
                print("验证码发送成功：", res1.status_code)
                print("验证码发送成功后的json：", res1.json())
                print("验证码发送成功后的txt：", res1.text)
            except  Exception as e:
                # 新增：异常时记录信息到Allure报告
                allure.attach(str(e), name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"验证失败：{str(e)}")

    # 新增：用例2的Allure注解（校验验证码）
    @allure.title("校验手机验证码接口")  # 用例标题
    @allure.severity(allure.severity_level.CRITICAL)  # 优先级：核心流程
    @allure.description("测试手机验证码校验接口，使用指定验证码校验手机号，打印响应结果")  # 用例描述
    @pytest.mark.run(order=2)  # 原有执行顺序保留
    def test_手机验证码生成(self):
        with allure.step("步骤1：准备请求URL和校验参数"):  # 新增：步骤注解
            # 原有逻辑保留
            url = "http://idrc.iflight-rc.com/api/smsgeet/checksms"
            sys.stdin = open('/dev/tty') if sys.platform != 'win32' else sys.stdin
            code = "888888"
            params_data = {
                "phone": self.phone,
                "code": code
            }
            # 新增：记录请求信息（脱敏手机号）
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            safe_params = {"phone": self.phone[:-4] + "****", "code": code}
            allure.attach(str(safe_params), name="请求参数（脱敏）", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求并打印响应"):  # 新增：步骤注解
            # 原有请求逻辑保留
            res1 = requests.post(url, params=params_data, timeout=10)

            # 新增：记录响应信息到Allure报告
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            # 原有打印逻辑保留
            print("输入手机验证码生成后的状态码", res1.status_code)
            print("输入手机验证码生成后的文本", res1.text)
            print("输入手机验证码生成后的json", res1.json())
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

