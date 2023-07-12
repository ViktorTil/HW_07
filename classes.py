from collections import UserDict
from datetime import datetime
import pickle
import re

class AddressBook(UserDict):

    filename = "data.bin"
    
    def add_record(self, record):
        self.data[record.name.value] = record


    def del_record(self, record):
        self.data.pop(record.name.value)
        
    def iterator(self, page_len = 3):
        page = {}
        for name, value in self.data.items():
            page.update({name : value})
            if len(page) == page_len:
                yield page
                page = {}
        if page:
            yield page
    
    def load_book(self):

        try:
            with open(self.filename, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass
    
    def save_book(self):
        with open(self.filename, "wb") as fh:
            pickle.dump(self.data, fh)   

        
class Field:
    def __init__(self, value):
        self.value = value
        


class Birthday(Field):
    def __init__(self, value : str = None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            birth_date = re.findall('\d+', value)
            if birth_date[2] and len(birth_date[2])==4:
                birth_date[2] = birth_date[2][2:]
            birth ="/".join(birth_date)
            self.__value = datetime.strptime(birth, '%d/%m/%y').date()
        except ValueError:
            print(f"Введите корректную дату в формате \033[34mmm-dd-yyyy\033[0m")

class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, phone):
        try:
            pattern = r"\+?3?8?[- (]?0\d{2}[- )]?\d{3}[- ]?\d{2}[- ]?\d{2}$"
            add_cod = "+380"
            result = (re.search(pattern, phone)).group()
            res_phone=re.sub(r"(\D)","",result)
            form_phone = add_cod[0:13-len(res_phone)] + res_phone
            self.__value = form_phone
            
        except AttributeError:
            print(f"Строка \033[34m{phone}\033[0m не похожа на укр телефон. Введите корректно номер телефона, например, в формате: \033[34m0XX-XXX-XX-XX\033[0m")
    


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday : Birthday = None):
        self.phones = []
        self.name = name
        if phone and phone.value:
            self.phones.append(phone)

        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone.value:
            self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                self.phones.pop(index)
                self.add_phone(new_phone)
                return f"У контакта \033[34m{self.name.value}\033[0m телефон \033[34m{old_phone.value}\033[0m изменён на \033[34m{new_phone.value}\033[0m"
        return f"Нет номера \033[34m{old_phone.value}\033[0m для изменения у контакта \033[34m{self.name.value}\033[0m"

    def del_phone(self):    
        self.phones.clear()
        
    def days_to_birthday(self):
        cd = datetime.now().date()
        if hasattr(self, "birthday") and self.birthday:
            nd = self.birthday.value
            if nd.month == 2 and nd.day == 29:
                new_bd = datetime(year = cd.year, month = 2, day = nd.day - int(bool(cd.year%4))).date()
            
                if new_bd < cd: 
                    new_bd = datetime(year = cd.year + 1, month = 2, day = nd.day - int(bool((cd.year+1)%4))).date()
            
            else:
                new_bd = new_bd = datetime(year = cd.year, month = nd.month, day = nd.day).date()
                if new_bd < cd:
                    new_bd = new_bd.replace(year = cd.year + 1)
            if  new_bd != cd:
                return f"До Дня рождения \033[34m{self.name.value}\033[0m осталось \033[34m{(new_bd - cd).days}\033[0m дня(ей)"
            return f"У контакта \033[34m{self.name.value}\033[0m сегодня День рождения! Поздравьте его"
        else:
            return f"У контакта \033[34m{self.name.value}\033[0m нет в книге даты рождения "

