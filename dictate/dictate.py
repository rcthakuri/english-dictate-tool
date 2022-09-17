import pickle
from threading import Thread
from time import sleep

import pyttsx3

from dictate.store.store import Store
from dictate.store.words import Words


class DictateModel(Store):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.wrong_ans_frequency_map = {}
        self.correct_msg = 'Congrats, it is correct answer!'
        self.wrong_alert_msg = 'Wrong answer, please try again!'
        self.store_data = self.load()
        self.init()

    def init(self):
        if self.store_data:
            print(self.store_data)
            self.wrong_ans_frequency_map = self.store_data['wfmap']
            self.counter = self.store_data['counter']

    def update_wrong_frequency(self, word) -> None:
        if word in self.wrong_ans_frequency_map.keys():
            self.wrong_ans_frequency_map[word] += 1
        else:
            self.wrong_ans_frequency_map[word] = 1

    def get_wrong_words_in_high_frequency_order(self):
        ordered_dict = {k: v for k, v in
                        sorted(self.wrong_ans_frequency_map.items(),
                               key=lambda item: item[1],
                               reverse=True
                               )
                        }
        return list(ordered_dict.keys())


class Dictate(DictateModel, Words):
    def __init__(self):
        super().__init__()
        Words.__init__(self)
        self.thread_inst_list = []
        self.max_try = 5
        self.engine = pyttsx3.init()
        self.thread_ints_list = []
        self.word_list = self.get_word_list()

    def __del__(self):
        for t_inst in self.thread_inst_list:
            t_inst.join()
        self.save_sate()

    def save_sate(self):
        store_obj = {
            'counter': self.counter,
            'wfmap': self.wrong_ans_frequency_map
        }
        pickle.dump(store_obj, open(self.store_path, 'wb'))

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
        word = self.word_list[self.counter]
        wrong_count = 0
        while answer != word:
            wrong_count += 1
            print(f'try {wrong_count}/{self.max_try}')
            self.update_wrong_frequency(word)
            self.alert_wrong()
            self.wait(3)
            self.say(word)
            answer = self.get_ans()
            if wrong_count >= self.max_try:
                print('Correct answer was -> ', word)
                break
        else:
            self.say(self.correct_msg)

    def set_word_list(self, w_list_type='all'):
        if w_list_type == 'all':
            self.word_list = self.get_word_list()
        if w_list_type == 'wrong':
            self.word_list = self.get_wrong_words_in_high_frequency_order()
            if not self.word_list:
                raise Exception('No words found in store, supply word list!!!')

    def thread_runner(self, target):
        try:
            thread_inst = Thread(target=target)
            self.thread_ints_list.append(thread_inst)
            thread_inst.start()
            thread_inst.join()
        except:
            self.__del__()

    @staticmethod
    def get_ans() -> str:
        return str(input('Enter the word: '))

    @staticmethod
    def wait(sec):
        sleep(sec)
