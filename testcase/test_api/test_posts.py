import requests
import allure
import json
import os
import pytest


# 类级别Allure注解（统一分类）
@allure.feature("接口自动化测试post请求")
@allure.story("apifox文档上的idrc接口")
@allure.epic("IDRC赛事系统接口测试")  # 补充史诗级分类
@allure.tag("IDRC", "上传接口", "POST请求", "图片上传")  # 补充标签（便于筛选）
@allure.link("https://apifox.com/apidoc/project/xxx", name="Apifox接口文档-图片上传")  # 关联接口文档
class Test_api:
    """IDRC赛事系统POST接口测试类（图片上传）"""

    @allure.description("""
    ### 图片上传接口测试
    **测试场景**：调用/ajax/upload接口上传合法JPG格式图片
    **预期结果**：
    1. HTTP响应状态码为200
    2. 业务码为成功状态（如code=0/200，根据实际接口调整）
    3. 响应返回图片URL（如url/file_path字段）
    **前置条件**：
    - 测试图片文件存在且为JPG格式
    - 文件路径正确可访问
    """)  # 详细描述（结构化）
    @allure.title("上传图片接口")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-IDRC-005", name="测试用例编号：TC-IDRC-005")  # 补充用例编号
    def test_上传图片接口(self):
        # 1. 准备请求基础信息
        url = "http://idrc.iflight-rc.com/api/ajax/upload"
        file_path = r"D:\Pictures\微信图片_20251017214318_93_82.jpg"

        with allure.step("步骤1：校验文件存在性并准备上传参数"):
            # 先校验文件是否存在（提前规避文件不存在异常）
            assert os.path.exists(file_path), f"测试图片不存在：{file_path}"
            allure.attach(f"文件路径：{file_path}", name="测试图片路径", attachment_type=allure.attachment_type.TEXT)

            # 打开文件并构造上传参数（指定文件名+MIME类型，确保接口识别格式）
            with open(file_path, "rb") as f:
                post_data = {
                    "file": ("微信图片_20251017214318_93_82.jpg", f, "image/jpeg"),  # 注意：JPG的MIME类型是image/jpeg
                    "category": ""
                }
                # 记录请求参数到Allure报告
                allure.attach(str(url), name="请求URL", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(post_data.keys()), name="上传参数Key", attachment_type=allure.attachment_type.TEXT)
                allure.attach("image/jpeg", name="文件MIME类型", attachment_type=allure.attachment_type.TEXT)

                with allure.step("步骤2：发送POST请求并校验响应"):
                    try:
                        # 发送POST请求（文件上传用files参数）
                        res1 = requests.post(url=url, files=post_data, timeout=10)

                        # 记录响应基础信息
                        allure.attach(str(res1.status_code), name="响应状态码",
                                      attachment_type=allure.attachment_type.TEXT)
                        allure.attach(res1.text, name="响应内容", attachment_type=allure.attachment_type.JSON)

                        # 打印响应（便于控制台调试）
                        print(f"响应状态码：{res1.status_code}")
                        print(f"响应内容：{res1.text}")  # 先打印文本，避免JSON解析失败报错

                        # 1. 校验HTTP状态码
                        assert res1.status_code == 200, f"HTTP状态码异常：预期200，实际{res1.status_code}"

                        # 2. 解析JSON响应（补充JSON解析异常捕获）
                        res_json = res1.json()

                        # 3. 业务断言（根据实际接口返回调整，以下为通用示例）
                        # 示例1：如果接口返回code=0表示成功
                        assert res_json.get("code") in [0, 200], f"业务码异常：{res_json}"
                        # 示例2：校验是否返回图片URL（根据实际字段名调整，如url/file_path等）
                        assert "url" in res_json or "file_path" in res_json, "响应缺少图片URL字段"
                        # 示例3：校验返回信息为成功
                        assert res_json.get("msg") in ["上传成功", "获取成功"], f"业务提示异常：{res_json.get('msg')}"

                    # 异常捕获：先具体 → 后通用（修正文案+补充场景）
                    except FileNotFoundError as e:
                        allure.attach(f"文件不存在：{str(e)}", name="异常信息",
                                      attachment_type=allure.attachment_type.TEXT)
                        pytest.fail(f"上传图片接口：测试图片文件不存在 - {e}")
                    except requests.exceptions.Timeout:
                        allure.attach("请求超时（10秒内未响应）", name="异常信息",
                                      attachment_type=allure.attachment_type.TEXT)
                        pytest.fail("上传图片接口请求超时")
                    except requests.exceptions.ConnectionError:
                        allure.attach("网络连接失败/域名解析失败", name="异常信息",
                                      attachment_type=allure.attachment_type.TEXT)
                        pytest.fail("上传图片接口网络连接失败")
                    except json.JSONDecodeError:
                        allure.attach(f"响应JSON解析失败，原始响应：{res1.text}", name="异常信息",
                                      attachment_type=allure.attachment_type.TEXT)
                        pytest.fail("上传图片接口响应不是合法JSON格式")
                    except AssertionError as e:
                        allure.attach(str(e), name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
                        raise  # 保留原始断言错误，便于定位
                    except Exception as e:
                        allure.attach(f"未知异常：{str(e)}，响应内容：{res1.text if 'res1' in locals() else '无响应'}",
                                      name="异常信息", attachment_type=allure.attachment_type.TEXT)
                        pytest.fail(f"上传图片接口测试失败：{e}")


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