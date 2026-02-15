import pytest
import requests
import allure  # 新增：导入allure库


# 新增：类级别Allure注解（分类管理）
@allure.feature("IDRC赛事系统接口测试")
@allure.story("投票/俱乐部/地址接口")
class TestVote:
    # 新增：用例1 - 获取投票列表（标记优先级+步骤+附件）
    @allure.title("获取投票列表接口")
    @allure.severity(allure.severity_level.NORMAL)  # 普通优先级，对应报告normal柱
    @allure.description("测试获取投票列表接口，发起GET请求并打印响应信息")
    def test_voteapi(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "https://www.idrc.com/api/vote/list"  # 获取投票列表
            get_params = {
                "keyword": "",
                "order": "player_no",
                "page": "1", "limit": "20"
            }  # 获取请求参数
            # 新增：记录请求信息到Allure报告
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并打印响应"):
            response = requests.get(url, params=get_params)
            # 新增：记录响应信息到Allure报告
            allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            # 原有打印逻辑保留
            print("响应码:", response.status_code)
            print("响应体：", response.text)
            print("响应体（json）：", response.json())

    # 新增：用例2 - 新增俱乐部（标记优先级+步骤+附件）
    @allure.title("新增俱乐部接口")
    @allure.severity(allure.severity_level.CRITICAL)  # 核心功能，对应报告critical柱
    @allure.description("测试新增俱乐部接口，发起POST请求并打印响应信息")
    def test_新增俱乐部(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "https://www.idrc.com/index/club/save"
            get_params = {
                # 这些参数是错误的
                "name": "小花",  # 主体全称
                "type": "1",  # 主体类型 1-有限公司 2-民非机构 3-社会团体 4-个体工商户
                "license_no": "营业执照或登记证书编号",
                "license_file": "营业执照或登记证书图片",
                "country": "国家",
                "province": "省",
                "city": "city",
                "address": "address",
                "legal_person": "legal_person",
                "leader_phone": "leader_phone",
                "leader_name": "leader_name",
                "is_asfc": "1",
                "club_name": "club_name",
                "short_name": "short_name",
                "avatar": "avatar",
                "club_desc": "club_desc",
                "account": "account",
                "password": "123456",
                "confirm": "confirm",
                "club_member": "club_member"
            }
            # 新增：记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送POST请求并打印响应"):
            res1 = requests.post(url, params=get_params)
            # 新增：记录响应信息
            allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            # 原有打印逻辑保留
            print("请求状态：", res1.status_code)
            print("请求文本：", res1.text)
            print("请求json：", res1.json())

    # 新增：用例3 - 获取地址接口（标记优先级+步骤）
    @allure.title("获取地址接口（无打印）")
    @allure.severity(allure.severity_level.NORMAL)  # 普通优先级
    @allure.description("测试获取地址接口，发起GET请求（无打印输出）")
    def test_获取地址接口(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "https://www.idrc.com/index/player/area"
            get_params = {
                "parent_code": "1"
            }
            # 新增：记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求"):
            res2 = requests.get(url, params=get_params)
            # 新增：记录响应状态码（即使无打印）
            allure.attach(str(res2.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)

    # 新增：用例4 - 地址接口（带打印）（标记优先级+步骤+附件）
    @allure.title("获取地址接口（带打印）")
    @allure.severity(allure.severity_level.MINOR)  # 次要优先级，对应报告minor柱
    @allure.description("测试获取地址接口，发起GET请求并打印响应/COOKIES信息")
    def test_jiekou(self):
        with allure.step("步骤1：准备请求URL和参数"):
            url = "https://www.idrc.com/index/player/area"
            get_params = {
                "parent_code": "1",
            }
            # 新增：记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并打印响应"):
            res3 = requests.get(url, params=get_params)
            # 新增：记录响应信息（包括COOKIES）
            allure.attach(str(res3.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
            allure.attach(res3.text, name="响应内容", attachment_type=allure.attachment_type.JSON)
            allure.attach(str(res3.cookies), name="响应COOKIES", attachment_type=allure.attachment_type.TEXT)

            # 原有打印逻辑保留
            print(res3.text)
            print(res3.json())
            print(res3.cookies)


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