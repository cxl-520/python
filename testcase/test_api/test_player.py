from json import JSONDecodeError
from wsgiref import headers

import pytest
import requests
import allure
@allure.feature("接口自动化测试")
@allure.story("apifox文档上的idrc接口")
class Test_player():
    # 方式1：装饰器（支持Markdown语法，适合复杂描述）
    @allure.description("""
    ### 获取参赛战队详情列表
    **测试场景*获取列表数据*：
    **预期结果**：返回200正确
    **前置条件**：无
    """)
    @allure.title("获取参赛战队详情列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_获取参赛战队详情列表(self):
        with allure.step("步骤1：拼接路径，请求参数，请求token"):
            url = "http://iflight-idrc.com//api/teams/get_teams_player"
            headers = {
                "Content-Type": "application/json",
            }
            params = {
                "team_id": 665,
                "carnival_id": 767,
                "page": 1,
                "size": 10,
            }
            cookies = {
                "PHPSESSID": "kujvjl6pfvnaqg1hnamj0f84b8",
                "backend_language": "zh-cn",
                "frontend_language": "zh-cn",
                "token": "47f77b10-7bd2-4d34-be27-1a4ad7e1df6b",
                "uid": "1"
            }
        with allure.step("步骤2：发送get请求"):
            res1=requests.get(url=url,headers=headers,params=params,cookies=cookies)
            assert res1.status_code == 200
        print(res1.text)
        print(res1.json())

    @allure.title("成绩排名")
    @allure.severity(allure.severity_level.NORMAL)
    def test_成绩排名(self,base_url):
        url = f"{base_url}/grades/get_grades_list"
        params = {
            "race_id": 783,
            "cid":"",
            "page": 1,
        }
        response = requests.get(url, params=params)
        assert response.status_code == 200

    @allure.title("获取赛程类别")
    @allure.severity(allure.severity_level.NORMAL)
    def test_获取赛程类别(self,base_url):
        with allure.step("步骤1：拼接上url"):
            url=f"{base_url}/fixture/get_fixture"
            headers = {
                "Content-Type": "application/json",
            }
            get_params={
                "carnival_id":"",
                "match_time":""
            }
        with allure.step("发送请求"):
            try:
                res=requests.get(url=url,headers=headers,params=get_params,timeout=5)
                res.raise_for_status()
                res_json=res.json()
                assert res_json["msg"]=="获取成功"
            except requests.exceptions.Timeout as e:
                # 捕获：请求超时
                print(f"【异常】获取赛程列表接口请求超时：{e}")
                raise  # 重新抛出，让pytest标记用例失败
            except requests.exceptions.HTTPError as e:
                # 捕获：HTTP响应码非200（如404/500）
                print(f"【异常】HTTP响应错误：{e}，响应内容：{res.text}")
                raise
            except JSONDecodeError as e:
                # 捕获：响应不是JSON格式
                print(f"【异常】响应解析失败：{e}，响应内容：{res.text}")
                raise
            except KeyError as e:
                # 捕获：响应JSON缺少字段
                print(f"【异常】响应缺少字段：{e}，响应内容：{res_json}")
                raise
            except AssertionError as e:
                # 捕获：断言失败（业务异常）
                print(f"【异常】业务断言失败：{e}")
                raise
            except Exception as e:
                # 兜底：捕获所有未预期的异常（避免脚本崩溃）
                print(f"【异常】未知错误：{e}")
                raise
    @allure.title("获取人气选手")
    @allure.severity(allure.severity_level.NORMAL)
    def test_获取人气选手(self,base_url):
        with allure.step("拼接url："):
            url=f"{base_url}/participants/get_hotplayer"
            params = {
                "search":"",
                "page":1,
                "size":10,
                "order":"votes"
            }
        with allure.step("填参数，发送请求；"):
            res1=requests.get(url=url,params=params,timeout=5)
            assert res1.status_code == 200
            try:
                res_json = res1.json()
                # 业务断言示例（根据实际接口返回调整）
                assert res_json.get("code") == 200, f"业务码异常：{res_json}"
                assert "data" in res_json, "响应缺少data字段"
            except Exception as e:
                raise Exception(f"响应解析失败或业务断言失败：{e}，响应内容：{res1.text}")

            except requests.exceptions.Timeout:
                allure.attach("请求超时（5秒内未响应）", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取人气选手接口请求超时")
            except requests.exceptions.ConnectionError:
                allure.attach("网络连接失败", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取人气选手接口网络连接失败")
            except AssertionError as e:
                allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                raise  # 重新抛出，标记用例失败
            except Exception as e:
                allure.attach(f"未知异常：{str(e)}", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取人气选手接口测试失败：{e}")


