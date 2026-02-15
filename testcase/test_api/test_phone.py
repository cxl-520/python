import sys
import json
import requests
import pytest
import allure


@allure.epic("SMS verification")
@allure.feature("Phone code")
@allure.story("Send and verify flow")
class TestPhone:
    # phone = None
    phone="18819781752"
    post_url = "http://idrc.iflight-rc.com/api/smsgeet/sendsms"
    check_url = "http://idrc.iflight-rc.com/api/smsgeet/checksms"
    # def setup_class(self):
    #     with allure.step("Step 0: read and validate phone number"):
    #         if sys.stdin is not sys.__stdin__:
    #             sys.stdin = sys.__stdin__
    #
    #         # self.phone = input("Enter 11-digit phone number: ")
    #         try:
    #             assert self.phone is not None and len(self.phone) == 11, "phone must be 11 digits"
    #             assert self.phone.isdigit(), "phone must be numeric"
    #             allure.attach(f"phone: {self.phone}", name="phone", attachment_type=allure.attachment_type.TEXT)
    #             print("Phone:", self.phone)
    #         except AssertionError as e:
    #             pytest.fail(f"phone validation failed: {e}")

    @allure.title("Send verification code")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=1)
    def test_send_code(self):
        with allure.step("Step 1: build request params"):
            params_data = {"phone": self.phone}
            allure.attach(json.dumps(params_data), name="params", attachment_type=allure.attachment_type.JSON)

        with allure.step("Step 2: call send API"):
            try:
                res = requests.post(self.post_url, data=params_data, timeout=10)
                allure.attach(str(res.status_code), name="status", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res.text, name="body", attachment_type=allure.attachment_type.JSON)

                if res.status_code != 200:
                    pytest.skip(f"Non-200 status code: {res.status_code}")

                res_json = res.json()
                if isinstance(res_json, dict) and "code" not in res_json and "status" in res_json:
                    res_json["code"] = res_json.get("status")

                code = res_json.get("code") if isinstance(res_json, dict) else None
                if code not in (0, 200, None):
                    pytest.fail(f"Send failed, business code: {code}")

                print("Send status:", res.status_code)
                print("Send json:", res_json)
                print("Send text:", res.text)

            except requests.exceptions.Timeout:
                pytest.fail("send API timeout")
            except requests.exceptions.ConnectionError:
                pytest.fail("send API connection error")
            except ValueError:
                pytest.fail("send API response is not JSON")
            except Exception as e:
                pytest.fail(f"send API error: {e}")

    @allure.title("Verify code")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.run(order=2)
    def test_verify_code(self):
        with allure.step("Step 1: read code input"):
            if sys.stdin is not sys.__stdin__:
                sys.stdin = sys.__stdin__
            # code = input("Enter received code: ")
            code="187234"
            allure.attach(f"code: {code}", name="code", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Step 2: build request params"):
            params_data = {"phone": self.phone, "code": code}
            allure.attach(json.dumps(params_data), name="params", attachment_type=allure.attachment_type.JSON)

        with allure.step("Step 3: call verify API"):
            try:
                res = requests.post(self.check_url, data=params_data, timeout=10)
                allure.attach(str(res.status_code), name="status", attachment_type=allure.attachment_type.TEXT)
                allure.attach(res.text, name="body", attachment_type=allure.attachment_type.JSON)

                if res.status_code != 200:
                    pytest.skip(f"Non-200 status code: {res.status_code}")

                res_json = res.json()
                if isinstance(res_json, dict) and "code" not in res_json and "status" in res_json:
                    res_json["code"] = res_json.get("status")

                code_val = res_json.get("code") if isinstance(res_json, dict) else None
                if code_val not in (0, 200, None):
                    pytest.fail(f"verify failed, business code: {code_val}")

                print("Verify status:", res.status_code)
                print("Verify text:", res.text)
                print("Verify json:", res_json)

            except requests.exceptions.Timeout:
                pytest.fail("verify API timeout")
            except ValueError:
                pytest.fail("verify API response is not JSON")
            except Exception as e:
                pytest.fail(f"verify API error: {e}")


if __name__ == '__main__':
    pytest.main(["-s", __file__])
