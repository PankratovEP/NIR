import sqlite3 as sq
import pandas as pd
from itertools import chain



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
            print(pd.DataFrame(dic_tab).to_markdown(tablefmt='grid'))

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

vtor_punkt()