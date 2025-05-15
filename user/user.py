import datetime
from bubble.bubbles import bubble
from user_static import user_static
from bubble.bid_config import bid_static, bid_config, where
from community import community_static, community_class
from utilities import layer_2_utility, layer_1_utility, layer_dic_utility
from db import mysql_connect



class user:
    def __init__(self,_uid):
        self.uid = _uid




class user_bubbles_dependcies(user,where,mysql_connect):
    def __init__(self,_uid,_where):
        user.__init__(self,_uid)
        where.__init__(self,_where)
        mysql_connect.__init__(self)


    def bubbles(self):
        bubbles = []
        sel_query = "SELECT * FROM {table} WHERE uid={id}".format(table=self.where['bubbles'], id=self.uid)
        sel_cursor = self.conn.cursor()
        sel_cursor.execute(sel_query)
        sel_fetch = sel_cursor.fetchall()
        for i in sel_fetch:
            ob = bubble(i[1],self.where)
            bubble_config = ob.bubble_config()
            try:
                
                cid = i[6]
                layer_dic = layer_dic_utility(bubble_config,'cid')
                bubble_config_add_cid = layer_dic.add_cid(cid)
                handle = bubble_config_add_cid
            except:
                handle = bubble_config
                
           
           
            bubbles.append(handle)
        return bubbles
        
        



    
class user_class(user_static,user):
    def __init__(self,_uid):
        user_static.__init__(self)
        user.__init__(self,_uid)
        
    
    def followers(self,id):
        followers = []
        sel_query = "SELECT * FROM follow WHERE gid={0}".format(id)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in  range(len(sel_fetch)):
            followers.append(sel_fetch[i][0])
        return followers    

    def followers_count(self):
        return len(self.followers(self.uid))

    def followers_graph(self):
        followers_graph = []
        sel_query = "SELECT * FROM follow"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        lis = []
        for i in range(len(sel_fetch)):
            if sel_fetch[i][1] in lis:
                continue
            else:
                followers_graph.append(
                    {
                        'uid': sel_fetch[i][1],
                        'count': len(self.followers(sel_fetch[i][1]))
                    })
                lis.append(sel_fetch[i][1])    
        return followers_graph    

    def followers_graph_count(self):
        followers_graph_count = {}
        for i in self.followers_graph():
            count = len(self.followers_graph()[i])
            followers_graph_count.update(
                {
                    i: count
                }
            )
        return followers_graph_count

    def followers_graph_count_index(self,collection):
        for n in range(len(collection)):
            for nn in range(len(collection) - 1):
                if(collection[nn]['count'] <= collection[nn + 1]['count']):
                    temp = collection[nn] #pos 1
                    collection[nn] = collection[nn + 1] #pos2
                    collection[nn + 1] = temp #pos
        return collection
    
    def followers_graph_count_index_config(self):
        followers_graph_count_index_config = self.followers_graph_count_index(self.followers_graph())
        for i in range(len(self.followers_graph_count_index(self.followers_graph()))):
            obj = user_static()
            fetch = obj.user_any_info(self.followers_graph_count_index(self.followers_graph())[i]['uid'])
            followers_graph_count_index_config[i].update(
                {
                    'user': fetch
                }
            )
        return followers_graph_count_index_config    

    def followers_bubbles_own(self):
        bubbles = []
        sel_query = "SELECT * FROM user_bubbles"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in range(len(sel_fetch)):
            own = self.followers(self.uid)
            if sel_fetch[i][0] in own:
                obj = bubble(sel_fetch[i][1], {'bubbles':  'user_bubbles', 'supscriptions': 'bubbles_supscriptions','notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
                bubbles.append(obj.bubble_config())
        return bubbles        

    def requests_to(self):
        requests_to = []
        sel_query = "SELECT * FROM friend_requests WHERE to_id={id}".format(id=self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            arr_in = {'rid': i[0], 'type': 'to', 'uid': i[1]}
            requests_to.append(arr_in)
        return(requests_to)
        
    def requests_to_ids(self):
        requests_ids = []
        sel_query = "SELECT * FROM friend_requests WHERE to_id={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            requests_ids.append(i[1])
        return requests_ids    
     
    def requests_not_accepted(self,_callback):    # _callback maybe requests_from OR requests_to
        requests = []
        for i in _callback:
            sel_query = "SELECT * FROM friend_requests_accepts WHERE rid={0}".format(i['rid'])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) == 0:
                requests.append(i)
        return requests 
        
    def requests_not_accepted_uids(self,_callback): # callback maybe requests_from or _to or communities_requests
        requests_uids = []
        for i in _callback:
            requests_uids.append(i['uid'])
        return requests_uids    
    
    def requests_from(self):
        requests_from = []
        sel_query = "SELECT * FROM friend_requests WHERE from_id={id}".format(id=self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            arr_in = {'rid': i[0], "type": 'from', 'uid':i[2]}
            requests_from.append(arr_in)
        return requests_from

    def requests_from_uid(self,collection):
        arr = []
        for i in collection:
            arr.append(i['uid'])
        return arr    


    def requests_to_and_from(self):
        requests_to_and_from = self.requests_to()
        requests_to_and_from.extend(self.requests_from())
        return requests_to_and_from

    def requests_config(self,collection):   # collection maybe requests_to OR requets_from OR friends
        config = []
        for i in range(len(collection)):
            uid = collection[i]['uid']
            obj = user_static()
            collection[i]['user'] = obj.user_any_info(uid)
            config.append(collection[i])
        return config    
     
     
    def communities_requests_from(self):
        communities_requests_from = []
        sel_query = "SELECT * FROM community_requests WHERE ruid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            for i in sel_fetch:
                arr_in  = {'rid': i[1], "uid": i[2], 'type': 'from'}
                communities_requests_from.append(arr_in)
        return communities_requests_from
    
    
    def communities_requests_to(self,_callback):
        communities_requests_from = []
        for i in _callback:
            sel_query = "SELECT * FROM community_requests WHERE cid={0}".format(i)
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) != 0:
                for i in sel_fetch:
                    arr_in  = {'rid': i[1], "uid": i[2], 'type': 'to'}
                    communities_requests_from.append(arr_in)
        return communities_requests_from
        
        
    def communities_requests_not_accepted(self,_callback):  # callback maybe communities_requests_from or _to
        requests = []
        for i in _callback:
            sel_query = "SELECT * FROM community_requests_accepted WHERE crid={0}".format(i['rid'])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) == 0:
                requests.append(i)
        return requests        
        
        
    def friends_uids(self):
        request_all = self.requests_to_and_from()
        friends = []
        for i in request_all:
            rid = i['rid']
            sel_query = "SELECT * FROM friend_requests_accepts WHERE rid={id}".format(id=rid)    
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) != 0:
                arr_in = i['uid']
                friends.append(arr_in)
            else:
                pass
        return friends
        
    def notification_token(self):
        notification_query = {}
        sel_query = "SELECT * FROM users_auth WHERE uid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0 and sel_fetch[0][6] != '':
            notification_query.update({'notification_token': sel_fetch[0][6]})
        return notification_query
        
    def friends_uids_notification_token(self,_callback):       # _callback maybe friends_uids
        tokens = []
        for i in _callback:
            obj = user_class(i)
            fetch = obj.notification_token()
            if fetch != {}:
                tokens.append(fetch['notification_token'])
        return tokens    
        
    def friends(self):
        request_all = self.requests_to_and_from()
        friends = []
        for i in request_all:
            rid = i['rid']
            sel_query = "SELECT * FROM friend_requests_accepts WHERE rid={id}".format(id=rid)    
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) != 0:
                arr_in = i
                friends.append(arr_in)
            else:
                pass
        return friends  
        
    def add_bubbles(self,collection,where):
        for i in range(len(collection)):
            collection[i]['bubbles'] = []
            sel_query = "SELECT * FROM {table} WHERE {uid}={id}".format(table=where['table']['bubbles'],uid=where['id'],id=collection[i][where['id']])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            for ii in range(len(sel_fetch)):
                bid = sel_fetch[ii][1]
                ob = bubble (bid, where['table'])
                collection[i]['bubbles'].append(ob.bubble_config())
        return collection       

    def friends_bubbles(self):
        friends_bubbles = self.add_bubbles(self.friends(),{'table': {'bubbles': 'user_bubbles', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' }, 'id': 'uid'})
        return friends_bubbles

    def friends_bubbles_index(self):
        obj_layer_1 = layer_1_utility(self.friends_bubbles(),'bubbles')
        bubbles = obj_layer_1.exctract()  
        obj_layer_1 = layer_1_utility(bubbles, 'bid')
        bubbles_remove_repeated = obj_layer_1.remove_repeated()
        obj_layer_1 = layer_1_utility(bubbles_remove_repeated, 'bid')
        bubbles_index =  obj_layer_1.sorting()
        bubbles_index.reverse()
        return bubbles_index
    
    
    def bubbles_access(self,_callback):
        new_str = [i for i in _callback if i['full_time_str'] != 'not valid time1']
        for i in new_str:
            if i['full_time_str'] != 'not valid time1':
                
                obj = time_access(i['full_time_str'])
                obj.set_handle_date()
                obj.set_current_date()
                if obj.bubble_access_current_hour() == False:
                    new_str.remove(i)
            else:
                new_str.remove(i)
        return new_str        
    
    
    def friends_of_friends(self):
        friends = self.friends()
        friends_of_friends = []
        for i in range(0,len(friends)):
            uid = friends[i]['uid'] #i
            user_as_friend = user_class(uid)
            friends_of_friend = user_as_friend.friends()
            nl = []
            for ii in friends_of_friend:
                if ii['uid'] != int(self.uid):
                    nl.append(ii)
            friends[i]['friends'] = nl
        return friends    


    def friends_of_friends_bubbles(self):
        friends_of_friends = self.friends_of_friends()
        for i in range(len(friends_of_friends)):
            for ii in range(len(friends_of_friends[i]['friends'])):
                if friends_of_friends[i]['friends'][ii]['uid'] != self.uid:
                    sel_query = "SELECT * FROM user_bubbles WHERE uid={id}".format(id=friends_of_friends[i]['friends'][ii]['uid'])  
                    cursor = self.conn.cursor()
                    cursor.execute(sel_query)
                    sel_fetch = cursor.fetchall()
                    friends_of_friends[i]['friends'][ii]['bubbles'] = []
                    for n in range(len(sel_fetch)):
                        bubble_ob = bubble(sel_fetch[n][1], {'bubbles':  'user_bubbles','supscriptions': 'bubbles_supscriptions', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
                        friends_of_friends[i]['friends'][ii]['bubbles'].append(bubble_ob.bubble_config())
        return friends_of_friends


    def friends_of_friends_exctract(self):    # exctract friends of friends layer to first layer --layer x
        obj_layer_1 = layer_1_utility(self.friends_of_friends(),'friends')
        friends_of_friends = obj_layer_1.exctract()   
        return friends_of_friends
        
        
    def friends_of_friends_exctract_common(self):   # find how times repeated item layer as freq x,y
        obj_layer_1 = layer_1_utility(self.friends_of_friends_exctract(), 'uid')
        return obj_layer_1.find_frequency()
        
    def friends_of_friends_exctract_common_explore(self):   # sort according to freq --layer x,y,z
        obj_layer_1 = layer_1_utility(self.friends_of_friends_exctract_common(), 'freq')
        friends_of_friends_index =  obj_layer_1.sorting()
        friends_of_friends_index.reverse()
        return friends_of_friends_index
    
    def friends_of_friends_exctract_common_explore_remove_repeated(self):
        obj_layer_1 = layer_1_utility(self.friends_of_friends_exctract_common_explore() ,'uid')
        return obj_layer_1.remove_repeated()
        
    def friends_of_friends_common_explore_card_config(self,_callback):
        config = []
        for i in _callback:
            ob = user_static()
            fetch = ob.user_any_info(i['uid'])
            config.append(fetch)
        return config    
            
    def friends_of_friends_common_explore_bubbles(self):       # set bubbles of friends of friends are most commonned --layer x
        add_bubbles = self.add_bubbles(self.friends_of_friends_exctract_common_explore_remove_repeated(), {'table': {'bubbles': 'user_bubbles', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' }, 'id': 'uid'})
        return add_bubbles
    
    def friends_of_friends_common_explore_bubbles_exctract_bubbles(self):  # extract bubbles as defined in layer x to first layer --layer x+y
        obj_layer_1 = layer_1_utility(self.friends_of_friends_common_explore_bubbles(),'bubbles')
        friends_of_friends = obj_layer_1.exctract()
        return friends_of_friends
    
    def friends_of_friends_common_explore_bubbles_exctract_bubbles_index(self):  # index bubbles according to bids in database --layer x+y+z
        obj_layer_1 = layer_1_utility(self.friends_of_friends_common_explore_bubbles_exctract_bubbles(), 'bid')
        friends_of_friends_index =  obj_layer_1.sorting() 
        return friends_of_friends_index

    def communities(self):
        communities = []
        sel_query = "SELECT * FROM community WHERE uid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in range(len(sel_fetch)):
            communities.append(sel_fetch[i][0])
        return communities    
        
        
    def supscription_communities(self):
        graph = []
        sel_query = "SELECT * FROM community_members WHERE mid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in sel_fetch:
            graph.append(i[0])
        return graph    
        
    def communities_config(self,_callback):
        communities_config = []
        for i in range(len(_callback)):
            obj = community_static()
            fetch = obj.community_card(_callback[i])
            ob = community_class(_callback[i])
            members_count = ob.community_users()
            fetch['members'] = members_count
            communities_config.append(fetch)
        return communities_config    
        
    def communities_users(self,_callback):
        users = []
        for i in range(len(_callback)):
            obj = community_class(_callback[i])
            fetch = obj.community_users()
            users.append({
                'cid': _callback[i],
                'members': fetch
            })
        return users        
    
    def communities_users_bubbles(self,_callback):
        for i in range(len(_callback)):
            users_bubbles = []
            for ii in range(len(_callback[i]['members'])):
                uid = _callback[i]['members'][ii]
                where ={'bubbles':  'community_bubbles', 'supscriptions': 'community_bubbles_supscriptions', 'notes': 'community_bubbles_notes', 'notes_text': 'community_bubbles_notes_text', 'notes_sound': 'community_bubbles_notes_sound', 'bubbles_blows': 'community_bubbles_blows' }
                ob = user_bubbles_dependcies(self.uid,where)
                fetch = ob.bubbles()
                #obj = user_class(uid)
                #fetch = obj.bubbles()
                users_bubbles.append({'uid': uid, 'bubbles': fetch})
            _callback[i]['users_and_their_bubbles'] = users_bubbles    
        return _callback  
        
    def communities_users_bubbles_exctract(self,_callback):
        obj_layer_2 = layer_2_utility(_callback,'users_and_their_bubbles','bubbles')
        bubbles = obj_layer_2.exctract()
        return bubbles
    
    def communities_users_bubbles_exctract_index(self,_callback):
        obj_layer_1 = layer_1_utility(_callback,'bid')
        bubbles_index = obj_layer_1.sorting()
        bubbles_index.reverse()
        return bubbles_index
    
    def communities_users_bubbles_config(self,_callback):
        bubbles_config = []
        for i in _callback:
            ob = bubble(i,  {'bubbles':  'community_bubbles', 'supscriptions': 'community_bubbles_supscriptions', 'notes': 'community_bubbles_notes', 'notes_text': 'community_bubbles_notes_text', 'notes_sound': 'community_bubbles_notes_sound', 'bubbles_blows': 'community_bubbles_blows' })
            bubble_config = ob.bubble_config()
            bubbles_config.append(bubble_config)
        return bubbles_config    
    
    def bubbles_ids(self):
        bubbles = []
        sel_query = "SELECT * FROM user_bubbles WHERE uid={id}".format(id=self.uid)
        sel_cursor = self.conn.cursor()
        sel_cursor.execute(sel_query)
        sel_fetch = sel_cursor.fetchall()
        for i in sel_fetch:
            bubbles.append(i[1])
        return bubbles    
        
    def bubbles_ids_last_one(self,_callback):
        return _callback.pop()
        
    def bubbles_ids_last_one_time(self,_callback):
        sel_query = "SELECT * FROM user_bubbles WHERE bid={0}".format(_callback)
        sel_cursor = self.conn.cursor()
        sel_cursor.execute(sel_query)
        sel_fetch = sel_cursor.fetchall()
        time = sel_fetch[0][3]
        return time
    
    def create_bubble_access(self,_callback):
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d')
        list_now = formatted_date.split("-")
        list_bubble = _callback.split("-")
        day_bubble = list_bubble[2]
        day_now = list_now[2]
        diff = int(day_now) - int(day_bubble)
        if diff == 0:
            return 'not_access'
        else:
            return 'access'
        
      
    
    def library(self):
        library = []
        sel_query = "SELECT * FROM users_library where uid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in  range(len(sel_fetch)):
            obj = bubble(sel_fetch[i][1], {'bubbles':  'user_bubbles','supscriptions': 'bubbles_supscriptions', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
            library.append(obj.bubble_config())
        return library    

    def notes_blows(self):
        notes_blows = []
        sel_query = "SELECT * FROM users_bubbles_notes_blows WHERE bluid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in range(len(sel_fetch)):
            notes_blows.append(sel_fetch[i][2])
        return notes_blows    

    def profile(self):
        profile = self.user_any_info(self.uid)
        profile['bubbles'] = self.bubbles()
        return profile
    
    def add_view(self,vuid):
        cursor = self.conn.cursor()
        ins_query = "INSERT INTO users_views (uid,vuid) VALUES({0},{1})".format(self.uid,vuid)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()

    def add_account(self,name,bio):
        cursor = self.conn.cursor()
        profile_ins_query = "INSERT INTO users_profile (uid,name,bio,image_profile,country,at_name) VALUES({0},'{1}','{2}','','','')".format(self.uid,name,bio)#"UPDATE users_profile SET name='{0}',bio='{1}' WHERE uid={2}".format(name,bio,self.uid)
        cursor.execute(profile_ins_query)
        temp_image_ins_query = "INSERT INTO users_images (uid,image) VALUES({0},'')".format(self.uid)#"UPDATE users_profile SET name='{0}',bio='{1}' WHERE uid={2}".format(name,bio,self.uid)
        cursor.execute(temp_image_ins_query)
        self.conn.commit()
        self.conn.close()

    def add_image(self,image_url):
        cursor = self.conn.cursor()
        ins_query = "UPDATE users_profile SET image_profile='{0}' WHERE uid={1}".format(image_url,self.uid)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()  
        
    def add_country(self,country):
        cursor = self.conn.cursor()
        ins_query = "UPDATE users_profile SET country='{0}' WHERE uid={1}".format(country,self.uid)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()      
        
    def add_notification_token(self,token):
        sel_query = "UPDATE users_auth SET notification_token='{0}' WHERE uid={1}".format(token,self.uid)
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
        
    
        
    def fetch_image(self):
        sel_query = "SELECT * FROM users_images WHERE uid={0}".format(self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        return fetch_query[0][2]



    # community recommendation
    
    def supscription_communities_users(self):
        graph = []
        communities = self.supscription_communities()
        for i in communities:
            obj_community = community_class(i)
            community_users = obj_community.community_users()
            graph.append(
                {
                    "cid": i,
                    'users': community_users
                }
                )
        return graph
    
    
    def communities_users_extend(self):
        new_list = []
        for i in self.supscription_communities_users():
            new_list.extend(i['users'])
        return new_list
    
    
    def communities_users_extend_remove_repeated(self):
        obj_layer_0 = layer_0_utility(self.communities_users_extend())
        return obj_layer_0.remove_repeated()
        
        
    def communities_users_extend_remove_repeated_communities(self):
        graph = []
        for i in self.communities_users_extend_remove_repeated():
            sel_query = "SELECT * FROM community_members WHERE mid={0}".format(i)
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            for ii in sel_fetch:
                graph.append(
                    {
                        'uid': i,
                        'cid': ii[0]
                    }
                    )
        return graph
    
    
    def communities_users_extend_remove_repeated_communities_freq(self):
        obj_layer_1 = layer_1_utility(self.communities_users_extend_remove_repeated_communities(),'cid')
        return obj_layer_1.find_frequency()
    
    def communities_users_extend_remove_repeated_communities_freq_remove_repeated(self):
        obj_layer_1 = layer_1_utility(self.communities_users_extend_remove_repeated_communities_freq(),'cid')
        return obj_layer_1.remove_repeated()
        
    
    def communities_users_extend_remove_repeated_communities_freq_remove_repeated_config(self):
        graph = []
        for i in self.communities_users_extend_remove_repeated_communities_freq_remove_repeated():
            obj_community = community_static()
            card_community = obj_community.community_card(i['cid'])
            graph.append(card_community)
        return graph   
        
    # community recommendation End.
    
    # community home
    
    def supscription_communities_objects(self):
        graph = []
        for i in self.supscription_communities():
            graph.append(
                {
                    'cid': i
                }
                )
        return graph    
    
    def supscription_communities_objects_bubbles(self):
        graph = self.add_bubbles(self.supscription_communities_objects(),{'table': {'bubbles':  'community_bubbles','supscriptions': 'bubbles_supscriptions', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' }, 'id': 'cid'})
        return graph
    
    def supscription_communities_objects_bubbles_exctract_bubbles(self):
        obj_layer_1 = layer_1_utility(self.supscription_communities_objects_bubbles(), 'bubbles')
        graph = obj_layer_1.exctract()
        return graph
        
    def supscription_communities_objects_bubbles_exctract_bubbles_index(self):
        obj_layer_1 = layer_1_utility(self.supscription_communities_objects_bubbles_exctract_bubbles(), 'bid')
        graph = obj_layer_1.sorting()
        return graph
 
 
 









class bubble_creation(user_static):
    def __init__(self,_uid,_text,_table):
        self.text = _text
        self.table = _table
        user_class.__init__(self,_uid)
    
    def add_bubble(self):
        cursor = self.conn.cursor()
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d %H-%M')
        ins_query = """INSERT INTO {table} (uid,text,timer,type,state) VALUES({id},'{text}','{date}','public',1)""".format(table=self.table,id=self.uid,text=self.text,date=formatted_date)
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()           
        
        



 
 
 
 
 
 
 
 
        
class time_access:
    def __init__(self, _handle):
        self.handle = _handle
        self.handle_date = {'date': 'wait for set_handle_date', 'time': 'wait for set_handle_date'}
        self.current_date = {'date': 'wait for set_current_date', 'time': 'wait for set_current_date', 'pm_am': 'wait for set_current_date'}
        
    def set_handle_date(self):
        new_str = self.handle.split(' ')
        self.handle_date['date'] = new_str[0]
        self.handle_date['time'] = new_str[1]
    
    def set_current_date(self):
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d %H-%M %P')
        new_str = formatted_date.split(' ')
        self.current_date['date'] = new_str[0]
        self.current_date['time'] = new_str[1]
        self.current_date['pm_am'] = new_str[2]
        
    
    
        
    def bubble_access_current_hour(self):
        if self.current_date['date'] == self.handle_date['date']:
            current_str = self.current_date['time'].split('-')
            handle_str = self.handle_date['time'].split("-")
            if int(handle_str[0]) == int(current_str[0]):
                return True
            elif int(handle_str[0]) == int(current_str[0]) -  1 and int(current_str[1]) < int(handle_str[1]):
                return True
            else:
                return False
        else: 
            return False
            
        
    
    
    
    
    
    
    
    
class requests_not_accepted(mysql_connect):
    def __init__(self,_requests,_table_config):
        self.requests = _requests
        self.table_config = _table_config
        mysql_connect.__init__(self)
    
    def find_requests_not_accepted(self):
        requests = []
        for i in self.requests:                               # rid -- friend_request
            sel_query = "SELECT * FROM {table_name} WHERE {table_index}={id}".format(table_name=self.table_config['table'],table_index=self.table_config['index'] ,id=i['rid'])
            cursor = self.conn.cursor()
            cursor.execute(sel_query)
            sel_fetch = cursor.fetchall()
            if len(sel_fetch) == 0:
                requests.append(i)
        return requests 
        










class user_class_bid(user_class,bid_config):

    def __init__(self,_bid,_uid):
        bid_config.__init__(self,_bid) 
        user_class.__init__(self,_uid)

    def add_library(self):
        ins_query = """INSERT INTO user_library (uid,bid) VALUES({0},{1})""".format(self.uid,self.bid)
        cursor = self.conn.cursor()
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
    
    def add_report(self):
        ins_query = """INSERT INTO report (bid,uid) VALUES({0},{1})""".format(self.uid,self.bid)
        cursor = self.conn.cursor()
        cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
    
    def add_supscription(self):
        sel_query = "SELECT * FROM bubbles_supscriptions WHERE bid={0} AND suid={1}".format(self.bid,self.uid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) == 0:
            ins_query = "INSERT INTO bubbles_supscriptions(bid,suid) VALUES({0},{1})".format(self.bid,self.uid)
            cursor = self.conn.cursor()
            cursor.execute((ins_query))
        else:
            del_query = "DELETE FROM bubbles_supscriptions WHERE sid={0}".format(sel_fetch[0][1])
            cursor.execute(del_query)
        self.conn.commit()
        self.conn.close()


    def add_bubble_note(self,note_type,sound,text,nuid):
        datef = datetime.datetime.now()
        formatted_date = datef.strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        ins_query = """INSERT INTO users_bubbles_notes (uid,bid,nuid,type,time,state) VALUES({0},{1},{2},'{3}','{4}',0)""".format(self.uid,self.bid,nuid,note_type,formatted_date)          
        cursor.execute(ins_query)
        self.conn.commit()
        last_id = cursor.lastrowid
        if note_type == 'text':
            ins_type_query = """INSERT INTO users_bubbles_notes_text (nid,text) VALUES({0},'{1}')""".format(last_id,text)
            cursor.execute(ins_type_query)
            self.conn.commit()
        else:
            ins_type_query = """INSERT INTO users_bubbles_notes_sound (nid,sound) VALUES({0},'{1}')""".format(last_id,sound)
            cursor.execute(ins_type_query)
            self.conn.commit()
        self.conn.close()       










class user_class_fid(user_class):
    
    def __init__(self,_uid,_fid):
        user_class.__init__(self,_uid)
        self.fid = _fid
        
   
    def add_bubble_blow(self):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM follow WHERE rid={0} AND gid={1}".format(self.fid,self.uid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            del_query = "DELETE FROM follow WHERE rid={0} AND gid={1}".format(self.fid,self.uid)
            cursor.execute(del_query)
        else:
            ins_query = "INSERT INTO follow (rid,gid) VALUES({0},{1})".format(self.fid,self.uid) 
            cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()        










class reid(user_class):
    def __init__(self,_to_id,_uid):
        user_class.__init__(self,_uid)
        self.to_id = _to_id


    def check_request(self):
        sel_query = "SELECT * FROM friend_requests WHERE from_id={0} AND to_id={1}".format(self.uid,self.to_id)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        return fetch_query
        
    def add_request_contact(self,_callback):
        _cursor = self.conn.cursor()
        if len(_callback) == 0:
            ins_query_request = "INSERT INTO friend_requests (from_id,to_id,state) VALUES({0},{1},0)".format(self.uid,self.to_id)
            _cursor.execute(ins_query_request)
            self.conn.commit()
            last_id = _cursor.lastrowid
            ins_query_friend = "INSERT INTO friend_requests_accepts (rid,state) VALUES({0},0)".format(last_id)
            _cursor.execute(ins_query_friend)
            self.conn.commit()
        self.conn.close()
        
        
    def add_request(self,_callback):
        _cursor = self.conn.cursor()
        if len(_callback) != 0:
            rid = _callback[0][0]
            del_query = "DELETE FROM friend_requests WHERE rid={0}".format(rid)
            _cursor.execute(del_query)
        else:
            ins_query = "INSERT INTO friend_requests (from_id,to_id,state) VALUES({0},{1},0)".format(self.uid,self.to_id)
            _cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()
           
           
           
           
           
           
           
           
           
           
            

class frid(user_static):
    
    def __init__(self,_frid):
        
        user_static.__init__(self)
        self.fid = _frid
        
   
    def add_friend(self):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM friend_requests_accepts WHERE rid={0}".format(self.fid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            del_query_request_accepts = "DELETE FROM friend_requests_accepts WHERE rid={0}".format(self.fid)
            cursor.execute(del_query_request_accepts)
            #del_query_request = "DELETE FROM friend_requests WHERE rid={0}".format(self.fid)
            #cursor.execute(del_query_request)
        else:
            ins_query = "INSERT INTO friend_requests_accepts (rid,state) VALUES({0},0)".format(self.fid) 
            cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()        












class user_class_bid_bluid(user_class_bid):

    def __init__(self,_bid,_bluid,_uid):
        self.bluid = _bluid  
        user_class_bid.__init__(self,_bid,_uid)


    def add_bubble_note_blow(self,nid):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM users_bubbles_notes_blows WHERE nid={0} AND bluid={1}".format(nid,self.bluid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch) != 0:
            del_query = "DELETE FROM users_bubbles_notes_blows WHERE blid={0}".format(sel_fetch[0][3])
            cursor.execute(del_query)
        else:
            ins_query = "INSERT INTO users_bubbles_notes_blows (uid,bid,nid,bluid) VALUES({0},{1},{2},{3})".format(self.uid,self.bid,nid,self.bluid)
            cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()       


    def add_bubble_blow(self):
        cursor = self.conn.cursor()
        sel_query = "SELECT * FROM uses_bubbles_blows WHERE bid={0} AND bluid={1}".format(self.bid,self.bluid)
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        if len(sel_fetch)  != 0:
            del_query = "DELETE FROM uses_bubbles_blows WHERE bid={0} AND bluid={1}".format(self.bid,self.bluid)
            cursor.execute(del_query)
        else:
            ins_query = "INSERT INTO uses_bubbles_blows (uid,bid,bluid,all_rows) VALUES({0},{1},{2},0)".format(self.uid,self.bid,self.bluid) 
            cursor.execute(ins_query)
        self.conn.commit()
        self.conn.close()    













class ml_models(user_class,bid_static,bubble):

    def __init__(self,_uid):
        user_class.__init__(self,_uid)
        bid_static.__init__(self)

 # naive bayes algorithm start

    # finding y start
    def bubbles_blows_others_bluid(self):  # {bid, bluid}
        blows_tree = {}
        sel_query = "SELECT * from uses_bubbles_blows"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in range(len(sel_fetch)):
            sel_bubble_query = "SELECT * FROM user_bubbles WHERE bid={0}".format(sel_fetch[i][1])
            cursor_bubble = self.conn.cursor()
            cursor_bubble.execute(sel_bubble_query)
            sel_bubble_fetch = cursor_bubble.fetchall()
            if len(sel_bubble_fetch) != 0 and sel_fetch[i][1] in self.blows_bid(self.uid) and sel_fetch[i][3] != self.uid and sel_bubble_fetch[0][4] == 'public':
                try:
                    blows_tree[sel_fetch[i][1]].append(sel_fetch[i][3])
                except:
                    blows_tree[sel_fetch[i][1]] = []
                    blows_tree[sel_fetch[i][1]].append(sel_fetch[i][3])
        return blows_tree  
    

    def bubbles_blows_others_collect(self): # [bluid]
        freq = []
        for i in self.bubbles_blows_others_bluid():
            for ii in range(len(self.bubbles_blows_others_bluid())):
                for i_plus in self.bubbles_blows_others_bluid():
                    if self.bubbles_blows_others_bluid()[i][ii] in self.bubbles_blows_others_bluid()[i_plus]:
                        if self.bubbles_blows_others_bluid()[i][ii] in freq:
                            pass
                        else:
                            freq.append(self.bubbles_blows_others_bluid()[i][ii])
        return freq


    def x_intercept_y(self):
        feature_naive_bayes = {}
        for i in self.graph_bid_bluid():
            for ii in range(len(self.graph_bid_bluid()[i])):
                for n in self.bubbles_blows_others_bluid():
                    if self.graph_bid_bluid()[i][ii] in self.bubbles_blows_others_bluid()[n] and i <= n:
                        try:
                            feature_naive_bayes[i] += 1
                        except:
                            feature_naive_bayes[i] = 0
                            feature_naive_bayes[i] += 1    
        return feature_naive_bayes                        


    def y_count(self):
        return len(self.bubbles_blows_others_collect())


    def feature_naive_bayes(self):
        feature_naive_bayes = {}
        #sorted_result = None
        for i in self.x_intercept_y():
            x_intercept_y = self.x_intercept_y()[i]
            y_count = self.y_count()
            y_probability = self.y_probility()
            x_probability = self.freq(i)
            naive_bayes = ((x_intercept_y / y_count) * y_probability) / x_probability
            feature_naive_bayes[i] = naive_bayes
            sorted_result = {k:v for k,v in sorted(feature_naive_bayes.items())}
        return sorted_result    

    
    def naive_render(self,vector):
        res = []
        for k in vector:
            obj = bubble(k, {'bubbles':  'user_bubbles', 'supscriptions': 'bubbles_supscriptions','notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
            res.append(obj.bubble_config())
        return res    


   # def y_conf_x(self):
   

    # find y end

    # find p(y) start
    def all_blows_count(self):
        sel_query = "SELECT * FROM uses_bubbles_blows"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        return len(sel_fetch)    


    def y_probility(self):
        y_probility = len(self.bubbles_blows_others_collect()) / self.all_blows_count()
        return y_probility

   # def x_probability(self):

    # find p(y) end    
        
  # find xs intercept y start
    # find x intercept y start 
li = {'table': {'bubbles':  'community_bubbles', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' }, 'id': 'uid'}
print(li['table']['bubbles'])
where1 = {'bubbles':  'community_bubbles', 'supscriptions': 'community_bubbles_supscriptions', 'notes': 'community_bubbles_notes', 'notes_text': 'community_bubbles_notes_text', 'notes_sound': 'community_bubbles_notes_sound', 'bubbles_blows': 'community_bubbles_blows' }
ob = user_class(1)
fetch = ob.communities_users_bubbles_exctract_index(ob.communities_users_bubbles_exctract(ob.communities_users_bubbles(ob.communities_users(ob.communities()))))
#fetch = ob.bubbles()

print(fetch)
#print([i for i in ob.friends_bubbles_index() if i['bid'] == 38])
obj = time_access('2023-02-21 4-41')
obj.set_handle_date()
obj.set_current_date()
print(obj.current_date)
