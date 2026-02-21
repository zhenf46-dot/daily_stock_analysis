import os

# ===================== 必改配置（填你的信息） =====================
# DeepSeek API Key（从DeepSeek平台复制）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# 企业微信机器人Webhook地址（从企业微信复制）
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK")

# ===================== 可选配置（按需修改） =====================
# 自选A股代码（英文逗号分隔）
STOCK_LIST = "000001,600519,000300"  # 平安银行、茅台、沪深300
# 自选期货合约代码（英文逗号分隔）
FUTURE_LIST = "cu2603,if2603,m2605"  # 沪铜、沪深300股指、豆粕
# 分析报告语言/长度
LANGUAGE = "zh"          # 仅支持中文
REPORT_LENGTH = "short"  # short(100字)/medium(200字)/long(300字)
