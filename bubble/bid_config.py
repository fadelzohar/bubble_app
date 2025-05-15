from db import mysql_connect

class bid_config(mysql_connect):
    def __init__(self,_bid, _where):
        self.bid = _bid
        self.where = _where
        mysql_connect.__init__(self)

   


class bid_static(mysql_connect):
    def __init__(self):
        mysql_connect.__init__(self)

    def blow_bluids(self,bid):
        bluids = []
        sel_query = "SELECT * FROM uses_bubbles_blows WHERE bid={0}".format(bid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        for i in range(len(sel_fetch)):
            bluids.append(sel_fetch[i][3])
        return bluids  
    
    def blows(self):
        sel_query = "SELECT * FROM uses_bubbles_blows WHERE all_rows=0"
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        return sel_fetch

    def graph_bid_bluid(self):
        graph_bid_bluid = {}
        for i in range(len(self.blows())):
            graph_bid_bluid[self.blows()[i][1]] = self.blow_bluids(self.blows()[i][1])
        return graph_bid_bluid    

    def freq(self,bid):
        sel_query = "SELECT * FROM uses_bubbles_blows WHERE bid={0}".format(bid)
        cursor = self.conn.cursor()
        cursor.execute(sel_query)
        sel_fetch = cursor.fetchall()
        return len(sel_fetch)


class bid_package(bid_config,bid_static):
    def __init__(self,_bid):
        bid_config.__init__(self,_bid)
        bid_static.__init__(self)

#ob = bid_static()
#print(ob.graph_bid_bluid())      