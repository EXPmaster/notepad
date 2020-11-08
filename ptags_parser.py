import os
import subprocess
import time
import json
import sqlite3
from singleton import Singleton

@Singleton
class Ptags_parser():

    def __init__(self):
        self.json_string = None
        self.json_data = None
        self.conn = None
        self.cursor = None
        self.build_ptags()

    ''''''

    def build_ptags(self):
        if os.path.exists('path.txt'):
            with open('path.txt', 'r') as fr:
                path = fr.readlines()
            self.projectFolderPath = path[0]
            os.chdir(self.projectFolderPath)
            print("Launching ptags on: " + self.projectFolderPath)
            proc = subprocess.Popen(["python", "ptags.py", '-path', self.projectFolderPath],
                                    stdout=subprocess.PIPE, shell=True)
            time.sleep(0.1)
            print("Waiting for ptags to finish")
            time.sleep(0.1)
            self.json_string = (proc.communicate()[0]).decode('utf-8')
            print("")
            print("")

            self.build_ptags_database()

    ''''''

    def build_ptags_database(self):
        self.json_string = self.json_string.replace("}\r\n", "},\r\n")
        self.json_string = "[" + self.json_string + "]"
        self.json_string = self.json_string.replace("},\r\n]", "}\r\n]")

        try:
            self.json_data = json.loads(self.json_string)
        except:
            print("Could not convert json_string to json_data")

        self.conn = sqlite3.connect("tags")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS main
            (def TEXT)
        """)

        for entry in self.json_data:
            self.cursor.execute("""
            INSERT INTO main
            (def)
            VALUES (?)""",
                (   entry["def"] if "def" in entry else None
                )
            )
        ###

    ''''''

    def get_symbol_kind(self, name):
        data = None
        try:
            self.cursor.execute("SELECT name,kind FROM main WHERE name = \"{n}\"".format(n=name))
            data = self.cursor.fetchone()
        except:
            pass

        if data is None:
            return ("", "")
        else:
            return (data[0], data[1])
        ###

    ''''''
            
            
    def where_to_jump(self, name):
        print('name:{}'.format(name))
        try:
            self.cursor.execute("SELECT path,line FROM main WHERE name = \"{n}\"".format(n=name))
            data = self.cursor.fetchone()
        except:
            pass
        
        if data is None:
            return ""
        else:
            return (data[0],data[1])
        ###

    ''''''
            

    def __del__(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
        print("Database closed")

    ''''''

'''=== end Class ==='''
