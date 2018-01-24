import os


def get_module_res(*res):
    try:
        import pkg_resources
        return pkg_resources.resource_stream(
            __name__,
            os.path.join(*res)
        )
    except:
        return open(
            os.path.normpath(os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                *res)
            ),
            'rb'
        )


def is_han(text):
    # sample: is_han('一') == True, is_han('我&&你') == False
    return all('\u4e00' <= char <= '\u9fff' for char in text)
