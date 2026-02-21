# main.py - 直接复制，无需修改
import os
import akshare as ak
import pandas as pd
import requests
import google.generativeai as genai

# 导入配置
from config import (
    DEEPSEEK_API_KEY, WECHAT_WEBHOOK,
    STOCK_LIST, FUTURE_LIST,
    LANGUAGE, REPORT_LENGTH
)

# 初始化 Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_stock_data(stock_code):
    """获取A股数据"""
    try:
        if stock_code.startswith(("00", "30", "60", "90")):
            # 个股数据
            df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq").tail(1)
            name = ak.stock_info_a_code_name(code=stock_code)
        else:
            # 指数数据
            df = ak.stock_zh_index_daily(symbol=stock_code).tail(1)
            name = stock_code
        if df.empty:
            return f"{stock_code}：数据获取失败"
        latest = df.iloc[-1]
        return f"{name}({stock_code})：收盘价{latest['收盘']}，涨跌幅{latest['涨跌幅']}%"
    except Exception as e:
        return f"{stock_code}：{str(e)[:20]}"

def get_future_data(future_code):
    """获取期货数据"""
    try:
        df = ak.futures_zh_daily(symbol=future_code, adjust="0").tail(1)
        if df.empty:
            return f"{future_code}：数据获取失败"
        latest = df.iloc[-1]
        return f"{future_code}：收盘价{latest['收盘']}，涨跌幅{latest['涨跌幅']}%，持仓量{latest['持仓量']}"
    except Exception as e:
        return f"{future_code}：{str(e)[:20]}"

def generate_ai_report(stock_data, future_data):
    """AI 生成分析报告"""
    prompt = f"""
    你是资深A股和期货分析师，用{REPORT_LENGTH}篇幅、{LANGUAGE}生成每日分析报告，要求：
    1. 总结核心数据，指出涨跌关键；
    2. 给出简洁的操作建议（仅供参考，不构成投资建议）；
    3. 语言通俗，重点突出。

    A股数据：
    {stock_data}

    期货数据：
    {future_data}
    """
    response = model.generate_content(prompt)
    return response.text

def send_wechat(msg):
    """推送到企业微信"""
    if not WECHAT_WEBHOOK:
        print("未配置微信Webhook，跳过推送")
        return
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    try:
        res = requests.post(WECHAT_WEBHOOK, json=data, headers=headers)
        if res.json()["errcode"] == 0:
            print("微信推送成功")
        else:
            print(f"微信推送失败：{res.text}")
    except Exception as e:
        print(f"微信推送异常：{str(e)}")

if __name__ == "__main__":
    print("===== 开始获取A股数据 =====")
    stock_list = [code.strip() for code in STOCK_LIST.split(",")]
    stock_data = [get_stock_data(code) for code in stock_list]
    stock_text = "\n".join(stock_data)

    print("===== 开始获取期货数据 =====")
    future_list = [code.strip() for code in FUTURE_LIST.split(",")]
    future_data = [get_future_data(code) for code in future_list]
    future_text = "\n".join(future_data)

    print("===== AI 生成分析报告 =====")
    ai_report = generate_ai_report(stock_text, future_text)
    final_report = f"""
【每日A股+期货分析报告】
{ai_report}

===== 原始数据 =====
A股：
{stock_text}

期货：
{future_text}

⚠️  提示：以上分析仅供参考，不构成投资建议
    """
    print(final_report)

    print("===== 推送结果 =====")
    send_wechat(final_report)
    print("===== 执行完成 =====")
