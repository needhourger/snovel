'''
Description:
Author: cc
Date: 2021-04-19 16:09:33
LastEditors: cc
LastEditTime: 2021-04-29 11:42:35
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
        self.load_book()

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
        self.text_frame = Frame(body=self.text_area,
                                key_bindings=keybindings.text_area(self))

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
                self.text_frame
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

    def load_book(self):
        self.book = Book(self.radio_book_list.current_value)
        self.radio_chapter_list.values = self.book.catalog
        self.radio_chapter_list.current_value = self.book.p_chapter
        self.next_page()

    def search_dir_books(self, path):
        res = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".txt"):
                    res.append((os.path.join(root, f), f))
        if res:
            self.radio_book_list.values = res
            self.radio_book_list.current_value = res[0][0]

    def select_chapter(self):
        self.book.select_chapter(self.radio_chapter_list.current_value)
        self.next_page()

    def next_page(self):
        columns = (self.application.output.get_size().columns -
                   self.RADIO_WIDTH-2)//2
        rows = self.application.output.get_size().rows-2
        data = self.book.next_page(rows, columns)

        if data is None:
            return

        self.text_area.text = data
        # self.text_frame.title = self.book.chapter_title
        self.radio_chapter_list.current_value = self.book.p_chapter

    def previous_page(self):
        columns = self.application.output.get_size().columns-self.RADIO_WIDTH-2
        rows = self.application.output.get_size().rows-2
        data = self.book.previous_page(rows, columns)

        if data is None:
            return

        self.text_area.text = data
        # self.text_frame.title = self.book.chapter_title
        self.radio_chapter_list.current_value = self.book.p_chapter

    def run(self):
        self.application.run()


if __name__ == "__main__":
    snoval = SnovalUI("./", Config)
    snoval.run()
