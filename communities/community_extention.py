from community.community import community_class,community_config
from user.user import user_class , bubble_creation
import datetime
from user.user_static import user_static




class community_class_uid(community_class, user_static):
    
    def __init__(self, _uid, _cid):
        user_class.__init__(self, _uid)
        community_class.__init__(self, _cid)
    
    
    def add_community_member(self):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM community_members WHERE cid={0} AND mid={1}".format(self.cid,self.uid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            del_query = "DELETE FROM community_members WHERE cid={0} AND mid={1}".format(self.cid,self.uid)
            cursor.execute(del_query)
        else:
            ins_query = "INSERT INTO community_members (cid,mid) VALUES({0},{1})".format(self.cid,self.uid) 
            cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()  
    
    
    def add_community_request(self):
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d')
        sel_query = "INSERT INTO community_requests(cid,ruid,time) VALUES({0},{1},'{2}')".format(self.cid,self.uid,formatted_date)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        self.conn.commit()
        self.conn.close()
    
        
    def add_community(self,name,bio,country):
        ins_query = "INSERT INTO community (uid,name,bio,country,image) VALUES({0},'{1}','{2}','{3}','')".format(self.uid,name,bio,country)
        cursor = self.conn.cursor()
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
    
    
    
    
    
        


class community_class_bubble_creation(bubble_creation,community_config):
    
    def __init__(self,_uid,_text,_table,_cid):
        bubble_creation.__init__(self,_uid,_text,_table)
        community_config.__init__(self,_cid)
        
    def add_community_bubble(self):
        cursor = self.conn.cursor()
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d %H-%M')
        ins_query = """INSERT INTO {table} (uid,text,timer,type,state,cid) VALUES({id},'{text}','{date}','public',1,{cid})""".format(table=self.table,id=self.uid,text=self.text,date=formatted_date,cid=self.cid)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
        
        
