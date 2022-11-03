import sqlite3 as sq


'''Обеспечить выбор из списка профиля вуза, интересующего пользователя.

Обеспечить выбор порогового значения отношения числа студентов к числу
преподавателей в вузе, интересующего пользователя (при этом должны быть
подсказки по мин и макс значениям этой величины). 

Составить и отобразить на экране перечень полных наименований вузов, соответствующих
выбранному профилю и имеющих значение указанного отношения ниже
порога.

Обеспечить возможность пользователю выбрать из списка субъект РФ или
значение «Все». 
Для выбранного субъекта РФ рассчитать и представить в
виде таблицы распределение работающих в вузах данного субъекта РФ
преподавателей по наличию ученой степени (доктор наук, кандидат наук, без
степени). 
Таблица должна иметь столбцы: порядковый номер, наличие
ученой степени, количество преподавателей в вузах выбранного субъекта РФ
с данной ученой степенью, процент от общего количества преподавателей в
вузах выбранного субъекта РФ. Последняя строка – итоговая, со значениями:
в столбце «наличие ученой степени» - значение «Все», в столбце «количество
преподавателей» - общее количество преподавателей в вузах выбранного
субъекта РФ.

Помимо функций, приведенных в индивидуальном задании,
программа должна обеспечивать отображение, по выбору пользователя,
каждой из двух таблиц, содержащихся в БД, а также предложение завершить
программу.'''

def otobr(tab_name):
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        tablica = cur.execute(f'SELECT rowid, * FROM {tab_name}')
        [print(*i) for i in tablica]

def perv_punkt(spec):
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        vuz_id = list(cur.execute(f'SELECT codvuz FROM vuzkart WHERE prof == "{spec}"'))
        vuz_id = tuple(j for i in vuz_id for j in i if j)
        data = [list(cur.execute(f'SELECT pps, stud from vuzstat WHERE codvuz == "{id}"')) for id in vuz_id]
        data = filter()

perv_punkt('ИТ')