from db import mysql_connect
from user.user_static import user_static
import codecs



class community_config:
    def __init__(self, _cid):
        self.cid = _cid

class community_static(mysql_connect):
    def __init__(self):
        mysql_connect.__init__(self)
        
    
    
    def community_card(self, cid):
        card = {}
        cursor = self.conn.cursor()
        profile_sel_query = "SELECT * FROM community WHERE cid={0}".format(cid)
        cursor.execute(profile_sel_query)
        profile_sel_fetch = cursor.fetchall()
        if len(profile_sel_fetch) != 0:
            
            card.update({
            'name': profile_sel_fetch[0][2],
            'uid': profile_sel_fetch[0][1],
            'cid': profile_sel_fetch[0][0],
            'bio': profile_sel_fetch[0][3],
            'image': ''
            
        })
        
        return card
        
    def communities_country(self,country):
        communities = []
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM community WHERE country='{0}'".format(country)
        
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        for i in fetch_query:
            communities.append(i[0])
        return communities 
        
    def communities_country_freq(self,_callback):
        communities_freq = {}
        for i in _callback:
            sel_query = "SELECT * FROM community_members WHERE cid={0}".format(i)
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            fetch_query = cursor.fetchall()
            communities_freq.update({
                i: len(fetch_query)
            })
       # sorted(communities_freq.items(), key=lambda item: item[1])   
        sorted_result = {k: v for k, v in sorted(communities_freq.items(), key=lambda item: item[1])}

       # res = dict(reversed(list(sorted_communities_freq.items())))
        return sorted_result    
        
    def communities_country_freq_config(self, _callback):
        arr = []
        for i in _callback:
            card = self.community_card(i)
            card.update({
                'members_count': _callback[i]
            })
            arr.append(card)
        return arr 
    


class community_class(community_static):
    def __init__(self, _cid):
        community_static.__init__(self)
        community_config.__init__(self, _cid)

    
    def community_config(self):
        config  = {}
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM community WHERE cid={0}".format(self.cid)
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        if len(fetch_query) != 0:
            ob = community_static()
            fetch = ob.community_card(fetch_query[0][0])
        return fetch
        
    def add_community_image(self,image_url):
        cursor = self.conn.cursor()
        ins_query = "UPDATE community SET image='{0}' WHERE cid={1}".format(image_url,self.cid)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
        return 'done'
        
        
    def community_users(self):
        members = []
        sel_query = "SELECT * FROM community_members WHERE cid={0}".format(self.cid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        if len(fetch_query) != 0:
            for i in fetch_query:
                members.append(i[1])
        return members        
        
    
    def get_image(self):
        cursor = self.conn.cursor()
        profile_sel_query = "SELECT * FROM community WHERE cid={0}".format(self.cid)
        cursor.execute(profile_sel_query)
        profile_sel_fetch = cursor.fetchall()
        if len(profile_sel_fetch) != 0:

            
            image_profile = codecs.decode(profile_sel_fetch[0][5])
            return image_profile
        else:
            return None   
          
            
    def community_requests(self):
        request = []
        sel_query = "SELECT * FROM community_requests WHERE cid={0}".format(self.cid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            request.append({'crid': i[1], 'cid': i[0]})
        return request


    def community_requests_accepted(self,_callback):     # callback maybe community_requests
        for i in _callback:
            sel_query = "SELECT * FROM community_requests_accepted WHERE crid={0}".format(i['crid'])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) != 0:
                index_of_i = _callback.index(i)
                _callback[index_of_i].update({'caid': sel_fetch[0][1]})
            else:
                _callback.remove(i)
        return _callback        
        
        
    def community_requests_not_accepted(self,_callback): # callback maybe community_requests
        for i in _callback:
            sel_query = "SELECT * FROM community_requests_accepted WHERE crid={0}".format(i['crid'])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) != 0:
                _callback.remove(i)
            else:
                pass
        return _callback  
        
        
        
class request_config(mysql_connect):                                   # a visitor class to handle request configs in community_class
    def __init__(self, _request):
        self.request = _request
        mysql_connect.__init__(self)
        
    def config(self):
        for i in self.request:
            ruid = i['crid']
            user_sel_query = "SELECT * FROM community WHERE cid={0}".format(i['cid'])
            user_cursor = self.conn.cursor()
            user_cursor.execute(user_sel_query)
            user_sel_fetch = user_cursor.fetchall()
            if user_sel_fetch != 0:
                uid = user_sel_fetch[0][1]
                obj = user_static()
                user_config = obj.user_any_info(uid)
                requester_config = obj.user_any_info(ruid)
                index_of_i = self.request.index(i)
                self.request[index_of_i].update({'uid': uid, 'user_config': user_config, 'requester_config': requester_config})  
        return self.request       
                    
                
            
        

ob = community_class(3)
fetch0 = ob.community_requests_not_accepted(ob.community_requests())
obj = request_config(fetch0)
print(obj.config())

obj0 = community_class(3)
fetch0 = obj0.community_requests_accepted(obj0.community_requests())
obj = request_config(fetch0)
fetch = obj.config()
print(fetch)
      
ob = community_static()
print(ob.community_card(3))
print(3)
        