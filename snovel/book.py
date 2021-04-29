'''
Description:
Author: cc
Date: 2021-04-28 15:29:40
LastEditors: cc
LastEditTime: 2021-04-29 18:06:08
'''
from snovel.database import T_Book

import os
import re
import chardet


class Book:

    def __init__(self, tbook: T_Book) -> None:
        self.id = None
        self.name = "(None)"
        self.author = None
        self.chapters = []
        self.p_chapter = 0
        self.path = None
        if not tbook:
            return

        self.id = tbook.id
        self.name = tbook.name
        self.author = tbook.author
        self.path = tbook.path

        if not os.path.exists(tbook.path):
            return

        encoding = get_encoding(tbook.path)
        with open(tbook.path, "r", encoding=encoding) as f:
            data = f.read()
            f.close()

            cs = re.split(r"\n[\n]+", data)
            if not cs:
                return

            self.__get_book_info(cs[0])

            for c in cs:
                self.chapters.append(Chapter(c))

            self.p_chapter = tbook.p_chapter
            self.chapters[self.p_chapter].p_start = tbook.p_start
            self.chapters[self.p_chapter].p_end = tbook.p_end

    @property
    def catalog(self):
        return [(i, v.title) for i, v in enumerate(self.chapters)]

    def __get_book_info(self, data: str):
        self.author = None

        lines = data.splitlines()
        for i, v in enumerate(lines):
            if "作者" in v:
                self.author = v.strip()
                return

    @property
    def chapter_title(self):
        return self.chapters[self.p_chapter].title

    def select_chapter(self, index: int):
        self.p_chapter = index
        self.chapters[self.p_chapter].p_init()

    def next_page(self, rows: int, columns: int):
        if self.p_chapter < 0 or self.p_chapter >= len(self.chapters):
            return None

        data = self.chapters[self.p_chapter].next_content(rows, columns)
        if data is None:
            if self.p_chapter+1 < len(self.chapters):
                self.p_chapter += 1
                self.chapters[self.p_chapter].p_init()
                return self.next_page(rows, columns)
            else:
                return None
        return data

    def previous_page(self, rows: int, columns: int):
        if self.p_chapter < 0 or self.p_chapter >= len(self.chapters):
            return None

        data = self.chapters[self.p_chapter].previous_content(rows, columns)
        if not data:
            if self.p_chapter-1 >= 0:
                self.p_chapter -= 1
                self.chapters[self.p_chapter].p_init(last=True)
                return self.previous_page(rows, columns)
            else:
                return None
        return data

    def export_tbook(self):
        ret = {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "p_chapter": self.p_chapter,
            "path": self.path,
            "p_start": self.chapters[self.p_chapter].p_start,
            "p_end": self.chapters[self.p_chapter].p_end
        }

        return ret


class Chapter:

    CHAPTER_SIGN = ["序", "卷", "章", "节", "篇", "后记"]

    def __init__(self, data: str) -> None:
        self.content = ""
        self.title = "(None)"
        self.p_start = 0
        self.p_end = 0

        ls = data.splitlines(keepends=True)
        lines = []
        for l in ls:
            if l.strip() == "":
                continue
            lines.append(l)

        if lines == []:
            return

        if len(lines) == 1:
            self.title = lines[0].strip()
            self.content = "".join(lines)
        else:
            if self.__has_chapter_sign(lines[0]):
                self.title = lines[0].strip()
                self.content = "".join(lines[1:])
            else:
                self.content = "".join(lines)

    def next_content(self, rows: int, columns: int):
        self.p_start = self.p_end
        if self.p_start >= len(self.content):
            return None

        p = self.p_start
        while rows > 0:
            if self.p_end+columns <= len(self.content):
                self.p_end += columns
                row = self.content[p:self.p_end]
                if "\n" in row:
                    self.p_end = self.p_end-columns+row.index("\n")+1
                rows -= 1
                p = self.p_end
            else:
                self.p_end = len(self.content)
                break
        return self.content[self.p_start:self.p_end]

    def previous_content(self, rows: int, columns: int):
        self.p_end = self.p_start
        if self.p_start <= 0:
            return None

        p = self.p_end
        while rows > 0:
            if self.p_start-columns >= 0:
                self.p_start = self.p_start-columns
                row = self.content[self.p_start:p]
                if "\n" in row:
                    self.p_start = self.p_start+row.index("\n")+1
                rows -= 1
                p = self.p_start
            else:
                self.p_start = 0
                break
        return self.content[self.p_start:self.p_end]

    def p_init(self, last=False):
        if last:
            self.p_start = len(self.content)
            self.p_end = len(self.content)
        else:
            self.p_start = 0
            self.p_end = 0

    @classmethod
    def __has_chapter_sign(cls, data: str):
        for i in cls.CHAPTER_SIGN:
            if i in data:
                return True
        return False


def get_encoding(file):
    with open(file, "rb") as f:
        ret = chardet.detect(f.read(1024))["encoding"]
        f.close()
        if ret == "GB2312":
            ret = "GBK"
        return ret


if __name__ == "__main__":
    b = Book("./test1.txt")
    # b.select_chapter(20)
    while True:
        input()
        d = b.next_page(30, 116)
        print(b.p_chapter, len(d))
        print(d)
