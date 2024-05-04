# Объявляем все необходимые импорты для работы приложения
from os import path
import json
from datetime import datetime, timedelta
from MyExceptions import UserNameException, PasswordException, JsonException


class Wallet:
    # Реализуем работу кошелька через ООП
    
    # Статический метод для инициализации json у нового пользователя
    @staticmethod
    def create_user_json():
        # Метод для создания начальных данных пользователя
        data = {
            "password": int(input("Установите пароль, состоящий только из цифр:\n")),
            "total": 0,
            "purchases": [],
            "deposits": []
        }
        return data
    
    @staticmethod
    def read_json(name):
        # Статический метод для чтения данных из файла JSON
        with open(f"D:/PyProjects/GitHub/MyWallet/Users/{name}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    
    @staticmethod
    def create_data(string):
        # Статический метод для создания разметки расхода\дохода под JSON
        data = {"ID": len(User.read_json(User.name_of_user)["deposits"]) + 1,
                "category": string,
                "name": input("Введите описание\n"),
                "value": (int(input("Введите сумму:\n"))),
                "date": input("Введите дату в формате '04-05-2024'\n")}
        return data
    
    def __init__(self, name):
        # Магический метод для инициализации всех экземпляров
        
        # Проверка, что имя пользователя состоит только из латинских букв
        if (set(name.lower()) & set("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())) == set(name.lower()):
            self.__name = name
        else:
            raise UserNameException("Доступ запрещён!")
        
        # Проверка на то, существует ли файл с данными пользователя
        if not path.exists(f"D:/PyProjects/GitHub/MyWallet/Users/{self.__name}.json"):
            # Если файл не существует, создаем новый файл с данными пользователя
            data = self.create_user_json()
            with open(f"D:/PyProjects/GitHub/MyWallet/Users/{self.__name}.json", 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            # Если файл существует, считываем данные из него
            data = self.read_json(self.__name)
            # Запрашиваем пароль для подтверждения доступа
            if int(input("Введите пароль для подтверждения\n")) == data["password"]:
                print("Доступ разрешён!")
            else:
                raise PasswordException("Доступ запрещён!")
    
    @property
    def name_of_user(self):
        # Свойство-геттер для взаимодействия с атрибутом вне класса
        return self.__name
    
    def balance(self):
        # Метод для получения баланса пользователя
        return self.read_json(self.__name)["total"]
    
    def deposits_upd(self, dict_value):
        # Метод для обновления данных о доходах/расходах и обновления баланса пользователя
        data = self.read_json(self.__name)
        if dict_value["category"] == "Доход":
            data["total"] += dict_value["value"]
        else:
            data["total"] -= dict_value["value"]
        data["deposits"].append(dict_value)
        with open(f"D:/PyProjects/GitHub/MyWallet/Users/{self.__name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def deposits_edit(self, date_for_editing, string):
        # Метод для редактирования данных о доходах/расходах
        data = self.read_json(self.__name)
        print(f"\nОперации за {date_for_editing.strftime("%d-%m-%Y")}:")
        for i in filter(lambda x: datetime.strptime(x["date"], "%d-%m-%Y") == date_for_editing,
                        data["deposits"]):
            if i["category"] == string:
                print(*i.values(), sep=' ' * 8)
        inp_value = int(input("\nВыберите номер для редактирования\n"))
        if string == "Доход":
            data["total"] -= data["deposits"][inp_value - 1]["value"]
        else:
            data["total"] += data["deposits"][inp_value - 1]["value"]
        data["deposits"][inp_value - 1] = self.create_data(string)
        if string == "Доход":
            data["total"] += data["deposits"][inp_value - 1]["value"]
        else:
            data["total"] -= data["deposits"][inp_value - 1]["value"]
        with open(f"D:/PyProjects/GitHub/MyWallet/Users/{self.__name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def detail_info(self, flag):
        # Метод для получения детальной информации о доходах/расходах
        data = self.read_json(self.__name)
        
        param = int(input("\nВыберите какие операции вы хотите увидеть:\n"
                          "1 - Все операции за всё время\n"
                          "2 - Операции определённой даты\n"
                          "3 - Операции с определённой суммой\n"))
        
        if param == 1:
            print(f"\nВсе {flag}ы:")
            for i in data["deposits"]:
                if i["category"] == flag:
                    print(*i.values(), sep=' ' * 8)
        
        elif param == 2:
            date = input("Введите дату в формате '04-05-2024'\n")
            print(f"\nВсе {flag}ы: за {date}")
            for i in filter(lambda x: x["date"] == date and x["category"] == flag, data["deposits"]):
                print(*i.values(), sep=' ' * 8)
        
        elif param == 3:
            value = int(input("Введите сумму\n"))
            print(f"\nВсе {flag}ы с суммой {value} Бенджаменов:")
            for i in data["deposits"]:
                if i["value"] == value:
                    print(*i.values(), sep=' ' * 8)
    
    def last_month(self):
        # Метод для получения операций за последний месяц
        data = self.read_json(self.__name)
        print("\nОперации за последний месяц:")
        
        # Поднимаем исключение, если список операций пуст
        if not data["deposits"]:
            raise JsonException
        
        for i in filter(lambda x: datetime.strptime(x["date"], "%d-%m-%Y") >= datetime.now() - timedelta(days=31),
                        data["deposits"]):
            print(*i.values(), sep=' ' * 8)


if __name__ == "__main__":
    while True:
        try:
            # Запрашиваем имя пользователя и создаем экземпляр класса Wallet
            User = Wallet(
                input("Привет, пользователь приложения MyWallet! Представься, пожалуйста (Только латиницей).\n"))
            break
        except Exception:
            print("Неверное имя пользователя или пароль, попробуйте ещё раз.\n")
    
    print(f"Большое спасибо, {User.name_of_user}!")
    
    while True:
        while True:
            try:
                # Запрашиваем команду у пользователя
                choose = int(input("\nВыберите что вы хотите сделать в своём кошельке\n"
                                   "1 - Посмотреть баланс\n"
                                   "2 - Добавить запись о доходах\n"
                                   "3 - Добавить запись о расходах\n"
                                   "4 - Изменить запись о доходах\n"
                                   "5 - Изменить запись о расходах\n"
                                   "6 - Детально о доходах\n"
                                   "7 - Детально о расходах\n"
                                   "8 - Сводка за месяц\n"
                                   "0 - Выход\n"))
                break
            except ValueError:
                print("\nНеизвестная команда, попробуйте ещё.")
        
        match choose:
            case 1:
                print(f"\nУ вас на балансе {User.balance()} Бенджаменов")
            
            case 2:
                User.deposits_upd(User.create_data("Доход"))
            
            case 3:
                User.deposits_upd(User.create_data("Расход"))
            
            case 4:
                User.deposits_edit(datetime.strptime(input("Введите дату, доходы за которую хотите отредактировать, "
                                                           "в формате '04-05-2024'\n"), "%d-%m-%Y"), "Доход")
            
            case 5:
                User.deposits_edit(datetime.strptime(input("Введите дату, расходы за которую хотите отредактировать, "
                                                           "в формате '04-05-2024'\n"), "%d-%m-%Y"), "Расход")
            
            case 6:
                User.detail_info("Доход")
            
            case 7:
                User.detail_info("Расход")
            
            case 8:
                try:
                    User.last_month()
                except JsonException:
                    print("Список пуст!")
            
            case 0:
                print(f"До скорых встреч, {User.name_of_user}!")
                break
            
            case _:
                print("\nНинада так, делай по инструкции!")
