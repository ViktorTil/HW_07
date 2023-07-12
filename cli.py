from classes import AddressBook
from func import add_phone, get_birthdate, change, delete, delete_phones, find_contact, phone, show_all, when_birthday

commands = ["hello", ["good bye", "close", "exit", "bye", "esc", "q"], "add", "birthdate", "change", "del", "del phones", "find", "phone", "show all", "birthday"]
answers = ["How can I help you?", "Good bye!", add_phone, get_birthdate, change, delete, delete_phones, find_contact, phone, show_all, when_birthday]


def main():
    working_bot= True
    phone_book = AddressBook(
    phone_book.load_book()
    
        
    while working_bot:
        command = input("->")
        working_bot = reply(command, phone_book)
    phone_book.save_book()
            

def reply(command, phone_book):
    bot=True
    operator=command.lower().split(" ")
    if command.lower() in commands[1]:
        print(answers[1])
        
        bot = False
    elif operator[0] in commands or (" ".join(command.lower().split(" ")[:2])) in commands:
        try:
            index_comm = commands.index(" ".join(command.lower().split(" ")[:2]))
        except ValueError:
            index_comm = commands.index(operator[0])

        try:
            print(answers[index_comm](command, phone_book))

        except:
            print(answers[index_comm])
    else:
        print(f'Введите правильную команду :\033[34m{commands[0]}, {", ".join(commands[2:])}\033[0m или \033[34m{", ".join(commands[1])}\033[0m для выхода')

    return bot


if __name__ == '__main__':
    main()
