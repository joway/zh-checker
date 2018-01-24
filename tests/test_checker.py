from zhchecker import ZhChecker

checker = ZhChecker()


class TestChecker(object):
    def test_checker(self):
        content = """
我今天要翻医一篇文章
"""
        ret = checker.check(content=content)
        print(ret)
