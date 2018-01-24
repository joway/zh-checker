import string

import jieba
from pypinyin import pinyin, Style

from zhchecker.utils import get_module_res, is_han

# jieba dict
DEFAULT_DICT = 'data/total.dict.txt'
# 一级字表
DEFAULT_WORDS_TABLE = 'data/level1_words_table.txt'
# 符号
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）—"
PUNCTUATION_LIST += " \n\t"


class TokenMark(object):
    def __init__(self, phrase, start, end, corrects=None):
        self.phrase = phrase
        self.start = start
        self.end = end
        self.corrects = corrects or []

    def to_json(self):
        return {
            'phrase': self.phrase,
            'start': self.start,
            'end': self.end,
            'corrects': self.corrects,
        }

    def __str__(self):
        return str(self.to_json())


class ZhChecker(object):
    def __init__(self, dict_file=None):
        self.dict_file = dict_file or DEFAULT_DICT
        self.words_table_file = DEFAULT_WORDS_TABLE

        self.phrase_freq = {}
        self.words_table = set()

        self.load()

    def check(self, content):
        ret = []
        tokens = jieba.tokenize(content)
        for token in tokens:
            if token[0] in PUNCTUATION_LIST:
                continue
            if not is_han(token[0]):
                continue

            if token[0] not in self.phrase_freq:
                mark = TokenMark(
                    phrase=token[0],
                    start=token[1],
                    end=token[2]
                )
                ret.append(mark)
        return ret

    def correct(self, content):
        checked = self.check(content)
        if len(checked) == 0:
            # nothing can be correct
            return False, None
        for mark in checked:
            mark.corrects = self.correct_phrase(mark.phrase)

        return checked

    def correct_phrase(self, error_phrase):
        splits = ((error_phrase[:i], error_phrase[i:]) for i in range(len(error_phrase) + 1))
        # 仅考虑单个字错误的情况
        candidates = (
            L + c + R[1:] for L, R in splits if R for c in self.words_table
        )
        candidates = (c for c in candidates if c in self.phrase_freq)

        # 通过拼音进行谐音词纠错
        target_phrase_pinyin = self._list_possible_pinyin(error_phrase)
        # 拼音完全一致
        trusted = []
        for candidate in candidates:
            _pinyin_list = self._list_possible_pinyin(candidate)
            diff = target_phrase_pinyin & _pinyin_list
            if diff:
                trusted.append(candidate)
                continue
        trusted = max(trusted, key=lambda k: self.phrase_freq[k]) if trusted else []
        return trusted

    def load(self):
        jieba.load_userdict(get_module_res(self.dict_file))
        self._load_phrase_freq()
        self._load_words_table()

    def _load_words_table(self):
        words_table_file = get_module_res(self.words_table_file)
        for line in words_table_file:
            content = line.decode('utf-8')
            word = content.replace('\n', '')
            self.words_table.add(word)

    def _load_phrase_freq(self):
        dict_file = get_module_res(self.dict_file)
        for line in dict_file:
            content = line.decode('utf-8')
            data = content.split(' ')
            phrase, freq = data[0], data[1]
            self.phrase_freq[phrase] = freq

    def _list_possible_pinyin(self, phrase):
        pinyin_set = None
        for word_pinyin in pinyin(phrase, style=Style.NORMAL, heteronym=True):
            if pinyin_set is None:
                pinyin_set = set(word_pinyin)
            else:
                pinyin_set = {
                    tpp + '/' + wp for tpp in pinyin_set
                    for wp in word_pinyin
                }
        return pinyin_set
