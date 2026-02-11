import requests
import allure
import json
import os
import pytest
@allure.feature("接口自动化测试post请求")
@allure.story("apifox文档上的idrc接口")
class Test_api:
    @allure.description("""
         ### 上传图片接口
        **测试场景**：上传合法图片文件
        **预期结果**：HTTP状态码200，业务码200，返回图片URL
        **前置条件**：无
        """)
    @allure.title("上传图片接口")
    @allure.severity(allure.severity_level.NORMAL)
    def test_上传图片接口(self):
        url = "http://idrc.iflight-rc.com/api/ajax/upload"
        file_path = r"D:\Pictures\微信图片_20251017214318_93_82.jpg"
        with open(file_path, "rb") as f:
            post_data = {
                # requests文件上传的元组规则,代码要给接口传递带后缀的文件名，要不然会导致接口无法识别 PNG 格式
                "file": ("微信图片_20251017214318_93_82.jpg", f, "image/jpg"),
                "category": ""
            }
            with allure.step("步骤2：发送GET请求并校验响应"):
                try:
                    res1 = requests.post(url=url, files=post_data, timeout=5)
                    # 打印响应详情（关键：看服务器返回的错误信息）
                    print(f"响应状态码：{res1.status_code}")
                    print(f"响应内容：{res1.json()}")
                    # 1. 校验HTTP状态码
                    assert res1.status_code == 200
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
