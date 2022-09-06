import pyttsx3


class Dictate:
    def __init__(self):
        self.word_list = []
        self.counter = 0
        self.engine = pyttsx3.init()

    def say(self, word: str) -> None:
        self.engine.say(word)
        self.engine.runAndWait()

    def next(self) -> None:
        self.counter = (self.counter + 1) % len(self.word_list)
        self.say(self.word_list[self.counter])

    def prev(self) -> None:
        self.counter = (self.counter - 1) % len(self.word_list)
        self.say(self.word_list[self.counter])

    def same(self) -> None:
        self.say(self.word_list[self.counter])

