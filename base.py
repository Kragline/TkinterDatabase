import os
import sqlite3


def start_base():
    """Function creates database"""
    global base, cursor

    base = sqlite3.connect('database.db')
    cursor = base.cursor()

    base.execute('CREATE TABLE IF NOT EXISTS people(name, surname, age)')
    base.commit()


def sql_add(name : str, surname : str, age : str):
    """Function addes new data to database

    Args:
        name (str): name of the person
        surname (str): surname of the person
        age (str): age of the person
    """
    cursor.execute('INSERT INTO people VALUES(?, ?, ?)', (name.capitalize(), surname.capitalize(), age))
    base.commit()


def sql_delete(member_number : int) -> list:
    """Function deletes person from db

    Args:
        member_number (int): Persons ID

    Returns:
        list: persons data
    """
    results = cursor.execute('SELECT * FROM people').fetchall()
    for i in range(len(results)):
        if i == member_number:
            del_name : str = results[i][0]
            del_surname : str = results[i][1]
            del_age : str = results[i][2]

    cursor.execute('DELETE FROM people WHERE name == ? AND surname == ? AND age == ?', (del_name.capitalize(), del_surname.capitalize(), del_age))
    base.commit()
    
    new_list = []
    new_list.append((del_name, del_surname, del_age))

    return new_list


def sql_show() -> list:
    """Function returns all data from db

    Returns:
        list: all data
    """
    results = cursor.execute('SELECT * FROM people').fetchall()
    return results

def delete_base():
    """Function clears db and deletes it"""
    base.execute('DROP TABLE IF EXISTS people')
    base.commit()
    base.close()
    os.remove('database.db')