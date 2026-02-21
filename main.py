
import requests

def generate_ai_report(stock_data, future_data):
    """用 DeepSeek 生成分析报告"""
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
    # DeepSeek API 调用
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
