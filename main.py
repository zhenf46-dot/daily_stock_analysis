import os
import akshare as ak
import requests
from datetime import datetime

# ===================== 从Secrets读取配置 =====================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK")

# ===================== 自选标的（英文引号，无中文符号） =====================
STOCK_LIST = "000001,600519,000300"  # 平安银行、贵州茅台、沪深300
FUTURE_LIST = "cu2603,if2603,m2605"  # 沪铜2603、沪深300股指、豆粕2605

# -------------------- 1. 获取A股数据 --------------------
def get_stock_data(stock_code):
    try:
        # 区分个股和指数
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
    
    # 提示词用英文引号，无中文符号
    prompt = """
    你是拥有10年A股和期货分析经验的资深分析师，按以下要求生成每日分析报告：
    1. 语言：中文，篇幅：100字以内，通俗易懂；
    2. 内容：分A股、期货、总结三部分，先总结数据，再给简洁建议；
    3. 提示：分析仅供参考，不构成投资建议。

    A股数据：
    {}

    期货数据：
    {}
    """.format(stock_data, future_data)

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI分析生成失败：{str(e)[:50]}"

# -------------------- 4. 企业微信推送 --------------------
def send_wechat(msg):
    if not WECHAT_WEBHOOK:
        print("未配置企业微信Webhook，跳过推送")
        return
    
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }

    try:
        res = requests.post(WECHAT_WEBHOOK, json=data, headers=headers)
        res.raise_for_status()
        if res.json()["errcode"] == 0:
            print("✅ 微信推送成功")
        else:
            print(f"❌ 微信推送失败：{res.text}")
    except Exception as e:
        print(f"❌ 微信推送异常：{str(e)}")

# -------------------- 5. 主执行逻辑 --------------------
if __name__ == "__main__":
    print("===== 开始获取A股数据 =====")
    # 处理A股列表（英文逗号分隔）
    stock_list = [code.strip() for code in STOCK_LIST.split(",")]
    stock_data = [get_stock_data(code) for code in stock_list]
    stock_text = "\n".join(stock_data)

    print("===== 开始获取期货数据 =====")
    # 处理期货列表（英文逗号分隔）
    future_list = [code.strip() for code in FUTURE_LIST.split(",")]
未来数据 =获取未来数据(代码)for代码在未来列表]
未来文本 =" ".join(未来数据)

    打印("===== AI生成分析报告 =====")
    # 生成AI分析报告
    ai_report = generate_ai_report(stock_text, future_text)
    # 拼接最终报告（所有引号都是英文半角）
    final_report = f"""
【每日A股+期货分析报告 {datetime.now().strftime('%Y-%m-%d %H:%M')}】
{ai_report}

===== 原始数据 =====
A股：
{stock_text}

期货：
{未来文本}

⚠️  提示：以上分析仅供参考，不构成任何投资建议
    """
    最终报告)

    打印("===== 推送分析报告 =====")
    # 推送到企业微信（同步到普通微信）
    发送微信(最终报告)
    打印(“===== 执行完成 =====”)
