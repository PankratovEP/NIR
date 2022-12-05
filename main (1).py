import sqlite3 as sq
import pandas as pd
from itertools import chain

# Отображение содержимого таблицы
def vivod_soderjimogo():
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        nomer = input('''Выберите таблицу, содержимое которой требуется вывести:
    1. Таблица "Картотека вузов"  - vuzkart  с записями, содержащими сведения о вузах России.
    2. Таблица vuzstat, содержащая статистические данные по вузам.
    3. Обе таблицы.

Введите номер :''')

        while nomer not in ['1', '2', '3']:
            print('Некорректный ввод! Требуется ввести цифру от 1 до 3. Попробуйте ещё раз.')
            nomer = input('''Выберите таблицу, содержимое которой требуется вывести:
    1. Таблица "Картотека вузов"  - vuzkart  с записями, содержащими сведения о вузах России.
    2. Таблица vuzstat, содержащая статистические данные по вузам.
    3. Обе таблицы.
        
Введите номер :''')
        nomer = int(nomer)
        if nomer == 1:
            for i in cur.execute('SELECT rowid, * FROM vuzkart'):
                print(*i, sep=' ')
        elif nomer == 2:
            for i in cur.execute('SELECT rowid, * FROM vuzstat'):
                print(*i, sep=' ')
        elif nomer == 3:
             for i in cur.execute('SELECT rowid, * FROM vuzkart'):
                print(*i, sep=' ')
             for i in cur.execute('SELECT rowid, * FROM vuzstat'):
                print(*i, sep=' ')


# Вывод перечня полных наименований вузов,расположенных
# в выбранном субъекте и осуществляющих заочное обучение студентов
def perechen():
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        print('Полный список субъектов: ')
        vse_subjecty = list([i[0].strip() for i in set(cur.execute('SELECT oblname FROM vuzkart'))])
        print(*vse_subjecty, sep='\n')
        subject = input('\nВведите название выбранного субъекта: ')

        while subject not in vse_subjecty:
            print('\nНекорректный ввод! Такого субъекта нет в таблице. Попробуйте ещё раз.')
            print('\nПолный список субъектов: ')
            print(vse_subjecty)
            subject = input('\nВведите название выбранного субъекта: ')

        dic_reg = dict(zip([i[0].strip() for i in set(cur.execute('SELECT oblname FROM vuzkart'))],
                           [i[0] for i in set(cur.execute('SELECT oblname FROM vuzkart'))]))

        id = tuple([i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE oblname == "{dic_reg[subject]}"')])
        id_zaoch = list([i[0] for i in cur.execute(f'SELECT codvuz FROM vuzstat WHERE st_z!=0 AND codvuz IN {id}')])
        vuzy = list([list(cur.execute(f'SELECT z1 from vuzkart WHERE codvuz == "{i}"')) for i in id_zaoch])
        print(*[j[0].strip() for j in [i[0] for i in vuzy]], sep='\n')





'''Обеспечить возможность пользователю выбрать из списка федеральный округ или значение «Все».

 Для выбранного федерального округа рассчитать и представить в виде таблицы распределение количества студентов по профилям вузов.
 
 Таблица должна иметь столбцы: порядковый номер, профиль, количество студентов, обучающихся по данному профилю в выбранном
 федеральном округе, процент от общего количества студентов в вузах данного федерального округа. Нижняя строка – итоговая:
 в столбце профиля – значение «все», в столбце «количество студентов» - число студентов в федеральном округе.'''

def vtor_punkt():
    with sq.connect('VUZ.sqlite') as con:
        def tabl(ids):
            for vuz_prof in dic_tab['Профиль вуза'][:-1]:
                buf_id = list(cur.execute(f'SELECT codvuz FROM vuzkart WHERE codvuz IN {tuple(ids)} AND prof == "{vuz_prof}" '))
                buf_id = tuple([j for i in buf_id for j in i if j])
                kol_stud = [[j[0] for j in cur.execute(f'SELECT stud FROM vuzstat WHERE codvuz == "{i}"')][0] for i in
                            buf_id]
                dic_tab['Кол-во студентов'].append(sum(kol_stud))

            dic_tab['Кол-во студентов'].append(sum(dic_tab['Кол-во студентов']))
            all_studs = dic_tab['Кол-во студентов'][-1]
            for ks in dic_tab['Кол-во студентов']:
                dic_tab['Процент от общего кол-ва студентов'].append(round(ks / all_studs, 4) * 100)
            print(pd.DataFrame(dic_tab).to_markdown(tablefmt='grid', index=False))

        cur = con.cursor()
        print('\nВ таблице присутствуют следующие федеральные округа: ')
        [print(i[0].strip(), end='  ') for i in set(cur.execute('SELECT region FROM vuzkart'))]
        reg = input('\n\nВведите интересующий Вас регион, если хотите выбрать все регионы, то введите "Всего": ')
        dic_reg = dict(zip([i[0].strip() for i in set(cur.execute('SELECT region FROM vuzkart'))] + ["Всего"],
                           [i[0] for i in set(cur.execute('SELECT region FROM vuzkart'))] + ["Всего"]))
        dic_tab = {'Порядковый номер': [1, 2, 3, 4, 5],
                   'Профиль вуза': ('ИТ', 'КЛ', 'МП', 'ГП', 'Все'),
                   'Кол-во студентов': [],
                   'Процент от общего кол-ва студентов': []}
        while reg not in dic_reg.keys():
            print('Пожалуйста, укажите корректное значение!')
            reg = input(r'Введите интересующий Вас федеральный округ, если хотите выбрать все, то введите "Всего": ')
        if reg == "Всего":
            regs = list(dic_reg.keys())
            id_s = [[i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE region =="{dic_reg[j]}"')] for j in regs][: -1]
            id_s = list(chain.from_iterable(id_s))
            tabl(id_s)
        else:
            id_s = [i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE region == "{dic_reg[reg]}"')]
            tabl(id_s)
       


# Основная часть

print('Начало работы')

while True:
    print('''\nСписок возможных операций: 
    1. Вывод содержимого любой из таблиц.
    2. Вывод перечня полных наименований вузов,расположенных 
    в выбранном субъекте и осуществляющих заочное обучение студентов. 
    3. Расчет и представление в виде таблицы распределения количества 
    студентов по профилям вузов для выбранного федерального округа.
    4. Завершение работы с программой''')
    operacia = int(input('\nУкажите цифру нужной операции: '))
    if operacia<1 or operacia>4:
        print('Некорректный ввод! Требуется ввести цифру от 1 до 4. Попробуйте ещё раз.')
        print('''\nСписок возможных операций: 
            1. Вывод содержимого любой из таблиц.
            2. Вывод перечня полных наименований вузов,расположенных 
            в выбранном субъекте и осуществляющих заочное обучение студентов. 
            3. Расчет и представление в виде таблицы распределения количества 
            студентов по профилям вузов для выбранного федерального округа.
            4. Завершение работы с программой''')
        operacia = int(input('\nУкажите цифру нужной операции: '))
    if operacia != 4:
        {1: vivod_soderjimogo,
         2: perechen,
         3: vtor_punkt}.get(operacia)()
    else:
        print('Завершение работы')
        break
