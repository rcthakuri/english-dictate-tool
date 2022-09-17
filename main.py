from dictate.dictate import Dictate
from dictate.store.words import Words


def cli_menu(dictate_callback):
    menu = '''
1. Next/Same/Previous : N/S/P or n/s/p
2. Practise wrongs words: W/w
3. Practise all words: A/a
4. Quite: Q/q
           '''

    print(menu)

    menu_option = input("$ Your input [n/s/p/w/a/q]=> ")

    if menu_option in ['N', 'n']:
        dictate_callback.next()
    elif menu_option in ['P', 'p']:
        dictate_callback.prev()
    elif menu_option in ['S', 's']:
        dictate_callback.same()
    elif menu_option in ['W', 'w']:
        try:
            dictate_callback.set_word_list(w_list_type='wrong')
        except Exception as e:
            print(e)
            print('Reverting to original word list...')
            dictate_callback.set_word_list(w_list_type='all')
    elif menu_option in ['A', 'a']:
        dictate_callback.set_word_list(w_list_type='all')

    elif menu_option in ['q', 'Q']:
        quit()
    else:
        print('\nWrong cmd!, enter proper command')


def dictate_loop():
    dictate = Dictate()

    while True:
        cli_menu(dictate)


if __name__ == '__main__':
    dictate_loop()
