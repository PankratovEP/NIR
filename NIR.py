import sqlite3 as sq

# Отображение полей БД
def vivod_info():
    global pole_names
    with sq.connect('NIR.sqlite') as con:
        cur = con.cursor()
        ls = list(cur.execute('PRAGMA table_info(scores)'))
        print("Таблица содержит следующие поля: ")
        pole_names = [i[1] for i in ls]
        print(*pole_names, sep='    ')


# Отображение текущего содержимого таблицы БД на экране в виде таблицы
def one():
    with sq.connect('NIR.sqlite') as con:
        cur = con.cursor()
        tablica = cur.execute('SELECT rowid, * FROM scores')
        [print(*i, sep='  ') for i in tablica]


# Сохранение текущего содержимого таблицы БД в текстовый файл с задаваемым именем
def two():
    with sq.connect('NIR.sqlite') as con, open(f'{input("Введите имя файла для вывода информации: ")}', 'w') as output:
        cur = con.cursor()
        tablica = cur.execute('SELECT * FROM scores')
        for i in tuple(tablica):
            dat = list(map(lambda x: str(x) + '   ', i)) + ['\n']
            output.writelines(dat)


# Выбор пользователем имени одного из полей БД и задание условия по значениям этого поля (логическое выражение).
# Отображение в виде таблицы подмножества строк, удовлетворяющих заданному условию.
def three():
    vivod_info()
    colom = input('Введите имя интересующего поля: ')
    with sq.connect('NIR.sqlite') as con:
        cur = con.cursor()
        cur.execute(f'SELECT * FROM scores WHERE {input(f"Введите условие (логич-ое выражение) поиска по {colom}: ")}')
        result = cur.fetchall()
        [print(*i, end='\n') for i in result]


# Выбор операции с подмножеством строк: .
def four():
    print(f'Таблица имеет вид:')
    one()
    oper = int(input('''Какую операцию хотите выполнить?
    1) Удалить данные из БД 
    2) Замена значений во всех строках в выбранном поле на выбранное значение
    Операция: '''))
    with sq.connect('NIR.sqlite') as con:
        cur = con.cursor()
        if oper == 2:  # операция замены в выбранных строках значений, которые сам выбирает и задает пользователь
            vivod_info()
            pole = input('Введите нужное поле: ')
            while pole not in pole_names:
                pole = input('Пожалуйста, ведите существующее поле: ')
            stroki = list(map(int, input('Введите rowid интересующих строк через пробел: ').split()))
            for i in stroki:
                dat_type = lambda x: int(x) if x.isdigit() and len(x) < 3 else str(x)
                cur.execute(f"UPDATE scores SET {pole} = ? WHERE rowid = {i}", [dat_type(input("Введите новое значение (оценку и семестр в кавычки заключать не надо): "))])
        elif oper == 1:  # операция удаления строки целиком
            udalenie = list(map(int, input('Введите rowid строк для удаления через пробел: ').split()))
            for i in udalenie:
                cur.execute("DELETE FROM scores WHERE rowid = ?", [i])


# Добавление новой строки с заданными значениями полей в таблицу БД.
def five():
    with sq.connect('NIR.sqlite') as con:
        cur = con.cursor()
        params = (input('Код дисциплины по учебному плану: '), input('Название дисциплины: '),
        int(input('Номер семестра с аттестацией по дисциплине: ')), input('Тип аттестации (экзамен/зачет): '),
        input('Дата аттестации: '), input('ФИО экзаменатора: '),input('Должность преподавателя: '),
        int(input('Полученная оценка: ')), input('Дата занесения/обновления записи: '))
        cur.execute('INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', params)


# для зацикливания программы
def ex(inp):
    return {1: one, 2: two, 3: three, 4: four, 5: five}.get(inp)


print('Добро пожаловать в интерфейс редактирования аттестационных данных!\n')
vivod_info()
print('''\n\nВыберите какую операцию хотите сделать и введите цифру: 
    1) Отображение текущего содержимого таблицы БД на экране в виде таблицы.
    2) Сохранение текущего содержимого таблицы БД в текстовый файл с задаваемым именем.
    3) Выбор пользователем имени одного из полей БД и задание условия по
    значениям этого поля (логическое выражение). Отображение в виде таблицы
    подмножества строк, удовлетворяющих заданному условию.
    4) Выбор операции с подмножеством строк: удаление из БД, замена
    значений во всех строках в указанном поле на заданное значение.
    5) Добавление новой строки с заданными значениями полей в таблицу БД.
    6) Выход из программы''')
while True:
    che_delat = int(input('''\nОперация номер: '''))
    while che_delat > 6:
        che_delat = int(input('''Введите корректную операцию, номер операции: '''))
    if che_delat == 6:
        exit(print('Всего доброго!'))
    else:
        ex(che_delat)()


