import sys

import requests
import pytest
import allure  # 新增：导入allure


@allure.feature("IDRC赛事系统接口测试")  # 新增：类级别feature
@allure.story("成绩/赛程/上传/验证码接口")  # 新增：类级别story
class TestGrade:
    # 新增：成绩排名用例Allure注解
    @allure.title("成绩排名接口")  # 用例标题
    @allure.severity(allure.severity_level.NORMAL)  # 优先级
    @allure.description("测试成绩排名接口，校验HTTP状态码为200")  # 用例描述
    def test_成绩排名(self):
        with allure.step("步骤1：准备请求URL和参数"):  # 新增：步骤注解
            url = "http://idrc.iflight-rc.com/api/grades/get_grades_list"
            params_data = {
                "race_id": "791",
                "search": "",
                "cid": "",
                "size": "10",
                "page": "1",
                "carnival_id": ""
            }
            # 新增：记录请求信息到Allure报告
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(params_data), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求并校验响应"):  # 新增：步骤注解
            res1 = requests.post(url, params=params_data)
            # 新增：记录响应状态码
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            assert res1.status_code == 200
            # 新增：记录响应内容
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
            print("响应文本：", res1.text)
            print("响应json", res1.json())

    # 新增：获取赛程列表用例Allure注解
    @allure.title("获取赛程列表接口")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试获取赛程列表接口，校验HTTP状态码为200")
    def test_获取赛程列表(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "http://idrc.iflight-rc.com/api/fixture/get_fixture"
            params_data = {
                "match_time": "2024-11-22",
                "carnival_id": ""
            }
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(params_data), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求并校验响应"):
            res1 = requests.post(url, params=params_data)
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            assert res1.status_code == 200
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
            print("响应文本：", res1.text)
            print("响应json", res1.json())

    # 新增：上传图片接口用例Allure注解
    @allure.title("上传图片接口")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试图片上传接口，上传指定JPG图片")
    def test_上传图片接口(self):
        with allure.step("步骤1：准备请求URL和上传文件"):
            url = "http://idrc.iflight-rc.com/api/ajax/upload"
            file_path = r"D:\Pictures\微信图片_20251017214318_93_82.jpg"
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(file_path, name="上传文件路径", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求上传图片"):
            with open(file_path, "rb") as f:
                post_data = {
                    "file": ("微信图片_20251017214318_93_82.jpg", f, "image/jpg"),
                    "category": ""
                }
                res1 = requests.post(url, files=post_data)
                allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
                print("json", res1.json())

    # 新增：手机验证码生成用例Allure注解
    @allure.title("手机验证码校验接口")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("测试手机验证码校验接口，使用指定手机号和验证码")
    def test_手机验证码生成(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "http://idrc.iflight-rc.com/api/smsgeet/checksms"
            sys.stdin = open('/dev/tty') if sys.platform != 'win32' else sys.stdin
            code = "888888"
            params_data = {
                "phone": "18819781752",
                "code": code
            }
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            # 新增：脱敏手机号后记录参数，保护敏感信息
            safe_params = {"phone": "1881978****", "code": code}
            allure.attach(str(safe_params), name="请求参数（脱敏）", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求校验验证码"):
            res1 = requests.post(url, params=params_data)
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
            print(res1.status_code)
            print(res1.text)
            print(res1.json())


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