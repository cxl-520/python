import sys

import requests
import json
import pytest
class Test_phone():
    phone = input("请输入11位的手机号码")
    post_url="http://idrc.iflight-rc.com/api/smsgeet/sendsms"
    assert phone is not None and len(phone) == 11
    print("输出的11位手机号码为：", phone)

    # 先执行发送验证码
    @pytest.mark.run(order=1)
    def test_发送手机验证码(self):
        #验证发送手机验证码的环节：
        phone=self.phone
        paeams_data = {"phone": phone}
        try:
            res1 = requests.post(self.post_url, data=paeams_data,timeout=10)
            assert res1.status_code == 200
            print("验证码发送成功：",res1.status_code)
            print("验证码发送成功后的json：",res1.json())
            print("验证码发送成功后的txt：",res1.text)
            # assert res1.status_code != 200
            # print("如果失败，打印验证码发送失败：",res1.status_code)
        except  Exception as e:
            pytest.fail(f"验证失败：{str(e)}")

    @pytest.mark.run(order=2)
    def test_手机验证码生成(self):
        url = "http://idrc.iflight-rc.com/api/smsgeet/checksms"
        # 替换原废弃代码，新版pytest兼容写法：恢复标准输入，让input正常工作
        sys.stdin = open('/dev/tty') if sys.platform != 'win32' else sys.stdin
        code = input("请输入验证码：")
        params_data = {
            "phone": self.phone,
            "code": code
        }
        res1 = requests.post(url, params=params_data,timeout=10)
        print("输入手机验证码生成后的状态码",res1.status_code)
        print("输入手机验证码生成后的文本",res1.text)
        print("输入手机验证码生成后的json",res1.json())


if __name__ == '__main__':
    pytest.main(["-s", __file__])
