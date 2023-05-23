import argparse
import json
import os
import random
from collections import OrderedDict

cards = {}
random.seed(2)
lines = []
hardest_cards = OrderedDict()
export_file = ''


def ask():
    usr_msg = 'How many times to ask?\n'
    lines.append(usr_msg)
    times_to_ask = int(input(usr_msg))
    lines.append(str(times_to_ask) + '\n')
    keys = (list(cards.keys()))
    key = random.choice(keys)
    for i in range(0, times_to_ask):
        def_message = f'Print the definition of "{key}":\n'
        __user_inp = input(def_message)
        lines.append(__user_inp + '\n')
        if cards[key] == __user_inp:
            correct_msg = "Correct!"
            lines.append(correct_msg)
            print(correct_msg)
            key = random.choice(keys)
        elif __user_inp in cards.values():
            k = (key for key, val in cards.items() if val == __user_inp)
            wrong_msg = f"""Wrong. The right answer is "{cards[key]}", but your definition is correct for "{''.join(k)}"."""
            lines.append(wrong_msg)
            print(wrong_msg)
            update_hardest_cards(key)
        else:
            wrong_msg = f'Wrong. The right answer is "{cards[key]}".'
            lines.append(wrong_msg)
            print(wrong_msg)
            update_hardest_cards(key)
        key = random.choice(keys)


def update_hardest_cards(key):
    if key in hardest_cards.keys():
        val = hardest_cards[key]
        hardest_cards[key] = val + 1
    else:
        hardest_cards[key] = 1


def add():
    term_incorrect = True
    definition_incorrect = True
    card_msg = "The card:\n"
    term = input(card_msg)
    lines.append(card_msg)
    lines.append(term + '\n')
    while term_incorrect:
        if term in cards.keys():
            card_exist_msg = f'The term "{term}" already exists. Try again:'
            lines.append(card_exist_msg)
            print(card_exist_msg)
            term = input()
            lines.append(term + '\n')
        else:
            term_incorrect = False

    def_msg = f'The definition of the card:\n'
    definition = input(def_msg)
    lines.append(definition + '\n')
    while definition_incorrect:
        if definition in cards.values():
            def_exist_msg = f'The definition "{definition}" already exists. Try again:'
            print(def_exist_msg)
            definition = input()
            lines.append(definition + '\n')
        else:
            definition_incorrect = False
            cards[term] = definition
    pair_added_msg = f"""The pair ("{term}":"{definition}") has been added."""
    print(pair_added_msg)
    lines.append(pair_added_msg)


def remove():
    card_msg = "Which card?\n"
    usr_inp = input(card_msg)
    lines.append(card_msg)
    lines.append(usr_inp + '\n')
    if usr_inp in cards.keys():
        card_removed_msg = 'The card has been removed.'
        print(card_removed_msg)
        lines.append(card_removed_msg)
        del cards[usr_inp]
    else:
        err_msg = f"""Can't remove "{usr_inp}": there is no such card.\n"""
        print(err_msg)
        lines.append(err_msg)


def _import(file_path=None):
    if file_path is None:
        file_name_msg = 'File name:\n'
        file_path = input(file_name_msg)
        lines.append(file_name_msg)
        lines.append(file_path + '\n')

    if not os.path.exists(file_path):
        file_not_found_msg = 'File not found.'
        print(file_not_found_msg)
        lines.append(file_not_found_msg)
        return

    with open(file_path, mode='r') as f:
        temp_dict = {}
        temp_dict |= dict(json.load(f))

    cards_loaded_msg = f'{len(temp_dict)} cards have been loaded.'
    print(cards_loaded_msg)
    lines.append(cards_loaded_msg)
    cards.update(temp_dict)


def export(file_path=None):
    if file_path is None:
        file_name_msg = "File name:\n"
        file_path = input(file_name_msg)
        lines.append(file_name_msg)
        lines.append(file_path + '\n')
    with open(file_path, 'w') as f:
        json.dump(cards, f)
    cards_saved_msg = f"{len(cards)} cards have been saved."
    print(cards_saved_msg)
    lines.append(cards_saved_msg)


def log():
    file_name_msg = 'File name:'
    file_path = input(file_name_msg)
    lines.append(file_name_msg)
    lines.append(file_path + '\n')
    with open(file_path, 'a') as f:
        f.writelines(lines)
        f.close()
        lines.clear()
    file_saved_msg = 'The log has been saved.'
    lines.append(file_saved_msg)
    print(file_saved_msg)


def hardest_card():
    if len(hardest_cards) == 0:
        empty_dict_msg = 'There are no cards with errors.'
        print(empty_dict_msg)
        lines.append(empty_dict_msg + '\n')
        return

    sorted_dict = sorted(hardest_cards.items(), key=lambda x: x[1])
    prev_val = sorted_dict[len(sorted_dict) - 1][-1]
    lst = []
    for item in reversed(sorted_dict):
        val = hardest_cards[item[0]]
        if val == prev_val:
            prev_val = val
            lst.append(item[0])
        else:
            break

    lst.reverse()
    if len(lst) == 1:
        msg = f'The hardest card is "{lst[0]}". You have {prev_val} errors answering it.'
        print(msg)
        lines.append(msg + '\n')
    else:
        for i in range(len(lst)):
            v = "\"" + lst[i] + "\"" + ", "
            lst[i] = v
        last_item = lst[len(lst) - 1].rstrip(", ")
        lst[len(lst) - 1] = last_item

        msg = f'The hardest cards are {"".join(str(x) for x in lst)}. You have {prev_val} errors answering them.'
        print(msg)
        lines.append(msg + '\n')


def reset_stats():
    hardest_cards.clear()
    msg = 'Card statistics have been reset.'
    print(msg)
    lines.append(msg + '\n')


def main():
    while True:
        menu_msg = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n"
        user_inp = input(menu_msg)
        lines.append(menu_msg)
        lines.append(user_inp + '\n')
        if user_inp == 'add':
            add()
        elif user_inp == 'remove':
            remove()
        elif user_inp == 'import':
            _import()
        elif user_inp == 'export':
            export()
        elif user_inp == 'ask':
            ask()
        elif user_inp == 'log':
            log()
        elif user_inp == 'hardest card':
            hardest_card()
        elif user_inp == 'reset stats':
            reset_stats()
        elif user_inp == 'exit':
            bye_msg = "Bye bye!"
            print(bye_msg)
            lines.append(bye_msg)
            if export_file != '':
                export(export_file)
            exit()
        print()


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--import_from")
    parse.add_argument("--export_to")
    args = parse.parse_args()

    if args.import_from is not None:
        _import(args.import_from)

    if args.export_to is not None:
        export_file = args.export_to
    main()
