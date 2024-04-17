#! /usr/bin/env python3

import sqlite3
from typing import Any, List, Tuple


class TreatDB():
    def __init__(self, filename: str):
        self.name = filename
        self.con = sqlite3.connect(filename)
        self.table = {}
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        for table in tables:
            cur.execute(f'SELECT * FROM {table[0]}')
            self.table[table[0]] = []
            for description in cur.description:
                self.table[table[0]].append(description[0])

    def __repr__(self):
        tables = ', '.join(self.table.keys())
        return f'TreatDB(file={self.name}, table=({tables}))'

    def add_table(self, name: str, items: List[str]) -> None:
        self.table[name] = items
        cur = self.con.cursor()
        table_items = ", ".join(items)
        cur.execute(f'CREATE TABLE {name}({table_items})')
        self.con.commit()

    def add_data(self, tablename: str, data: List[Tuple[Any]]) -> None:
        if tablename not in self.table:
            print(f'{tablename} not in the table.')
            return
        cur = self.con.cursor()
        ques = ', '.join(['?' for x in range(len(self.table[tablename]))])
        cur.executemany(f'INSERT INTO {tablename} VALUES({ques})', data)
        self.con.commit()

    def close(self):
        self.con.close()


if __name__ == '__main__':
    print('''
from pymeflib.terat_db import TreatDB
db = TreatDB("data_base.db")
db.add_table("table", ["id", "val1", "val2"])
db.add_data("table", [(1, "a", "A")])

db.close()
''')
