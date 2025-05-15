from db import mysql_connect
import datetime

class login(mysql_connect):
    def __init__(self,_query):
        mysql_connect.__init__(self)
        self.query = _query
        


    def facebook(self):
        sel_query = "SELECT * FROM users_auth where fid='{0}'".format(self.fid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            return sel_fetch[0][0]
        else:
            return False 

    def phone(self):
        message = {}
        sel_query = "SELECT * FROM users_auth WHERE phoneNubmer='{query}'".format(query=self.query)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) == 0:
            datef = datetime.datetime.now()
            formatted_date = datef.strftime('%Y-%m-%d')
            ins_query = "INSERT INTO users_auth(fid,phoneNubmer,gmail,email,password,notification_token,time,state) VALUES('0','{query}','','','','','{time}',0)".format(query=self.query, time=formatted_date)
            cursor.execute(ins_query)
            uid = cursor.lastrowid
            
            self.conn.commit()
            self.conn.close()
            message.update({'uid': uid, 'state': 'new_user'})
            return message
           
            

        else:
            message.update({'uid': sel_fetch[0][0], 'state': 'current_user'})
            return message
 
    def gmail(self):
        message = {}
        sel_query = "SELECT * FROM users_auth WHERE gmail='{query}'".format(query=self.query)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) == 0:
            datef = datetime.datetime.now()
            formatted_date = datef.strftime('%Y-%m-%d')
            ins_query = "INSERT INTO users_auth(fid,phoneNubmer,gmail,email,password,notification_token,time,state) VALUES('0','','{query}','','','','{time}',0)".format(query=self.query, time=formatted_date)
            cursor.execute(ins_query)
            uid = cursor.lastrowid
            
            self.conn.commit()
            self.conn.close()
            message.update({'uid': uid, 'state': 'new_user'})
            return message
           
            

        else:
            message.update({'uid': sel_fetch[0][0], 'state': 'current_user'})
            return message
    
    
    def uid_of_phone(self):
        message = {}
        sel_query = "SELECT * FROM users_auth WHERE phoneNubmer='{query}'".format(query=self.query)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        if len(fetch_query) != 0:
            
            message.update({'uid': fetch_query[0][0]})
        else:
            message.update({'uid': 'none'})
        return message   

