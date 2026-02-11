# -*- coding: utf-8 -*-
import json
import requests
import pytest


class TestIdrcApi:
    def test_get_teams_player(self):
        """
        获取参赛战队详情列表
        """
        # 建议优先用 https（很多站点 http 会跳转或被策略限制）
        url = "https://idrc.iflight-rc.com/api/teams/get_teams_player"
        params = {"team_id": "870"}

        # 模拟浏览器请求头，避免被当成“非浏览器/爬虫”返回 HTML 或被拦截
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Referer": "http://idrc.iflight-rc.com/",
        }

        cookies = None

        session = requests.Session()

        # 先请求 https，如果失败再回退 http（避免你环境里 https 有问题）
        resp = None
        last_err = None
        resp = session.get(
            'http://idrc.iflight-rc.com/api/teams/get_teams_player',
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=15,
            allow_redirects=True,
        )
        if resp is None:
            pytest.fail(f"请求失败（网络/域名/协议问题）：{last_err}")

        # ------- 诊断信息（非常关键，方便你定位“为何浏览器能行，代码不行”）-------
        print("status:", resp.status_code)
        print("final_url:", resp.url)
        print("redirect_history:", [r.status_code for r in resp.history])
        print("content-type:", resp.headers.get("Content-Type"))
        print("text_head:", resp.text[:300])


if __name__ == "__main__":
    # -s: 显示 print 输出
    pytest.main(["-s", __file__])
