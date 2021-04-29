'''
Description: 
Author: cc
Date: 2021-04-20 17:04:40
LastEditors: cc
LastEditTime: 2021-04-29 16:25:38
'''
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next


def root(cls):
    kb = KeyBindings()
    kb.add("tab")(focus_next)

    @kb.add("c-c")
    def _(event):
        cls.save()
        event.app.exit()

    @kb.add("c-right")
    def _(event):
        cls.next_page()

    @kb.add("c-left")
    def _(event):
        cls.previous_page()

    return kb


def book_list(cls):
    kb = KeyBindings()

    @kb.add("c-x")
    def _(event):
        cls.save()
        cls.load_book()

    return kb


def chapter_list(cls):
    kb = KeyBindings()

    @kb.add("c-x")
    def _(event):
        cls.select_chapter()

    return kb


def text_area(cls):
    kb = KeyBindings()

    return kb
