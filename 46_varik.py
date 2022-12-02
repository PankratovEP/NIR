import sqlite3 as sq
import pandas as pd


'''Программа должна обеспечивать отображение, по выбору пользователя,
каждой из двух таблиц, содержащихся в БД, а также предложение завершить
программу'''


def otobr():
    tab_name = input('''\nВ базе данных присутствуют 2 таблицы\n"vuzkart"-картотека с записями, содержащими сведения о вузах России.
"vuzstat"- таблица содержащая статистические данные по вузам.
Введите имя таблицы, которую хотите отобразить: ''')
    while tab_name not in ['vuzkart', 'vuzstat']:
        print('\nТаблица не существует! Пожалуйста, повторите попытку.\n')
        tab_name = input('''В базе данных присутствуют 2 таблицы\n"vuzkart"-картотека с записями, содержащими сведения о вузах России.
"vuzstat"- таблица содержащая статистические данные по вузам.
Введите имя таблицы, которую хотите отобразить: ''')
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        tablica = cur.execute(f'SELECT rowid, * FROM {tab_name}')
        [print(*i[1:]) for i in tablica]


'''Обеспечить выбор порогового значения числа аспирантов в вузе, интересу-ющего пользователя 
(при этом должны быть подсказки по мин и макс зна-чениям этой величины). 


Обеспечить возможность выбора пользователем операции отношения (не больше или не меньше).  
В соответствии с выбором пользователя составить и отобразить на экране перечень полных наименований вузов, 
в которых количество аспирантов соотносится с выбранным порогом заданным отношением.  
'''

def perv_punkt():
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()

        kol_aspirants = sorted(list(map(lambda x: x[0], list(cur.execute(f'SELECT asp from vuzstat ')))))
        porog = int(input(f'Введите пороговое значение числа аспирантов в пределах [{max(kol_aspirants)}, {min(kol_aspirants)}]: '))
        while porog < min(kol_aspirants) or porog > max(kol_aspirants):
            porog = int(input(f'Ошибка! Введите пороговое значение числа аспирантов в пределах [{max(kol_aspirants)}, {min(kol_aspirants)}]: '))

        operaciya = int(input('\nВведите число, которое соотвествует желаемой операции:\n1)Не больше\n2)Не меньше\nОперация: '))
        while operaciya not in [1, 2]:
            operaciya = int(input('\nОшибка! Введите число, которое соотвествует желаемой операции:\n1) Не больше\n2)Не меньше\nОперация: '))

        if operaciya == 1:
            vuz_id = list(cur.execute(f'SELECT codvuz FROM vuzstat WHERE asp <= {porog}'))
            vuz_id = tuple([j for i in vuz_id for j in i if j])
        elif operaciya == 2:
            vuz_id = list(cur.execute(f'SELECT codvuz FROM vuzstat WHERE asp >= {porog}'))
            vuz_id = tuple([j for i in vuz_id for j in i if j])

        if len(vuz_id) > 1:
            vivod = list(cur.execute(f'SELECT z1 FROM vuzkart WHERE codvuz IN {vuz_id}'))
        else:
            vivod = list(cur.execute(f'SELECT z1 FROM vuzkart WHERE codvuz == "{vuz_id[0]}"'))

        print(f'\nСписок вузов, где количество аспирантов соотносится с выбранным порогом заданным отношением :\n')
        [print(*i) for i in vivod]


'''Обеспечить возможность пользователю выбрать из списка уровень подготовки студентов: 
бакалавр, специалист, магистр или «Все». 
Рассчитать и представить в виде таблицы распределение количества студентов выбранно-го уровня подготовки по профилям вузов.
 Таблица должна иметь столбцы: порядковый номер, профиль вузов, количество студентов выбранного уров-ня подготовки, 
 процент от общего количества студентов выбранного уровня подготовки. Последняя строка таблицы – итоговая со значениями: 
 в столбце «профиль» - значение «все», в столбце «количество студентов» - общее ко-личество студентов 
 выбранного уровня подготовки.'''


def vtor_punkt():
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        dic_spec = {'бакалавр': 'bac',
                    'специалист': 'spec',
                    'магистр': 'mag',
                    'все': 'stud'}

        dic_tab = {'Порядковый номер': [1, 2, 3, 4, 5],
                   'Профиль вузов': ['ИТ', 'КЛ', 'МП', 'ГП', 'ВСЕ'],
                   'Кол-во студентов выбранного уров-ня подготовки': [],
                   'Процент от общего количества студентов выбранного уровня подготовки': []}

        print('\nВ таблице присутствуют следующие уровни подготовки: бакалавр, специалист, магистр.')
        spec = input('\nВведите желаемый профиль, если хотите выбрать все, то введите "все": ').lower()
        while spec not in dic_spec.keys():
            spec = input('Ошибка! Введите желаемый профиль, если хотите выбрать все, то введите "все": ').lower()

        for vuz_type in dic_tab['Профиль вузов'][:-1]:
            id_s = [i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE prof =="{vuz_type}"')]
            all_studs = sum([i[0] for i in cur.execute(f'SELECT {dic_spec[spec]} FROM vuzstat WHERE codvuz IN {tuple(id_s)}')])
            dic_tab['Кол-во студентов выбранного уров-ня подготовки'].append(all_studs)
        alls = sum(dic_tab['Кол-во студентов выбранного уров-ня подготовки'])
        dic_tab['Кол-во студентов выбранного уров-ня подготовки'].append(alls)
        for k in dic_tab['Кол-во студентов выбранного уров-ня подготовки']:
            dic_tab['Процент от общего количества студентов выбранного уровня подготовки'].append(round(k / alls, 4) * 100)
        print(pd.DataFrame(dic_tab).to_markdown(index=False, tablefmt="grid"))


def vizov(func):
    return {'1': otobr, '2': perv_punkt, '3': vtor_punkt}.get(func)


print('Здравствуйте! Добро пожаловать в программу!')
while True:
    oper = input('''\nВам доступны следующие операции: 
1) Вывести интересующую таблицу на экран
2) Вузы с заданным порогом аспирантов
3) Информация об уровне подготовки студентов по профилям вузов
4) Завершение программы
Пожалуйста, введите номер операции, которую хотите выполнить: ''')
    while oper not in ['1', '2', '3', '4']:
        print('\nОшибка! Такой операции не существует!\n')
        oper = input('''\nВам доступны следующие операции: 
1) Вывести интересующую таблицу на экран
2) Вузы с заданным порогом аспирантов
3) Информация об уровне подготовки студентов по профилям вузов
4) Завершение программы
Пожалуйста, введите номер операции, которую хотите выполнить: ''')
    if oper == '4':
        exit(print("\nДо свидания!"))
    else:
        vizov(oper)()