from user.user_static import user_static
from db import mysql_connect
from bubble.bid_config import bid_config


class bubble(bid_config):
    def __init__(self,_bid, _where):
        bid_config.__init__(self,_bid,_where)

    def bubble_config(self):
        bubble = {}
        bubble_sel_query = "SELECT * FROM {table} WHERE bid={id}".format(table=self.where['bubbles'],id=self.bid)
        bubble_cursor = self.conn.cursor()
        bubble_cursor.execute(bubble_sel_query)
        bubble_sel = bubble_cursor.fetchall()
        user_info = None
        if len(bubble_sel) != 0:
            time_db = bubble_sel[0][3]
            time = {}
            full_time_str = ''
            try:
                time_db_split = time_db.split(' ')
                if len(time_db_split) == 2:
                    
                    full_time_str = time_db
                    time_split_date = time_db_split[0].split('-')
                    time.update(
                        
                        {
                            
                            'year': time_split_date[0],
                            'month': time_split_date[1],
                            'day': time_split_date[2]
                        }
                    )
                else:
                    time = 'not valid time1'  
                    full_time_str = 'not valid time1'
            except: 
                time = 'not valid time1'
                full_time_str = 'not valid time1'
            ob = user_static()
            user_info = ob.user_any_info(bubble_sel[0][0])
            bubble.update({
                'uid': user_info,
                'bid': bubble_sel[0][1],
                'uid': bubble_sel[0][0],
                'text': bubble_sel[0][2],
                'time': time,
                'full_time_str': full_time_str,
                'user': user_info,
                'most_interacted': {
                    'images': [],
                    'uids': self.bubbles_noters_repeated_freq_sorted_first_three(self.bubbles_noters_repeated_freq_sorted(self.bubbles_noters_repeated_freq(self.bubbles_noters_repeated())))
                }
                
            })
            
            bubble['blow_count'] = len(self.bubble_blows())
            bubble['blows'] = self.bubble_blows()
            bubble['notes'] = self.bubble_notes()
            
        return bubble

    
    def bubble_blows(self):
        blows = []
        bubble_blows_query = "SELECT * FROM {table} WHERE bid={id}".format(table=self.where['bubbles_blows'],id=self.bid)
        bubble_blows_cursor = self.conn.cursor()
        bubble_blows_cursor.execute(bubble_blows_query)
        bubble_blows_sel = bubble_blows_cursor.fetchall()
        for e in range(len(bubble_blows_sel)):
              blows.append({
                'blid': bubble_blows_sel[e][2],
                'bluid': bubble_blows_sel[e][3]
            })
        return blows    
    
    
    def bubble_notes(self):
        bubble_notes_sel_query = "SELECT * FROM {table} WHERE bid={id}".format(table=self.where['notes'],id= self.bid)
        bubble_notes_cursor = self.conn.cursor()
        bubble_notes_cursor.execute(bubble_notes_sel_query)
        bubble_notes_sel = bubble_notes_cursor.fetchall()
        notes = []
        for ee in range(len(bubble_notes_sel)):
            user_tag = user_static()
            time_db = bubble_notes_sel[ee][5]
            time_db_split = time_db.split('-')
            time = {}
            if len(time_db_split) == 3:
                time.update(
                    {
                        'year': time_db_split[0],
                        'month': time_db_split[1],
                        'day': time_db_split[2]
                    }
                )
            else:
                time = 'not valid time' 
            obj = bubble_note(bubble_notes_sel[ee][2])
            note_type = bubble_notes_sel[ee][4]
            content = ''
            if note_type == 'text':
                sel_type_query = "SELECT * FROM {table} WHERE nid={id}".format(table=self.where['notes_text'],id=bubble_notes_sel[ee][2])
                bubble_notes_cursor.execute(sel_type_query)
                sel_type_fetch = bubble_notes_cursor.fetchall()
                if len(sel_type_fetch) != 0:
                    content = sel_type_fetch[0][2]
            elif note_type == 'sound':
                sel_type_query = "SELECT * FROM {table} WHERE nid={id}".format(table=self.where['notes_sound'],id=bubble_notes_sel[ee][2])
                bubble_notes_cursor.execute(sel_type_query)
                sel_type_fetch = bubble_notes_cursor.fetchall()
                if len(sel_type_fetch) != 0:
                    content = sel_type_fetch[0][2]
                    
            blows = obj.notes_blows()    
            notes.append({
            'nid': bubble_notes_sel[ee][2],
            'nuid': bubble_notes_sel[ee][3],
            'user_tag': user_tag.user_any_info(bubble_notes_sel[ee][3]),
            'content': content,
            'time': time,
            'blows': blows,
            'type': note_type,
            
            })
        return notes    

    def extract_uid_of_bid(self):
        sel_query = "SELECT * FROM {table} WHERE bid={id}".format(table=self.where['bubbles'],id=self.bid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()  
        if len(sel_fetch) != 0:
            return sel_fetch[0][0]
        else:
            return 'not_done'    

    def bubbles_noters_repeated(self):
        noters = []
        sel_query = "SELECT * FROM {table} WHERE bid={id}".format(table=self.where['notes'],id=self.bid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        fetch_query = cursor.fetchall()
        for i in fetch_query:
            noters.append(i[3])
        return noters    
    
    def bubbles_noters_repeated_freq(self,_callback):
        freq = {}
        for i in _callback:
            if i not in freq.keys():
                freq[i] = _callback.count(i)
        return freq        
            
    def bubbles_noters_repeated_freq_sorted(self,_callback):
        
        sorted_values = sorted(_callback.values()) # Sort the values
        sorted_dict = {}
        for i in sorted_values:
            for k in _callback.keys():
                if _callback[k] == i:
                    sorted_dict[k] = _callback[k]

        reversed_sorted_dict =dict(reversed(list(sorted_dict.items())))
        return reversed_sorted_dict

    def bubbles_noters_repeated_freq_sorted_first_three(self,_callback):
        keys_list = list(_callback.keys())
        highest_noters = []
        for i in range(3):
            try:
                highest_noters.append(keys_list[i])
            except: 
                continue
                
            
            
        return highest_noters    
            


class bubble_note(mysql_connect):
    def __init__(self,nid):
        self.nid = nid
        mysql_connect.__init__(self)
       

    def notes_blows(self):
        sel_query = "SELECT * FROM users_bubbles_notes_blows WHERE nid={nid}".format(nid=self.nid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        blows_count = len(sel_fetch)
        return blows_count



ob = bubble(3, {'bubbles':  'user_bubbles', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
print(ob.bubble_notes())