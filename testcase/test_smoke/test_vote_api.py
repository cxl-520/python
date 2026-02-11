import pytest
import requests
class TestVote:
    def test_voteapi(self):
        url = "https://www.idrc.com/api/vote/list"#获取投票列表
        get_params = {
            "keyword": "",
            "order": "player_no",
            "page": "1", "limit": "20"
        }  # 获取请求参数
        response = requests.get(url, params=get_params)
        # post的要上传表单参数
        # json_data = {"username": "test", "password": "123456", "gender": "男"}
        # response = request_demo.post(url, data=form_data)  # data参数传表单数据
        print("响应码:", response.status_code)
        print("响应体：", response.text)
        print("响应体（json）：", response.json())
    def test_新增俱乐部(self):
        url="https://www.idrc.com/index/club/save"
        get_params={
            #这些参数是错误的
            "name":"小花",# 主体全称
            "type":"1",#主体类型 1-有限公司 2-民非机构 3-社会团体 4-个体工商户
            "license_no":"营业执照或登记证书编号",
            "license_file":"营业执照或登记证书图片",
            "country":"国家",
            "province":"省",
            "city":"city",
            "address":"address",
            "legal_person":"legal_person",
            "leader_phone":"leader_phone",
            "leader_name":"leader_name",
            "is_asfc":"1",
            "club_name":"club_name",
            "short_name":"short_name",
            "avatar":"avatar",
            "club_desc":"club_desc",
            "account":"account",
            "password":"123456",
            "confirm":"confirm",
            "club_member":"club_member"
        }
        res1=requests.post(url,params=get_params)
        print("请求状态：",res1.status_code)
        print("请求文本：",res1.text)
        print("请求json：",res1.json())
    def test_获取地址接口(self):
        url="https://www.idrc.com/index/player/area"
        get_params={
            "parent_code":"1"
        }
        res2=requests.get(url,params=get_params)
    def test_jiekou(self):
        url="https://www.idrc.com/index/player/area"
        get_params={
            "parent_code":"1",
        }
        res3=requests.get(url,params=get_params)
        print(res3.text)
        print(res3.json())
        print(res3.cookies)
if __name__ == "__main__":
    pytest.main(["-vs", __file__])  # __file__代表当前文件，-vs包含上述两个参数