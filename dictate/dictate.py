import pyttsx3
from time import sleep
from threading import Thread


class DictateModel:
    def __init__(self):
        self.wrong_alert_msg = 'Wrong answer, please try again!'
        self.correct_msg = 'Congrats, it is correct answer!'


class Dictate(DictateModel):
    def __init__(self):
        self.word_list = []
        self.counter = 0
        self.engine = pyttsx3.init()
        super().__init__()

    def say(self, word: str) -> None:
        if self.engine._inLoop:
            self.engine.endLoop()
        self.engine.say(word)
        self.engine.runAndWait()

    def _next(self) -> None:
        self.counter = (self.counter + 1) % len(self.word_list)
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def _prev(self) -> None:
        self.counter = (self.counter - 1) % len(self.word_list)
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def _same(self) -> None:
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def next(self):
        self.thread_runner(self._next)

    def prev(self):
        self.thread_runner(self._prev)

    def same(self):
        self.thread_runner(self._same)

    def alert_wrong(self) -> None:
        self.say(self.wrong_alert_msg)

    def loop_until_wrong_ans(self) -> None:
        answer = self.get_ans()
        while answer != self.word_list[self.counter]:
            self.alert_wrong()
            self.wait(3)
            self.say(self.word_list[self.counter])
            answer = self.get_ans()
        else:
            self.say(self.correct_msg)

    @staticmethod
    def get_ans() -> str:
        return str(input('Enter the word: '))

    @staticmethod
    def thread_runner(target):
        thread_inst = Thread(target=target)
        thread_inst.start()
        thread_inst.join()

    @staticmethod
    def wait(sec):
        sleep(sec)
