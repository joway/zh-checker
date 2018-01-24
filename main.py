# encoding=utf-8

from zhchecker import ZhChecker

checker = ZhChecker()

ret = checker.check("""
今天天气真豪。

哈哈哈，你是一个怀人。
""")

for r in ret:
    print(r.to_json())
