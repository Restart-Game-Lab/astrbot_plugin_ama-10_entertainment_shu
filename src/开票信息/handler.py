"""
开票信息命令执行文件

负责 /开票信息 指令的全部逻辑：发送上海大学收款、开票及外汇账户信息。
"""

ACCOUNT_INFO_TEXT = """1. 人民币账户及增值税开票信息

单位名称：上海大学
统一社会信用代码：1231000042502637XE
开票代码：TQ4HXQ
【宝山校区】
银行账号：03327000801210489
开户银行：中国农业银行上海大场支行
联行号/CNAPS NO.：103290005138
地址/电话：上海市上大路99号，021-66136210
【延长校区】
银行账号：03358400801000968
开户银行：中国农业银行上海共和支行
联行号/CNAPS NO.：103290041057
地址/电话：上海市延长路149号，021-56331221

2. 外汇银行账户信息
Account Name: Shanghai University
Account Number: 30601442920000443
Bank Name: Jingan Sub-branch, Shanghai Pudong Development Bank, Shanghai, P.R.China.
Bank Address: No.669, West Beijing Road, Shanghai, P.R.China.
SWIFT NO.: SPDBCNSHXXX"""


async def handle(event):
    """发送上海大学账户及开票信息。"""
    yield f"\u200b{ACCOUNT_INFO_TEXT}\n\n[2026/11/9]"