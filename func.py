from classes import Name, Phone, Record, Birthday
import re


def error_with_func(arg1,arg2):
    def input_error(func):
        def proc_error(*args):
            try:
               return func(*args)
            except IndexError:
                return f'Добавьте все данные в команду \033[34m{arg1}\033[0m по шаблону: \033[34m<{arg2}>\033[0m'
            except ValueError:
                pass
        return proc_error
    return input_error


@error_with_func('add', "add [name] [phone]")  
def add_phone(cont, phone_book):
    
    contact = cont.split(' ')[1:]

    name = contact[0].capitalize()
    contact_phone = "".join(contact[1:])
    if len(contact) >= 2:
        if not name in phone_book.keys():
            phone = Phone(contact_phone)
            rec = Record(Name(name), phone)
            phone_book.add_record(rec)
            if phone.value:
                message_add = f"Новый контакт \033[34m{name}\033[0m с номером \033[34m{phone.value}\033[0m создан"
            else:
                message_add = f"Новый контакт \033[34m{name}\033[0m без номера создан"
        else: 
            rec = phone_book.get(name)
            phone = Phone(contact_phone)
            if phone.value:
                rec.add_phone(phone)
                message_add = f"Номер \033[34m{phone.value}\033[0m добавлен к контакту \033[34m{name}\033[0m"
            else:
                message_add = f"Не могу её добавить в контакты \033[34m{name}\033[0m"
                
                
    else:
        message_add =  "Добавьте в команду \033[34madd\033[0m номер телефона"
        if not name in phone_book.keys():
            rec = Record(Name(name))
            phone_book.add_record(rec)
            message_add = f"Контакт \033[34m{name}\033[0m без номера добавлен"
        
    return message_add
        
@error_with_func("birthdate", 'birthdate [name] dd-mm-yy')
def get_birthdate(comm, phone_book):
    comm_birth = comm.split(' ')[1:]
    name = comm_birth[0].capitalize()
    message_birthday = f"В вашей книге ещё нет контакта \033[34m{name}\033[0m"
    if name in phone_book.keys():
        birth_str = "".join(comm_birth[1:])
        birt_list = re.findall(r'\d{2}', birth_str)
        birth = ",".join([birt_list[0],birt_list[1],"".join(birt_list[2:])])
        add_birth = Birthday(birth)
        message_birthday = f"Контакту \033[34m{name}\033[0m не могу записать эту дату рождения "
        if add_birth.value:
            phone_book.get(name).birthday = add_birth
            message_birthday= f"Контакту \033[34m{name}\033[0m добавили дату рождения \033[34m{add_birth.value}\033[0m"
    return message_birthday

    
@error_with_func("birthday", 'birthday [name]')
def when_birthday(comm, phone_book):
    c_number=comm.split(" ")[1].capitalize()
    message_birth = f'В ваших контактах отсутствует \033[34m{c_number}\033[0m'
    if c_number in phone_book.keys():
        message_birth = phone_book.get(c_number).days_to_birthday()
    return message_birth


@error_with_func("change", 'change [name] [old_phone], [new_phone]')
def change(contact, phone_book):
    chng_phone = contact.split(',')
    chng_cont = chng_phone[0].split(' ')[1:]
    name = chng_cont[0].capitalize()
    old_phone = "".join(chng_cont[1:])
    new_phone = chng_phone[1]
    if name in phone_book.keys():
        rec = phone_book.get(name)
        message_chng = rec.change_phone(Phone(old_phone), Phone(new_phone))
    
    else :
        message_chng = f'Нет контакта \033[34m{name}\033[0m в Вашем списке'
    return message_chng


@error_with_func('del', 'del [name]')
def delete(contact, phone_book):
    c_number=contact.split(" ")[1].capitalize()
    message_del_cont = f"Не могу удалить номер несуществующего контакта \033[34m{c_number}\033[0m"
    if c_number in phone_book.keys():
        phone_book.del_record(phone_book.get(c_number))
        message_del_cont = f"Контакт \033[34m{c_number}\033[0m удалён из Вашей книги"
    return message_del_cont
 
        
@error_with_func('del phones', 'del phones [name]')
def delete_phones(contact, phone_book):
    del_ph = contact.title().split(' ')[2:]
    message_del_phones = f"Не могу удалить телефоны несуществующего контакта \033[34m{del_ph[0]}\033[0m"
    if del_ph[0] in phone_book.keys():
        phone_book.get(del_ph[0]).del_phone()
        message_del_phones = f"Номера контакта \033[34m{del_ph[0]}\033[0m удалены из книги"
    return message_del_phones


@error_with_func('find', 'find [str]')
def find_contact(command, phone_book):
    str_find = command.split(" ")[1]
    itog_find = ""
    for rec in phone_book.values():
        united_value = rec.name.value.lower() + ''.join(list(phone.value for phone in rec.phones))
        find_str = united_value.find(str_find.lower()) + 1
        
        if find_str:
            try:
                itog_find = itog_find + f"Имя: \033[34m{rec.name.value}\033[0m, дата рождения: \033[34m{rec.birthday.value}\033[0m телефонные номера: \033[34m{', '.join(list(phone.value for phone in rec.phones))}\033[0m \n"
            except AttributeError:
                itog_find = itog_find + f"Имя: \033[34m{rec.name.value}\033[0m, телефонные номера: \033[34m{', '.join(list(phone.value for phone in rec.phones))}\033[0m \n"

    if not itog_find:
        itog_find = f"По вашему поиску в книге ничего не найдено"
         
    return itog_find


@error_with_func('phone', 'phone [name]')
def phone(contact, phone_book):
    c_number=contact.split(" ")[1].capitalize()
    message_cont = f'В ваших контактах отсутствует \033[34m{c_number}\033[0m'
    if c_number in phone_book.keys():
        message_cont = f"Номер(а) контакта \033[34m{c_number} : {', '.join(list(phone.value for phone in phone_book.get(c_number).phones))}\033[0m"
    return message_cont


def show_all(comm, phone_book):
    try:
        page_len = int(comm.removeprefix("show all"))
    except ValueError:
        page_len = 3
        
    num_rec = len(phone_book)
    for i in phone_book.iterator(page_len):
        for value in i.values():
            num_rec -= 1
            try:
                print(f"Имя: \033[34m{value.name.value}\033[0m, дата рождения: \033[34m{value.birthday.value}\033[0m телефонные номера: \033[34m{', '.join(list(phone.value for phone in value.phones))}\033[0m")
            
            except AttributeError:
                print(f"Имя: \033[34m{value.name.value}\033[0m, телефонные номера: \033[34m{', '.join(list(phone.value for phone in value.phones))}\033[0m")   
        if  num_rec > 0:
            input(f"Вывод по \033[34m{page_len}\033[0m контактов из книги, для продолжения нажмите \033[34m[ENTER]\033[0m")
    return ""
