from pkgutil import get_data
from tokenize import cookie_re

import requests
import pytest
import allure  # 新增：导入allure库


# 新增：类级别Allure注解（分类管理）
@allure.feature("IDRC赛事系统接口测试")
@allure.story("参赛战队详情接口")
class Test_idrcspi():
    # 新增：用例级别Allure注解
    @allure.title("获取参赛战队详情列表接口")  # 用例标题（报告中展示）
    @allure.severity(allure.severity_level.NORMAL)  # 用例优先级
    @allure.description("测试获取参赛战队详情列表接口，携带指定cookies和参数发起GET请求")  # 用例描述
    def test_获取参赛战队详情列表(self):
        with allure.step("步骤1：准备请求URL、参数、Cookies"):  # 新增：步骤注解
            url = "http://idrc.iflight-rc.com/api/teams/get_teams_player"
            get_params = {
                "team_id": "870",
                "carnival_id": "767",
                "page": "1",
                "size": "10"
            }
            json_data = {
                "team_id": "870",
                "carnival_id": "767",
                "page": "1",
                "size": "10"
            }
            cookie_re = {
                "PHPSESSID": "kujvjl6pfvnaqg1hnamj0f84b8",
                "backend_language": "zh-cn",
                "frontend_language": "zh-cn",
                "token": "47f77b10-7bd2-4d34-be27-1a4ad7e1df6b",
                "uid": "1"
            }
            # 新增：记录关键请求信息到Allure报告（脱敏敏感字段）
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            # 脱敏token/PHPSESSID后记录Cookies，保护敏感信息
            safe_cookies = {
                "PHPSESSID": "***",
                "backend_language": "zh-cn",
                "frontend_language": "zh-cn",
                "token": "***",
                "uid": "1"
            }
            allure.attach(str(safe_cookies), name="请求Cookies（脱敏）", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并打印响应"):  # 新增：步骤注解
            res1 = requests.get(url, params=get_params, cookies=cookie_re)
            # 新增：记录响应状态码和内容到Allure报告
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            # 原有打印逻辑完全保留
            print("请求状态：", res1.status_code)
            print("请求文本：", res1.text)
            print("请求json：", res1.json())

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