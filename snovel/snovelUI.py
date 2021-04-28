'''
Description:
Author: cc
Date: 2021-04-19 16:09:33
LastEditors: cc
LastEditTime: 2021-04-28 11:13:17
'''
import os
from prompt_toolkit.application.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.widgets.base import Frame, TextArea
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.layout.dimension import D, Dimension

from snovel import keybindings
from snovel.config import Config
from snovel.book import Book


class RadioBookList(RadioList):
    def __init__(self, values) -> None:
        super().__init__(values)


class RadioChapterList(RadioList):
    def __init__(self, values) -> None:
        super().__init__(values)


class SnovalUI:

    RADIO_WIDTH = 40

    def __init__(self) -> None:
        pass

    def __init__(self, path: str, config: Config) -> None:
        self.createUI()

        if not os.path.isdir(path):
            path = config.DEFAULT_PATH
        self.search_dir_books(path)
        self.load_book(self.radio_book_list.current_value)

    def createUI(self):
        self.radio_book_list = RadioBookList(values=[(None, "(None)")])
        self.radio_chapter_list = RadioChapterList(values=[(None, "(None)")])
        self.text_area = TextArea(
            multiline=True,
            focusable=False,
            wrap_lines=True,
            scrollbar=False,
            read_only=True,
            line_numbers=False
        )

        root_conationer = VSplit([
            HSplit([
                Frame(
                    title="Books",
                    body=self.radio_book_list,
                    height=Dimension(min=3, max=12, preferred=12),
                    key_bindings=keybindings.book_list(self)
                ),
                Frame(
                    title="Chapters",
                    body=self.radio_chapter_list,
                    height=Dimension(min=8, preferred=12),
                    key_bindings=keybindings.chapter_list(self)
                )
            ], width=D.exact(self.RADIO_WIDTH)),
            HSplit([
                Frame(body=self.text_area,
                      key_bindings=keybindings.text_area(self))
            ])
        ])

        self.application = Application(
            layout=Layout(root_conationer,
                          focused_element=self.radio_book_list),
            key_bindings=keybindings.root(self),
            enable_page_navigation_bindings=True,
            full_screen=True,
            mouse_support=True
        )

    def load_book(self, value):
        self.book = Book(value)
        self.radio_chapter_list.values = self.book.get_table_content_tuple_list()

    def search_dir_books(self, path):
        res = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".txt"):
                    res.append((os.path.join(root, f), f))
        if res:
            self.radio_book_list.values = res
            self.radio_book_list.current_value = res[0][0]

    def select_book(self):
        self.load_book(self.radio_book_list.current_value)

    def select_chapter(self):
        columns = self.application.output.get_size().columns-self.RADIO_WIDTH-2
        rows = self.application.output.get_size().rows-2
        data = self.book.get_content(
            self.radio_chapter_list.current_value, rows, columns)
        if data is None:
            return
        self.text_area.text = data

    def next_page(self):
        columns = self.application.output.get_size().columns-self.RADIO_WIDTH-2
        rows = self.application.output.get_size().rows-2
        data = self.book.get_content(
            self.radio_chapter_list.current_value, rows, columns)

        if data is None:
            self.radio_chapter_list.current_value += 1
            self.select_chapter()
            return

        self.text_area.text = data

    def previous_page(self):
        self.text_area.buffer.cursor_up()

    def run(self):
        self.application.run()


if __name__ == "__main__":
    snoval = SnovalUI("./", Config)
    snoval.run()
