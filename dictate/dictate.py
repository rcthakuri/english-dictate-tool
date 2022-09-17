import pyttsx3


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
        self.engine.say(word)
        self.engine.runAndWait()

    def next(self) -> None:
        self.counter = (self.counter + 1) % len(self.word_list)
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def prev(self) -> None:
        self.counter = (self.counter - 1) % len(self.word_list)
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def same(self) -> None:
        self.say(self.word_list[self.counter])
        self.loop_until_wrong_ans()

    def alert_wrong(self) -> None:
        self.say(self.wrong_alert_msg)

    def loop_until_wrong_ans(self) -> None:
        answer = self.get_ans()
        while answer != self.word_list[self.counter]:
            self.alert_wrong()
            self.say(self.word_list[self.counter])
            answer = self.get_ans()
        else:
            self.say(self.correct_msg)

    @staticmethod
    def get_ans() -> str:
        return str(input('Enter the word: '))
