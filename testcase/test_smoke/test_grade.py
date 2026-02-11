import sys

import requests
import pytest
class TestGrade:
    def test_成绩排名(self):
        url = "http://idrc.iflight-rc.com/api/grades/get_grades_list"
        params_data = {
            "race_id": "791",
            "search":"",
            "cid":"",
            "size":"10",
            "page":"1",
            "carnival_id":""
        }
        res1=requests.post(url,params=params_data)
        assert res1.status_code == 200
        print("响应文本：",res1.text)
        print("响应json",res1.json())

    def test_获取赛程列表(self):
        url = "http://idrc.iflight-rc.com/api/fixture/get_fixture"
        params_data = {
            "match_time": "2024-11-22",
            "carnival_id": ""
        }
        res1 = requests.post(url, params=params_data)
        assert res1.status_code == 200
        print("响应文本：", res1.text)
        print("响应json", res1.json())
    def test_上传图片接口(self):
        url = "http://idrc.iflight-rc.com/api/ajax/upload"
        file_path=r"D:\Pictures\微信图片_20251017214318_93_82.jpg"
        with open(file_path,"rb") as f:
            post_data = {
                #requests文件上传的元组规则,代码要给接口传递带后缀的文件名，要不然会导致接口无法识别 PNG 格式
                 "file": ("微信图片_20251017214318_93_82.jpg", f,"image/jpg"),
                 "category":""
            }
            res1 = requests.post(url, files=post_data)
        print("json", res1.json())
    def test_手机验证码生成(self):
        url = "http://idrc.iflight-rc.com/api/smsgeet/checksms"
        # 替换原废弃代码，新版pytest兼容写法：恢复标准输入，让input正常工作
        sys.stdin = open('/dev/tty') if sys.platform != 'win32' else sys.stdin
        code=input("请输入验证码：")
        params_data = {
            "phone":"18819781752",
            "code":code
        }
        res1 = requests.post(url, params=params_data)
        print(res1.status_code)
        print(res1.text)
        print(res1.json())
if __name__ == '__main__':
    pytest.main(["-s", __file__])