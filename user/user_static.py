from email.mime import image
from db import mysql_connect
import json
import base64
import codecs
import PIL.Image as Image

class user_static(mysql_connect):
    def __init__(self):
        mysql_connect.__init__(self)


    def get_image(self,uid):
        cursor = self.conn.cursor()
        profile_sel_query = "SELECT * FROM users_profile WHERE uid={0}".format(uid)
        cursor.execute(profile_sel_query)
        profile_sel_fetch = cursor.fetchall()
        if len(profile_sel_fetch) != 0:

            try:
                image_profile = codecs.decode(profile_sel_fetch[0][3])
                
                return image_profile
            except:
                return None
            
            
        else:
            return None    

    def get_image2(self,uid):
        cursor = self.conn.cursor()
        profile_sel_query = "SELECT * FROM users_profile WHERE uid={0}".format(uid)
        cursor.execute(profile_sel_query)
        profile_sel_fetch = cursor.fetchall()
        if len(profile_sel_fetch) != 0:
           
            image_profile = codecs.decode(profile_sel_fetch[0][3])
            return image_profile
        else:
            return None  


    def user_any_info(self,uid):
        cursor = self.conn.cursor()
        auth_sel_query = "SELECT * FROM users_auth WHERE uid={0}".format(uid)
        cursor.execute(auth_sel_query)
        auth_sel_fetch = cursor.fetchall()
        user_info = {}
        profile_sel_query = "SELECT * FROM users_profile WHERE uid={0}".format(uid)
        cursor.execute(profile_sel_query)
        profile_sel_fetch = cursor.fetchall()
        
       # base_profile = base64.b64decode(profile_sel_fetch[0][3])
        
       # base_cover = base64.b64decode(profile_sel_fetch[0][4])
        #image_cover = codecs.decode(profile_sel_fetch[0][4])#Image.open(io.BytesIO(base_cover))
        if len(auth_sel_fetch) != 0 and len(profile_sel_fetch) != 0:
            image_profile = codecs.decode(profile_sel_fetch[0][3])#Image.open(io.BytesIO(base_profile))
            user_info['emaill'] =  auth_sel_fetch[0][1]
            user_info['phone_number'] = auth_sel_fetch[0][2]
            user_info['name'] =  profile_sel_fetch[0][1]
            user_info['bio'] = profile_sel_fetch[0][2]
            user_info['image_profile'] = '' 
            user_info['image'] = ''
           # user_info['plus'] = 'true' 
            #user_info['image_cover'] = image_cover
        friends_count_sel_query = "SELECT * FROM friend_requests WHERE from_id={0} OR to_id={1}".format(uid,uid)
        cursor.execute(friends_count_sel_query)
        friends_count_sel_fetch = cursor.fetchall()
        user_info['friends_count'] = len(friends_count_sel_fetch)   
        followers_count_sel_query = "SELECT * FROM follow WHERE gid={0}".format(uid)
        cursor.execute(followers_count_sel_query)
        followers_count_sel_fetch = cursor.fetchall()
        user_info['followers_count'] = len(followers_count_sel_fetch)    
        return user_info
    
    
    def blows_bid(self,uid):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM uses_bubbles_blows WHERE bluid={0}".format(uid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        blows = []
        for i in range(len(sel_fetch)):
            blows.append(sel_fetch[i][1])
        return blows    


    def exctract_bubbles(self,collection):
        bubbles = []
        for i in range(len(collection)):
            for ii in range(len(collection[i]['bubbles'])):
                bubbles.append(collection[i]['bubbles'][ii])
        return bubbles

    def exctract_bubbles_index(self,collection):
        for n in range(len(collection)):
            for nn in range(len(collection) - 1):
                if(collection[nn]['bid'] >= collection[nn + 1]['bid']):
                    temp = collection[nn] #pos 1
                    collection[nn] = collection[nn + 1] #pos2
                    collection[nn + 1] = temp #pos
        return collection  
        
    def users_numbers(self):
        numbers = []
        sel_query = "SELECT * FROM users_auth"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            numbers.append(i[2])
        return numbers    
        
ob = user_static()
fetch = ob.get_image(3)     
print(fetch)
ob = user_static()
fetch = ob.get_image(1)

#ob = user_static()

#print(json.dumps(ob.exctract_bubbles_index()))