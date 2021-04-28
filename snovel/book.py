'''
Description: 
Author: cc
Date: 2021-04-19 14:41:42
LastEditors: cc
LastEditTime: 2021-04-28 10:23:34
'''
import re
import chardet


class Chapter:

    CHAPTER_SIGN = ["卷", "章", "节", "篇"]

    def __init__(self) -> None:
        pass

    def __init__(self, data: str) -> None:
        temp = data.splitlines()
        lines = []
        for i in temp:
            if i.strip() == "":
                continue
            lines.append(i)

        self.content = []
        if not lines:
            return

        if len(lines) == 1:
            self.title = lines[0].strip()
            self.content = lines
        else:
            if self._has_chapter_sign(lines[0]):
                self.title = lines[0].strip()
                self.content = lines[1:]
            else:
                self.title = lines[0].strip()
                self.content = lines

        self._p = 0

    def get_content(self, rows: int, columns: int):
        if self._p >= len(self.content):
            return None

        ret = ""
        line_rows = len(self.content[self._p])/columns + \
            (0 if len(self.content[self._p]) % columns == 0 else 1)
        while (rows-line_rows > 0):
            ret += self.content[self._p]
            self._p += 1
            rows = rows-line_rows
            if (self._p < len(self.content)):
                line_rows = len(self.content[self._p])/columns + \
                    (0 if len(self.content[self._p]) % columns == 0 else 1)
            else:
                break

        return ret

    @classmethod
    def _has_chapter_sign(cls, data):
        for i in cls.CHAPTER_SIGN:
            if i in data:
                return True
        return False


class Book:

    def __init__(self) -> None:
        self.chapters = []
        self.table_contents = []

    def __init__(self, path: str) -> None:
        if not path:
            self.__init__()
            return

        encoding = self.get_encoding(path)
        with open(path, "r", encoding=encoding) as f:
            data = f.read()
            f.close()

            chapters = re.split(r'\n[\n]+', data)
            if not chapters:
                self.chapters = None

            self._get_info(chapters[0])

            self.chapters = []
            for c in chapters:
                self.chapters.append(Chapter(c))

            self.table_contents = [i.title for i in self.chapters]

    def _get_info(self, data: str):
        self.name = None
        self.author = None

        lines = data.splitlines()
        for i, v in enumerate(lines):
            if "作者" in v:
                if i > 0:
                    self.name = lines[i-1].strip()
                self.author = v.strip()
                return

    def get_content(self, index: int, rows: int, columns: int):
        if index < 0 or index >= len(self.chapters):
            return None

        return self.chapters[index].get_content(rows, columns)

    def get_table_content_tuple_list(self):
        return [(i, v) for i, v in enumerate(self.table_contents)]

    @classmethod
    def get_encoding(cls, file):
        if not file:
            return None
        with open(file, "rb") as f:
            ret = chardet.detect(f.read(1024))["encoding"]
            f.close()
            if ret == "GB2312":
                ret = "GBK"
            return ret


if __name__ == "__main__":
    b = Book("./test1.txt")
    print(b.get_content(0, 0, 800))
