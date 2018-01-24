FILES = [
    'data/normal.dict.txt',
    'data/web.dict.txt',
]

TARGET_FILE = 'data/total.dict.txt'

with open(TARGET_FILE, 'w', encoding='utf-8') as target_file:
    content = ''
    for fn in FILES:
        with open(fn, 'r', encoding='utf-8') as rf:
            content += rf.read()

    target_file.write(content)
