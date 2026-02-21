# config.py - 直接复制，替换以下【】中的内容
import os

# ===================== 必改配置 =====================
# 1. AI 分析接口配置（二选一即可，推荐 Gemini）
# DEEPSEEK_API_KEY = os.getenv("sk-9085536762ae4be48ffc67553aa858d2")  # 若用深度求索，替换此行

# 2. 推送配置（企业微信机器人）
WECHAT_WEBHOOK = os.getenv("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eb82dddc-bb30-4fbc-bd09-d088e9a68732")  # 从 GitHub Secrets 读取，也可直接填地址

# 3. 自选标的（A股代码/期货合约代码，用英文逗号分隔）
# A股示例：000001（平安银行）、600519（贵州茅台）、000300（沪深300）
STOCK_LIST = "000001,600519,000300"
# 期货示例：cu2603（沪铜）、if2603（沪深300股指）、m2605（豆粕）
FUTURE_LIST = "cu2603,if2603,m2605"

# ===================== 可选配置 =====================
# 分析语言（中文/英文）
LANGUAGE = "zh"
# 分析报告长度（short/medium/long）
REPORT_LENGTH = "short"
# 收盘时间（A股15:00，期货15:00/23:00）
CLOSE_TIME = "15:00"
