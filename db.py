import imp
import sqlite3 as sql
from datetime import datetime, date , timedelta
import time 
con = sql.connect('users.db')

with con:
    db = con.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS `users`(
    id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0,
    cash INTEGER DEFAULT 0,
    role INTEGER DEFAULT 0,
    vk_id STRING,
    reg STRING,
    vip_end TEXT
    )""")
    con.commit()

def id_to_str(id):
    if id == 0:
        return "Player"
    elif id == 1:
        return "Admin"
    elif id == 2:
        return "Admin+"
    else:
        return "Error role id"

class UsersInfo:

    def rows():
        db.execute("SELECT COUNT(*) FROM 'users'")
        con.commit()
        values = db.fetchone()
        return int(values[0])

    def is_reg(user_vk_id):
        db.execute(f"SELECT * FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        if values is None:
            return False
        else:
            return True

    def insert(user_vk_id):
        if user_vk_id == 459292228:
            db.execute(f"INSERT INTO 'users' (vk_id,reg,vip_end,role) VALUES (?,?,?,?)", (user_vk_id,str(datetime.now()),"no",2,))
        else:
            db.execute(f"INSERT INTO 'users' (vk_id,reg,vip_end) VALUES (?,?,?)", (user_vk_id,str(datetime.now()),"no",))
       
        con.commit()   

    def get_cash(user_vk_id):
        db.execute(f"SELECT cash FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]
    
    def get_reg(user_vk_id):
        db.execute(f"SELECT reg FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]
        
    def update(user_vk_id, clicks):
        db.execute(f"UPDATE 'users' SET cash = {clicks} WHERE vk_id = {user_vk_id}")
        con.commit()   

    def get_top(count):
        db.execute(f"SELECT vk_id, clicks FROM 'users' ORDER BY cash DESC LIMIT {count}")
        con.commit()
        values = db.fetchall()
        return values 
    
    def is_vip(user_vk_id):
        db.execute(f"SELECT vip_end FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        val1 = db.fetchone()[0]
        now = datetime.now()
        if val1 == "no":
            return False
        else:
            val = datetime.strptime(val1,"%Y-%m-%d %H:%M:%S.%f")
            if now <val :
                return True
            else:
                return False
        
    def get_vip(user_vk_id):
        db.execute(f"SELECT vip_end FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]

    def give_vip(user_vk_id,days_):
        time = str(datetime.now()+ timedelta(days = int(days_)))
        db.execute("UPDATE 'users' SET vip_end = (?) WHERE vk_id = (?)", (time,user_vk_id))
        con.commit() 
        return time 
    
    def get_role(user_vk_id):
        total = id_to_str(db.execute(f"SELECT role FROM 'users' WHERE vk_id= '{user_vk_id}'").fetchone()[0])
        return total
    
    def give_admin(user_vk_id,who):
        if db.execute(f"SELECT role FROM 'users' WHERE vk_id= '{who}'").fetchone()[0] == 2:
            db.execute("UPDATE 'users' SET role = (?) WHERE vk_id = (?)", (1,user_vk_id))
            con.commit()
            return True
        else:
            return False