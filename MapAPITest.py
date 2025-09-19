# -*- coding: utf-8 -*-
# @Time    : 2026/9/19 16:20
# @Author  : Dragonkeep
# @File    : MapAPITest.py

import requests

BaiDu_AK =  ""  # 在这里填写百度地图API密钥
GaoDe_AK = ""  # 在这里填写高德地图API密钥
Tencent_AK = ""  # 在这里填写腾讯地图API密钥
Google_AK = ""  # 在这里填写谷歌地图API密钥

# 测试百度地图API AK是否可以使用
def BaiduMapAPI(ak):
    result={
        "Server_API": False,
        "Referer_Whitelist": False,
    }
    # 1. 服务端API有效性检测
    api_url = "http://api.map.baidu.com/geocoding/v3/"
    params = {"address": "北京天安门", "output": "json", "ak": ak}
    try:
        r_api = requests.get(api_url, params=params, timeout=5)
        data = r_api.json()
        #print(data)
        if data.get("status") == 0:
            result["Server_API"] = True
    except Exception as e:
        print(f"[!] 服务端API请求异常: {e}")

    # 2. Referer白名单检测（设置非白名单域名）
    headers = {"Referer": "http://example.com"}
    try:
        r_url=f"https://api.map.baidu.com/geocoding/v3/"
        r_ref = requests.get(r_url, params=params,headers=headers, timeout=5)
        #print(r_ref.text)
        if data.get("status") == 0:
            result["Referer_Whitelist"] = True
    except Exception as e:
        print(f"[!] Referer检测异常: {e}")

    return result

# 测试高德API Key是否可以使用
def GaoDeMapAPI(key):
    results={
        "PLATFORM": "",
        "Status": False,
        "Reason": ""
    }

    params = {"key": key}
    try:
        api_url = "https://restapi.amap.com/v3/ip"
        r = requests.get(api_url, params=params, timeout=5)
        data = r.json()
        if data.get("status") == "1":
            results["Status"] = True
            results["Reason"] = "Key有效"
            results["PLATFORM"] = "Web服务API"
        else:
            try:
                api_url = "https://webapi.amap.com/maps?v=2.0"
                r = requests.get(api_url, params=params, timeout=5)
                data = r.json()
                if data.get("status") == "1":
                    results["Status"] = True
                    results["Reason"] = "Key有效"
                    results["PLATFORM"] = "JavaScript API"
                else:
                    results["Reason"] = data.get("info", "未知错误")
                    results["PLATFORM"] = "未知"
            except Exception as e:
                pass
    except Exception as e:
        pass
    return results

# 测试Google Maps API Key是否可以使用
def GoogleMapAPI(key):
    results={
        "Status": False,
        "Reason": ""
    }
    proxies = {
    "http": "socks5://127.0.0.1:7890",
    "https": "socks5://127.0.0.1:7890",
}
    params = {"key": key, "address": "Beijing"}
    try:
        api_url = "https://maps.googleapis.com/maps/api/geocode/json"
        r = requests.get(api_url, params=params, timeout=10,proxies=proxies)
        data = r.json()
        if data.get("status") == "OK":
            results["Status"] = True
            results["Reason"] = "Key有效"
        else:
            results["Reason"] = data.get("error_message", "未知错误")
    except Exception as e:
        print(f"[!] Google Maps API请求异常: {e}")
    return results

# 测试腾讯地图API Key是否可以使用
def TencentMapAPI(key):
    results={
        "Status": False,
        "Reason": ""
    }
    params = {"key": key, "address": "北京"}
    try:
        api_url = "https://apis.map.qq.com/ws/geocoder/v1/"
        r = requests.get(api_url, params=params, timeout=5)
        data = r.json()
        if data.get("status") == 0:
            results["Status"] = True
            results["Reason"] = "Key有效"
        else:
            results["Reason"] = data.get("message", "未知错误")
    except Exception as e:
        print(f"[!] 腾讯地图API请求异常: {e}")
    return results


if __name__ == "__main__":
    if  BaiDu_AK:
        results = BaiduMapAPI(BaiDu_AK)
        print("百度地图API密钥检测结果:")
        for k, v in results.items():
            status = "可用" if v else "不可用"
            print(f"{k}: {status}")
    if GaoDe_AK:
        results = GaoDeMapAPI(GaoDe_AK)
        print("高德地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
    if Google_AK:
        results = GoogleMapAPI(Google_AK)
        print("Google地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
    if Tencent_AK:
        results = TencentMapAPI(Tencent_AK)
        print("腾讯地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
