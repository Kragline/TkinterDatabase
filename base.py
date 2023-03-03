import os
import sqlite3


def start_base():
    global base, cursor

    base = sqlite3.connect('database.db')
    cursor = base.cursor()

    base.execute('CREATE TABLE IF NOT EXISTS people(name, surname, age)')
    base.commit()


def sql_add(name : str, surname : str, age : str):

    cursor.execute('INSERT INTO people VALUES(?, ?, ?)', (name.capitalize(), surname.capitalize(), age))
    base.commit()


def sql_delete(member_number : int):
    results = cursor.execute('SELECT * FROM people').fetchall()
    for i in range(len(results)):
        if i == member_number:
            del_name : str = results[i][0]
            del_surname : str = results[i][1]
            del_age : str = results[i][2]

    cursor.execute('DELETE FROM people WHERE name == ? AND surname == ? AND age == ?', (del_name.capitalize(), del_surname.capitalize(), del_age))
    base.commit()
    
    new_list = []
    new_list.append(del_name)
    new_list.append(del_surname)
    new_list.append(del_age)

    return new_list


def sql_show():
    results = cursor.execute('SELECT * FROM people').fetchall()
    return results

def delete_base():
    base.execute('DROP TABLE IF EXISTS people')
    base.commit()
    base.close()
    os.remove('database.db')