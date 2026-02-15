from json import JSONDecodeError
import pytest
import requests
import allure


# 类级别Allure注解（全局生效）
@allure.feature("接口自动化测试")
@allure.story("apifox文档上的idrc接口")
@allure.epic("IDRC赛事系统接口测试")  # 史诗级分类
@allure.tag("IDRC", "赛事接口", "GET请求")  # 标签（便于筛选）
@allure.link("https://apifox.com/apidoc/project/xxx", name="Apifox接口文档")  # 关联接口文档
@allure.issue("JIRA-1234", name="Known issue: Code expiration time")  # 关联缺陷
class Test_player():
    """IDRC赛事系统接口测试类"""

    # ====================== 用例1：获取参赛战队详情列表 ======================
    @allure.description("""
    ### 获取参赛战队详情列表接口测试
    **测试场景**：调用/get_teams_player接口获取指定战队的参赛选手详情列表
    **预期结果**：
    1. HTTP响应状态码为200
    2. 响应返回正确的战队选手数据
    **前置条件**：
    - 需携带有效的PHPSESSID和token
    - team_id=870和carnival_id=767为有效参数
    """)  # 详细描述（支持Markdown）
    @allure.title("获取参赛战队详情列表")  # 用例标题
    @allure.severity(allure.severity_level.NORMAL)  # 用例优先级
    @allure.testcase("TC-IDRC-001", name="测试用例编号：TC-IDRC-001")  # 测试用例编号
    def test_获取参赛战队详情列表(self, base_url):
        with allure.step("步骤1：准备请求参数、Headers、Cookies"):
            url = f"{base_url}/teams/get_teams_player"
            headers = {"Content-Type": "application/json"}
            params = {"team_id": 870, "carnival_id": 767, "page": 1, "size": 10}
            cookies = {
                "PHPSESSID": "kujvjl6pfvnaqg1hnamj0f84b8",
                "backend_language": "zh-cn",
                "frontend_language": "zh-cn",
                "token": "47f77b10-7bd2-4d34-be27-1a4ad7e1df6b",
                "uid": "1"
            }
            # 记录请求信息到Allure报告
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(params), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(cookies), name="请求Cookies", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并验证响应"):
            try:
                res1 = requests.get(url=url, headers=headers, params=params, cookies=cookies, timeout=10)
                # 断言HTTP状态码
                assert res1.status_code == 200, f"HTTP状态码异常：预期200，实际{res1.status_code}"

                # 记录响应信息到Allure报告
                allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

                # 打印响应（便于控制台调试）
                print(res1.text)
                print(res1.json())

            except requests.exceptions.Timeout:
                allure.attach("请求超时（10秒内未响应）", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取参赛战队详情列表接口请求超时")
            except requests.exceptions.ConnectionError:
                allure.attach("网络连接失败/域名解析失败", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取参赛战队详情列表接口网络连接失败")
            except AssertionError as e:
                allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                raise  # 重新抛出，标记用例失败
            except Exception as e:
                allure.attach(f"未知异常：{str(e)}", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取参赛战队详情列表接口测试失败：{e}")

    # ====================== 用例2：成绩排名 ======================
    @allure.description("""
    ### 成绩排名接口测试
    **测试场景**：调用/grades/get_grades_list接口获取指定赛事的成绩排名列表
    **预期结果**：
    1. HTTP响应状态码为200
    2. 响应返回正确的成绩排名数据
    **前置条件**：race_id=783为有效赛事ID
    """)
    @allure.title("成绩排名")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-IDRC-002", name="测试用例编号：TC-IDRC-002")
    def test_成绩排名(self, base_url):
        with allure.step("步骤1：准备请求URL和参数"):
            url = f"{base_url}/grades/get_grades_list"
            params = {"race_id": 783, "cid": "", "page": 1}
            # 记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并验证响应状态码"):
            try:
                response = requests.get(url, params=params, timeout=10)
                assert response.status_code == 200, f"HTTP状态码异常：预期200，实际{response.status_code}"

                # 记录响应信息
                allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(response.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            except requests.exceptions.Timeout:
                allure.attach("请求超时（10秒内未响应）", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("成绩排名接口请求超时")
            except requests.exceptions.ConnectionError:
                allure.attach("网络连接失败", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("成绩排名接口网络连接失败")
            except AssertionError as e:
                allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                raise
            except Exception as e:
                allure.attach(f"未知异常：{str(e)}", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"成绩排名接口测试失败：{e}")

    # ====================== 用例3：获取赛程类别 ======================
    @allure.description("""
    ### 获取赛程类别接口测试
    **测试场景**：调用/fixture/get_fixture接口获取赛程类别列表
    **预期结果**：
    1. HTTP响应状态码为200
    2. 响应msg字段为"获取成功"
    3. 响应包含有效的赛程类别数据
    **前置条件**：无（carnival_id和match_time为空时返回全量数据）
    """)
    @allure.title("获取赛程类别")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-IDRC-003", name="测试用例编号：TC-IDRC-003")
    def test_获取赛程类别(self, base_url):
        with allure.step("步骤1：准备请求URL、Headers和参数"):
            url = f"{base_url}/fixture/get_fixture"
            headers = {"Content-Type": "application/json"}
            get_params = {"carnival_id": "", "match_time": ""}
            # 记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(headers), name="请求Headers", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(get_params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并验证业务逻辑"):
            try:
                res = requests.get(url=url, headers=headers, params=get_params, timeout=5)
                res.raise_for_status()  # 触发HTTPError（非200状态码）
                res_json = res.json()

                # 业务断言
                assert res_json["msg"] == "获取成功", f"业务提示异常：预期'获取成功'，实际{res_json.get('msg')}"

                # 记录响应信息
                allure.attach(str(res.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

            except requests.exceptions.Timeout as e:
                allure.attach(f"请求超时（5秒内未响应）：{str(e)}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取赛程类别接口请求超时")
            except requests.exceptions.HTTPError as e:
                allure.attach(f"HTTP响应错误：{str(e)}，响应内容：{res.text}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取赛程类别接口HTTP错误：{e}")
            except JSONDecodeError as e:
                allure.attach(f"响应解析失败：{str(e)}，响应内容：{res.text}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取赛程类别接口响应解析失败：{e}")
            except KeyError as e:
                allure.attach(f"响应缺少字段：{str(e)}，响应内容：{res_json}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取赛程类别接口响应缺少字段：{e}")
            except AssertionError as e:
                allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                raise
            except Exception as e:
                allure.attach(f"未知异常：{str(e)}", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取赛程类别接口测试失败：{e}")

    # ====================== 用例4：获取人气选手 ======================
    @allure.description("""
    ### 获取人气选手接口测试
    **测试场景**：调用/participants/get_hotplayer接口按投票数排序获取人气选手列表
    **预期结果**：
    1. HTTP响应状态码为200
    2. 业务码code=0、msg="获取成功"
    3. 响应包含data字段且为列表类型
    **前置条件**：无（search为空时返回全量选手）
    """)
    @allure.title("获取人气选手")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-IDRC-004", name="测试用例编号：TC-IDRC-004")
    def test_获取人气选手(self, base_url):
        with allure.step("步骤1：准备请求URL和参数"):
            url = f"{base_url}/participants/get_hotplayer"
            params = {"search": "", "page": 1, "size": 10, "order": "votes"}
            # 记录请求信息
            allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(params), name="请求参数", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤2：发送GET请求并验证业务逻辑"):
            try:
                res1 = requests.get(url=url, params=params, timeout=5)
                # 断言HTTP状态码
                assert res1.status_code == 200, f"HTTP状态码异常：预期200，实际{res1.status_code}"

                # 解析响应并记录
                res_json = res1.json()
                allure.attach(str(res1.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

                # 业务断言（核心：code=0为成功）
                assert res_json.get("code") == 0, f"业务码异常：预期0，实际{res_json.get('code')}，响应内容：{res_json}"
                assert "data" in res_json, "响应缺少data字段"
                assert isinstance(res_json.get("data"), list), "data字段不是列表类型"  # 额外校验数据类型

            # 异常捕获顺序：先具体异常 → 后通用异常（关键修复）
            except requests.exceptions.Timeout:
                allure.attach("请求超时（5秒内未响应）", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取人气选手接口请求超时")
            except requests.exceptions.ConnectionError:
                allure.attach("网络连接失败", name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail("获取人气选手接口网络连接失败")
            except AssertionError as e:
                allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                raise  # 保留原始断言错误
            except JSONDecodeError as e:
                allure.attach(f"响应解析失败：{str(e)}，响应内容：{res1.text}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取人气选手接口响应解析失败：{e}")
            except Exception as e:
                allure.attach(f"未知异常：{str(e)}，响应内容：{res1.text if 'res1' in locals() else '无响应'}",
                              name="异常信息", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"获取人气选手接口测试失败：{e}")


# （可选）pytest主函数（便于直接运行）
if __name__ == "__main__":
    # 执行所有用例并生成Allure报告（需提前安装allure-pytest）
    pytest.main([
        __file__,
        "-v",  # 详细输出
        "--alluredir=./allure-results",  # 报告输出目录
        "--clean-alluredir"  # 清空旧报告
    ])