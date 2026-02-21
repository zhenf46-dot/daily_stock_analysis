import os
import akshare as ak
import requests
from datetime import datetime

# ===================== 从Secrets读取配置（和你的Secrets名称一致） =====================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK")

# ===================== 自选标的（按需修改） =====================
STOCK_LIST = "000001,600519,000300"  # 平安银行、茅台、沪深300
FUTURE_LIST = "cu2603,if2603,m2605"  # 沪铜、沪深300股指、豆粕

# -------------------- 1. 获取A股数据 --------------------
def get_stock_data(stock_code):
    try:
        if stock_code.startswith(("00", "30", "60", "90")):
            df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq").tail(1)
            name = ak.stock_info_a_code_name(code=stock_code)
        else:
            df = ak.stock_zh_index_daily(symbol=stock_code).tail(1)
            name = stock_code
        if df.empty:
            return f"{stock_code}：数据获取失败"
        latest = df.iloc[-1]
        return f"{name}({stock_code})：收盘价{latest['收盘']:.2f}，涨跌幅{latest['涨跌幅']:.2f}%"
    except Exception as e:
        return f"{stock_code}：{str(e)[:20]}"

# -------------------- 2. 获取期货数据 --------------------
def get_future_data(future_code):
    try:
        df = ak.futures_zh_daily(symbol=future_code, adjust="0").tail(1)
        if df.empty:
            return f"{future_code}：数据获取失败"
        latest = df.iloc[-1]
        return f"{future_code}：收盘价{latest['收盘']:.2f}，涨跌幅{latest['涨跌幅']:.2f}%，持仓量{latest['持仓量']}"
    except Exception as e:
        return f"{future_code}：{str(e)[:20]}"

# -------------------- 3. DeepSeek AI生成分析报告 --------------------
def generate_ai_report(stock_data, future_data):
    if not DEEPSEEK_API_KEY:
        return "未配置DeepSeek API Key，无法生成AI分析"
    
    prompt = f"""
    你是10年经验的A股期货分析师，用100字生成每日分析，分A股、期货、总结三部分，语言通俗，建议仅供参考。
    A股数据：{stock_data}
    期货数据：{future_data}
    """

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI分析失败：{str(e)[:50]}"

# -------------------- 4. 企业微信推送 --------------------
def send_wechat(msg):
    if not WECHAT_WEBHOOK:
        print("未配置微信Webhook，跳过推送")
        return
    headers = {"Content-Type": "application/json"}
数据 ={
        "msgtype": "text",
        "text": {"content": msg}
    }
    尝试:
        res = requests.post(WECHAT_WEBHOOK, json=data, headers=headers)
        if res.json()["errcode"] == 0:
            打印(“微信推送成功”)
        否则:
            print(f"微信推送失败：{res.text}")
    除了异常作为e：
        print(f"微信推送异常：{str(e)}")

# -------------------- 5. 主执行逻辑 --------------------
if __name__ == "__main__":
    # 获取数据
    stock_text = "\n".join([get_stock_data(code) for code in STOCK_LIST.split(",")])
    future_text = "\n".join([get_future_data(code) for code in FUTURE_LIST.split(",")])
    
    # 生成报告
    ai_report = generate_ai_report(stock_text, future_text)
    final_report = f"""
【每日分析报告 {datetime.now().strftime('%Y-%m-%d')}】
{ai_report}

===== 原始数据 =====
A股：
{stock_text}

期货：
{未来文本}

⚠️  分析仅供参考，不构成投资建议
    """
    
    # 推送+打印
    发送微信(最终报告)
    打印(最终报告)
