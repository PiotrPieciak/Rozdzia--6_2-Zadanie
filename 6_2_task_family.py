# Program family ma za zadanie utworzyć bazę danych w pliky family.db stworzyć 2 tabele i wypełnić je danymi poszczególnych członków rodziny oraz ich obowiazkami
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_member(conn, member):
    """
    Create a new project into the members table
    :param conn:
    :param member:
    :return: member id
    """
    sql = '''INSERT INTO members(name, surname, sex, birth_date) 
    VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, member)
    conn.commit()
    return cur.lastrowid

def add_duty(conn, task):
    """
    Create a new task into the tasks table
    :param conn:
    :param task:
    :return:
    """
    sql = '''INSERT INTO tasks(duty_id, duty_name, duty_description, day_of_week_to_complete) 
    VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def update(conn, table, id, **kwargs):
    """
    update status, day_of_week_to_complete  of a duty
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )
    sql = f''' UPDATE {table} SET {parameters} WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except sqlite3.OperationalError as e:
        print(e)

def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn: Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

if __name__ == "__main__":
#stworzenie tabeli members
    create_members_sql = """
    -- family members table
    CREATE TABLE IF NOT EXISTS members (
        id integer PRIMARY KEY,
        name text NOT NULL,
        surname text NOT NULL,
        sex text NOT NULL,
        birth_date text NOT NULL
    );
    """
#stworzenie tabeli resposibilities
    create_responsibilities_sql = """
    -- responsibilities table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        duty_id integer NOT NULL,
        duty_name text NOT NULL,
        duty_description text NOT NULL,
        day_of_week_to_complete text NOT NULL,
        FOREIGN KEY (duty_id) REFERENCES members (id)
    );
    """
#Nawiązanie połaczenia z bazą danych i utworzenie 2 tabeli
    db_file = "family.db"
    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_members_sql)
        execute_sql(conn, create_responsibilities_sql)

#_______________dodanie pierwszej osoby______________
    member = ("Piotr", "Pieciak", "male", "01-01-1984")
    mb_id = add_member(conn, member)
    duty = (
        mb_id,
        "Weekly shopping",
        "Once per week go to supermarket to buy needed items",
        "saturday"
    )
    add_duty(conn, duty)
#_______________dodanie drugiej osoby i obowiązków______________
    member = ("Dorota", "Pieciak", "female", "01-01-1984")
    mb_id = add_member(conn, member)
    duty = (
        mb_id,
        "Cooking",
        "Cooking for whole family 3 times in week",
        "monday, wednesday, friday"
    )
    add_duty(conn, duty)
#_______________dodanie trzeciej osoby i obowiązków______________
    member = ("Rafal", "Pieciak", "male", "01-01-2015")
    mb_id = add_member(conn, member)
    duty = (
        mb_id,
        "Clean room",
        "before bedtime room must be cleaned, all items must be place, in order",
        "each day"
    )
    add_duty(conn, duty)  
#_______________dodanie czwartej osoby i obowiązków______________
    member = ("Natalia", "Pieciak", "female", "01-01-2023")
    mb_id = add_member(conn, member)
    duty = (
        mb_id,
        "Eat and look sweet",
        "Primary task for 2year old is to eat and be awsome, look sweet",
        "all week long"
    )
    add_duty(conn, duty)

#_______ Zaznaczenie i wydrukowanie wszystkich rzędów z tabeli members
    cur = conn.cursor()
    cur.execute("SELECT * FROM members")
    rows = cur.fetchall()
    print(rows)
#___________update danych z tabeli_______________
    update(conn, "tasks", 1, day_of_week_to_complete="FRIDAY")
#____________usuwanie wpisu (Rafałek wchodzi w fazę buntu nastolatka)_____________
    delete_where(conn, "tasks", id=3)
#__________Zakonczenie programu_____________
    print("Program stworzył bazę danych i nawiązał połączenie, stworzył 2 tabele i  dodał do nich wpisy, następnie zaznaczył i wydrukował wszytskie wiersze w tabeli members, Zrobił update na danych a na końcu usunał zadanie przypisane do Rafała (gdy zaczyna wchodzić w fazę buntu nastolatka)")
    conn.commit()
    conn.close()