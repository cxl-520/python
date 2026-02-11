from pkgutil import get_data
from tokenize import cookie_re

import requests
import pytest
class Test_idrcspi():
    def test_获取参赛战队详情列表(self):
        url="http://idrc.iflight-rc.com/api/teams/get_teams_player"
        get_params = {
            "team_id":"870",
            "carnival_id":"767",
            "page":"1",
            "size":"10"
        }
        json_data={
            "team_id":"870",
            "carnival_id":"767",
            "page":"1",
            "size":"10"
        }
        # headers = {
        #     "User-Agent": (
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        #         "AppleWebKit/537.36 (KHTML, like Gecko) "
        #         "Chrome/120.0.0.0 Safari/537.36"
        #     ),  # ✅ 这里不要再写逗号
        #     "Accept": "application/json, text/plain, */*",
        #     "Referer": "https://idrc.iflight-rc.com/",
        # }
        cookie_re={
            "PHPSESSID":"kujvjl6pfvnaqg1hnamj0f84b8",
            "backend_language":"zh-cn",
            "frontend_language":"zh-cn",
            "token":"47f77b10-7bd2-4d34-be27-1a4ad7e1df6b",
            "uid":"1"
        }
        res1=requests.get(url,params=get_params,cookies=cookie_re)
        # res1 = request_demo.get(url, params=get_params, headers=headers,data=get_data)
        print("请求状态：", res1.status_code)
        print("请求文本：", res1.text)
        print("请求json：", res1.json())
if __name__ == '__main__':
    pytest.main(["-s", __file__])
