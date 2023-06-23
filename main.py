import json

phone_book = {}
path: str = 'phones.txt'


def open_file():
    phone_book.clear()
    file = open(path, 'r', encoding='UTF-8')
    data = file.readlines()
    file.close()
    for contact in data:
        nc = contact.strip().split(':')
        phone_book[int(nc[0])] = {'name': nc[1], 'phone': nc[2], 'comment': nc[3]}
    print('\n Телефонная книга успешно загружена.')


def menu() -> int:
    main_menu = '''Главное  меню:
    1. Открыть файл
    2. Сохранить файл
    3. Показать все контакты
    4. Создать контакт
    5. Найти контакт
    6. Изменить контакт
    7. Удалить контакт
    8. Импорт из JSON
    9. Экспорт в JSON
    10. Выход'''
    print(main_menu)
    while True:
        select = input('Выберите пункт меню: ')
        if select.isdigit() and 0 < int(select) < 11:
            return int(select)
        print('Ошибка ввода, введи число от 1 до 10')


def show_contacts(book: dict[int, dict]): #Добавлена подпись столбцов телефонной книги
    print(f'{"".rjust(2)}Id{"".ljust(3)}Имя{"".ljust(17)}Телефон{"".ljust(13)}Комментарий')
    for i, cnt in book.items():
        print(f'{i:>3}. {cnt.get("name"):<20}{cnt.get("phone"):<20}{cnt.get("comment"):<20}')
    print('=' * 200 + '\n')


def add_contact():  # Добавлена возможность подтверждения создания контакта,
    # с обработкой подтверждения при неправильном вводе.
    uid = max(list(phone_book.keys()))

    name = input('Введите имя контакта: ')
    phone = input('Введите телефон контакта: ')
    comment = input('Введите комментарий контакта: ')
    print('Подтвердите создание контакта(0-Нет,1-Да):')
    while True:
        while True:
            try:
                accord = int(input())
                break
            except ValueError:
                print('Упс! Вы ввели не число! Повторите попытку!')
        if accord == 0:
            print(f'\nКонтакт {name} не добавлен!')
            break
        elif accord == 1:
            phone_book[uid + 1] = {'name': name, 'phone': phone, 'comment': comment}
            print(f'\nКонтакт {name} успешно добавлен!')
            break
        else:
            print('Некорректное подтверждение, повторите попытку:')

    print('=' * 200 + '\n')


def save_file(): # Добавил подтверждение сохранения файла, с обработкой подтверждения.
    data = []
    for i, contact in phone_book.items():
        new = ':'.join([str(i), contact.get('name'), contact.get('phone'), contact.get('comment')])
        data.append(new)
    data = '\n'.join(data)
    print('Подтвердите сохранение изменений в книге(0-Нет,1-Да):')
    while True:
        while True:
            try:
                accord = int(input())
                break
            except ValueError:
                print('Упс! Вы ввели не число! Повторите попытку!')
        if accord == 0:
            print(f'\nТелефонная книга не сохранена!')
            break
        elif accord == 1:
            with open(path, 'w', encoding='UTF-8') as file:
                file.write(data)
            print(f'\nТелефонная книга успешно сохранена!')
            break
        else:
            print('Некорректное подтверждение, повторите попытку:')
    print('=' * 200 + '\n')


def search():
    result = {}
    word = input('Введите слово по которому мы будем осуществлять поиск: ')
    for i, contact in phone_book.items():
        if word.lower() in ' '.join(list(contact.values())).lower():
            result[i] = contact
    return result


def remove():# Добавил возможность подтверждения
    result = search()
    show_contacts(result)
    index = int(input('Введите id контакта который хотим удалить: '))
    print('Подтвердите удаление контакта (0-Нет,1-Да):')
    while True:
        while True:
            try:
                accord = int(input())
                break
            except ValueError:
                print('Упс! Вы ввели не число! Повторите попытку!')
        if accord == 0:
            print(f'\nКонтакт {phone_book[index].get("name")} не удален!')
            break
        elif accord == 1:
            del_cnt = phone_book.pop(index)
            print(f'\nКонтакт {del_cnt.get("name")} успешно удален')
            break
        else:
            print('Некорректное подтверждение, повторите попытку:')

def update():  # Добавил возможность обновить данные контакта, с подтверждением обновления
    result = search()
    show_contacts(result)
    index = int(input('Введите id контакта который хотим изменить: '))
    print(f'Чтобы изменить данные контакта с id = {index} введите новое значение, если нет - просто нажмите Enter')

    print('Введите новое имя контакта: ', end='')
    new_name = input()
    print('Введите новый номер телефона контакта: ', end='')
    new_phone = input()
    print('Введите новый комментарий к контакту: ', end='')
    new_comment = input()
    print('Подтвердите удаление контакта (0-Нет,1-Да):')
    while True:
        while True:
            try:
                accord = int(input())
                break
            except ValueError:
                print('Упс! Вы ввели не число! Повторите попытку!')
        if accord == 0:
            print(f'\nКонтакт {phone_book[index].get("name")} не обновлен!')
            break
        elif accord == 1:
            if new_name != '': phone_book[index]['name'] = new_name
            if new_phone != '': phone_book[index]['phone'] = new_phone
            if new_comment != '': phone_book[index]['comment'] = new_comment
            print(f'Данные контакта {phone_book[index].get("name")} успешно изменены')
            break
        else:
            print('Некорректное подтверждение, повторите попытку:')

def impJSON():# Добавлена функция импорта из json-файла
    json_path = input('Укажите путь к JSON файлу: ')
    with open(json_path, 'r',encoding='UTF-8') as file:
        phone_book = json.load(file)
    return phone_book
def expJSON(phone_book: dict):# Добавлена функция экспорта в json-файл
    print("Введите название JSON файла: ",end='')
    file_path = input() + '.json'
    with open(file_path,'w',encoding='UTF-8') as file:
        json.dump(phone_book,file,ensure_ascii=False)
    print("Экспорт успешно выполнен.")


print('По умолчанию открыта телефонная книга phones.txt, для открытия другого воспользуйтесь функцией импорта из JSON-файла.')
open_file()
while True:
    select = menu()
    match select:
        case 1:
            open_file()
        case 2:
            save_file()
        case 3:
            show_contacts(phone_book)
        case 4:
            add_contact()
        case 5:
            result = search()
            show_contacts(result)
        case 6:
            update()
        case 7:
            remove()
        case 8:
            phone_book = impJSON()
        case 9:
            expJSON(phone_book)
        case 10:
            print('До свидания! До новых встреч!')
            break
    print('=' * 200)