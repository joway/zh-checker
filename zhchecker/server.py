from lemon.app import Lemon
from lemon.context import Context
from lemon.router import Router

from zhchecker import ZhChecker

zh_checker = ZhChecker()


async def checker(ctx: Context):
    data = ctx.req.json
    content = data['content']

    ret = zh_checker.check(content=content)
    ret = [r.to_json() for r in ret]
    ctx.body = {
        'data': ret,
    }


async def correct(ctx: Context):
    data = ctx.req.json
    content = data['content']

    ret = zh_checker.correct(content=content)
    ret = [r.to_json() for r in ret]
    ctx.body = {
        'data': ret,
    }


app = Lemon(debug=True)

router = Router()
router.post('/api/v1/zhchecker/check', checker)
router.post('/api/v1/zhchecker/correct', correct)

app.use(router.routes())

app.listen(host='0.0.0.0')
