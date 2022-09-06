from dictate.dictate import Dictate

WORD_LIST = [
    'haha',
    'ok',
    'done'
]


def dictate_loop():
    dictate = Dictate()
    dictate.word_list = WORD_LIST

    while True:
        prev_or_next_or_same: 'N' or 'P' = input("Play next or prev or same(N/P/S): ")
        if prev_or_next_or_same in ['N', 'n']:
            dictate.next()
        elif prev_or_next_or_same in ['P', 'p']:
            dictate.prev()
        elif prev_or_next_or_same in ['S', 's']:
            dictate.same()
        else:
            print('\nWrong cmd!, enter N or P or S')
        line_formatter()


def line_formatter():
    print("\n")


if __name__ == '__main__':
    dictate_loop()
