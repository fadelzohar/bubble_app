import json
#from production import produce
from flask import Flask,request, render_template, make_response, Response
from user import user_class, user_class_bid, user_class_bid_bluid, user_class_fid, frid, reid, requests_not_accepted
from community import community_static, community_class
from community.community_extention import community_class_uid
from user.user_static import user_static
from security_rules import secure_class
from bubble.bubbles import bubble
from user import ml_models
from auth import login
#from auth import facebook_login
import pymysql
from flask_cors import CORS
from waitress import serve
import base64

app = Flask(__name__)
CORS(app)
from flask_socketio import SocketIO,emit

app.config['SECRET_KEY'] = 'ffff111jjj52'
#app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 
socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('note', namespace='/rt')
def notes():
    #bid = msg['bid']
    #obj = bubble(bid)
    #fetch = obj.bubble_config()
    
    #send({'data': fetch['notes']})
    emit('rec', {'data': 'fetch'})
    
    #emit('get_notes', {'data': 'msg'})
def fil():
    return "ji"
def filter_string(strin):
    list_string = strin.split('')
    blocked_symbols = ['>','<','!','/']
    result = [el for el in list_string if el != 't']
    result_string = ''
    for ii in result:
        result_string += ii
    return result_string
    
    
@app.route("/fetch/bubble/subscribers/<bid>", methods=["POST","GET"])
def fetch_bubble_subscribers(bid):
    ob = bubble(bid, {'bubbles':  'user_bubbles', "supscriptions": 'bubbles_supscriptions', 'notes': 'users_bubbles_notes', 'notes_text': 'users_bubbles_notes_text', 'notes_sound': 'users_bubbles_notes_sound', 'bubbles_blows': 'uses_bubbles_blows' })
    fetch = ob.bubble_supscriptions()
    return json.dumps(fetch)

@app.route("/add/subscribtion/<bid>/<uid>", methods=["POST","GET"])
def add_subscripbtion(bid,uid):
    ob = user_class_bid(bid,uid)
    try:
        ob.add_supscription()
        return "sc"
    except:
        return 'str'


@app.route('/fetch/users/phone_numbersfet', methods=["POST","GET"])
def fetch_users_phone_numbers():
    ob = user_static()
    fetch = ob.users_numbers()
    return json.dumps(fetch)
@app.route('/create/account', methods=['POST','GET'])
def create_account():
    if request.method == 'POST':
        return {'name': 'ahmed'}
@app.route('/hint/<uid>', methods=['POST','GET'])
def hint(uid):
    ob = user_class(uid)
    fetch = ob.friends_of_friends_common_explore()
    return json.dumps(fetch)
    
@app.route('/fetch/community/users/<cid>', methods=["POST","GET"])
def fetch_community_users(cid):
    ob = community_class(cid)
    fetch = ob.community_users()
    return json.dumps(fetch)
@app.route('/fetch/user/communties/cids/<uid>', methods=["POST","GET"])
def fetch_user_communities_cids(uid):
    ob = user_class(uid)
    fetch = ob.communities()
    return json.dumps(fetch)
@app.route("/fetch/community/info/<cid>", methods=["POST","GET"])
def fetch_community_info(cid):
    ob = community_class(cid)
    fetch = ob.community_config()
    return json.dumps(fetch)
@app.route('/deug/<cid>/<country>', methods=["POST","GET"])
def debug(cid,country):
    sec_cid = secure_class(uid)
    sec_country = secure_class(country)
    secure_cid = sec_cid.filter_integer()
    secure_country = sec_country.filter_string()
    ob = community_static()
    fetch = ob.communities_country_freq_config(ob.communities_country_freq(ob.communities_country(secure_country)))
    return json.dumps(fetch)
@app.route('/read/user/uid/<phone_number>', methods=['POST', "GET"])
def read_user_uid(phone_number):
    ob = login(phone_number)
    fetch = ob.uid_of_phone()
    return json.dumps(fetch)
@app.route('/det/<uid>', methods=["POST", "GET"])
def det(uid):
    ob = user_class(uid)
    fetch = ob.friends_of_friends_common_explore_card_config(ob.friends_of_friends_common_explore())
    return json.dumps(fetch)
@app.route("/add/community/<uid>/<name>/<bio>/<country>", methods=["POST", "GET"])
def add_community(uid,name,bio,country):
    sec_uid = secure_class(uid)
    sec_bio = secure_class(bio)
    sec_name = secure_class(name)
    sec_country = secure_class(country)
    secure_uid = sec_uid.filter_integer()
    secure_bio = sec_bio.filter_string()
    secure_name = sec_name.filter_string()
    secure_country = sec_counrty.filter_string()
    ob = user_class(secure_uid)
    try:
        ob.add_community(secure_name,secure_bio,secure_country)
        return 'done'
    except:
        return "str"
@app.route('/add/community/member/<uid>/<cid>', methods=["POST","GET"])
def debug3(uid,cid):
    sec_uid = secure_class(uid)
    sec_cid = secure_class(cid)
    secure_uid = sec_uid.filter_integer()
    secure_cid = sec_cid.filter_integer()
    ob = community_class_uid(secure_uid,secure_cid)
    try:
        ob.add_community_member()
        return 'done'
    except:
        return 'str'

@app.route('/add/notification_tokens/<uid>/<token>', methods=["POST","GET"])
def add_notification_tokens(uid,token):
    obj = user_class(uid)
    obj.add_notification_token(token)
    return 'done'
@app.route('/fetch/user/communities/<uid>', methods=["POST", "GET"])
def fetch_user_communities(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.communities()
    return json.dumps(fetch)
@app.route('/fetch/user/communities/config/<uid>', methods=['POST','GET'])
def fetch_user_communities_config(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.communities_config(ob.communities())
    return json.dumps(fetch)
@app.route('/add/community/image/<cid>', methods=["POST","GET"])
def debug2(cid):
    sec = secure_class(uid)
    secure_cid = sec.filter_integer()
    if request.method == 'POST':
        obj = community_class(secure_cid)
        image_url = request.form['photo']
        obj.add_community_image(image_url)
     
        return "done"
     
@app.route('/add/country/<uid>/<country>', methods=["POST", "GET"])
def add_country(uid,country):
    sec_uid = secure_class(uid)
    sec_country = secure_class(country)
    secure_uid = sec_uid.filter_integer()
    ob = user_class(secure_uid)
    secure_country = sec_country.filter_string()
    try:
        ob.add_country(secure_country)
        return "done"
    except: 
        return 'str'
    
  
@app.route("/ry/<uid>", methods=["POST","GET"])
def ry(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.create_bubble_access(ob.bubbles_ids_last_one_time(ob.bubbles_ids_last_one(ob.bubbles_ids())))
    return fetch
@app.route('/add/bubble')
def create_bubble():
    return 'create bubble'

@app.route("/cb/<bid>", methods=["POST","GET"])
def cb(bid):
    sec = secure_class(uid)
    secure_bid = sec.filter_integer()
    ob = bubble(secure_bid)
    fetch = ob.bubbles_noters_repeated_freq_sorted_first_three(ob.bubbles_noters_repeated_freq_sorted(ob.bubbles_noters_repeated_freq(ob.bubbles_noters_repeated())))
    return json.dumps(fetch)
@app.route("/co/<uid>", methods=["POST","GET"])
def co(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.communities_users_bubbles_config(ob.communities_users_bubbles(ob.communities_users(ob.communities())))
    return json.dumps(fetch)
@app.route('/fetch/follow/index', methods=["POST","GET"])
def fetch_follow_index():
    obj = user_class(3)
    fetch = obj.followers_graph_count_index_config()
    if len(fetch) < 7:
        return json.dumps(fetch)
    else:
        return json.dumps(fetch[1:6])
        
@app.route("/fetch/community/<uid>", methods=["POST","GET"])
def fetch_comm(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.communities_users_bubbles_exctract_index(ob.communities_users_bubbles_exctract(ob.communities_users_bubbles(ob.communities_users(ob.communities()))))
    return json.dumps(fetch)
@app.route("/fetch/followers/count/<uid>", methods=["POST","GET"])
def fetch_followers_count(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.followers(secure_uid)
    return json.dumps(fetch)
    
@app.route("/fetch/requests/from/<uid>", methods=["POST","GET"])
def fetch_requests_count(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.requests_from()
    return json.dumps(fetch)   
@app.route("/fetch/requests/to/<uid>", methods=["POST","GET"])
def fetch_requests_to_count(uid):
    ob = user_class(uid)
    fetch = ob.requests_to()
    return json.dumps(fetch)

@app.route('/fetch/user/community/subscribtions/cards/<uid>', methods=["POST","GET"])
def fetch_user_community_subscribtions(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.communities_config(ob.supscription_communities())
    return json.dumps(fetch)
@app.route("/fetch/community/requests/to/<uid>", methods=["POST", "GET"])
def fetch_community_requests_to(uid):
    ob = user_class(uid)
    fetch1 = ob.communities_requests_to(ob.communities())
    ob2 = requests_not_accepted(fetch1, {'table': 'community_requests_accepted', "index": 'crid'})
    fetch2 = ob1.requests_config(ob2.find_requests_not_accepted())
    return json.dumps(fetch2)
    
@app.route("/fetch/community/requests/from/<uid>", methods=["POST", "GET"])
def fetch_community_requests_from(uid):
    ob = user_class(uid)
    fetch1 = ob.communities_requests_from()
    ob2 = requests_not_accepted(fetch1, {'table': 'community_requests_accepted', "index": 'crid'})
    fetch2 = ob1.requests_config(ob2.find_requests_not_accepted())
    return json.dumps(fetch2)
    
@app.route('/fetch/requests/to/uids/<uid>', methods=["POST","GET"])
def fetch_frequests_from_uids(uid):
    obj = user_class(uid)
    fetch = obj.requests_to_ids()
    return json.dumps(fetch)
@app.route("/fetch/friends/uids/<uid>", methods=["POST","GET"])
def fetch_friends_count(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    fetch = ob.friends_uids()
    return json.dumps(fetch)
@app.route('/add/follow/<fid>/<uid>', methods=["GET", "POST"])
def add_follower(fid,uid):
    sec_uid = secure_class(uid)
    sec_fid = secure_class(fid)
    secure_uid = sec_uid.filter_integer()
    secure_fid = sec_fid.filter_integer()
    obj = user_class_fid(secure_uid,secure_fid)
    obj.add_bubble_blow()
    return 'done' 
@app.route('/follow/er/<fid>/<uid>', methods=['POST', "GET"])
def follow_er(uid,fid):
    sec_uid = secure_class(uid)
    sec_fid = secure_class(fid)
    secure_uid = sec_uid.filter_integer()
    secure_fid = sec_fid.filter_integer()
    ob = user_class_fid(int(secure_uid),int(secure_fid))
    ob.add_bubble_blow()
    return 'fid'
    
@app.route('/add/bubble/note/<bid>/<uid>/<note_type>/<sound>/<text>/<nuid>', methods=['POST','GET'])
def add_note(bid,uid,note_type,sound,text,nuid):
    if request.method == 'POST':
        
        sec_uid = secure_class(request.form['uid'])
        sec_bid = secure_class(request.form['bid'])
        sec_nuid = secure_class(request.form['nuid'])
        secure_nuid = sec_nuid.filter_integer()
        secure_uid = sec_uid.filter_integer()
        secure_bid = sec_bid.filter_integer()
        obj = user_class_bid(int(secure_bid),int(secure_uid))
        obj.add_bubble_note(note_type,sound,text,int(secure_nuid))
        return bid
    

@app.route('/add/note/blow/<bid>/<bluid>/<nid>', methods=['POST','GET'])
def add_note_blow(bid,bluid,nid):
    sec_nid = secure_class(nid)
    sec_bid = secure_class(bid)
    sec_bluid = secure_class(bluid)
    secure_bluid = sec_bluid.filter_integer()
    secure_nid = sec_nid.filter_integer()
    get_bubble_class = bubble(secure_bid)
    uid = get_bubble_class.extract_uid_of_bid()
    if uid != 'not_done':
        get_user_bid_bluid_class = user_class_bid_bluid(bid,bluid,uid)
        get_user_bid_bluid_class.add_bubble_note_blow(nid)
        return 'done'
    else: return 'not_ok'    

@app.route('/add/blow/<bid>/<bluid>/<uid>', methods=["POST","GET"])
def add_blow(bid,bluid,uid):
    sec_uid = secure_class(uid)
    sec_bluid = secure_class(bluid)
    sec_bid = secure_class(bid)
    secure_uid = sec_uid.filter_integer()
    secure_bid = sec_bid.filter_integer()
    secure_bluid = sec_bluid.filter_integer()
    ob = user_class_bid_bluid(int(secure_bid),int(secure_bluid),int(secure_uid))
    ob.add_bubble_blow()
    return "done"

@app.route('/fetch/blows/<uid>', methods=['POST','GET'])
def fetch_blows(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_static()
    fetch = ob.blows_bid(secure_uid)
    return json.dumps(fetch)

@app.route('/fetch/cafe/<uid>', methods=["POST","GET"])
def fetch_cafe(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    obj = user_class(secure_uid)
    fetch = obj.friends_of_friends_common_explore_bubbles_exctract_bubbles_index()
    fetch.reverse()
    return json.dumps(fetch)
@app.route('/auth/<fid>')
def auth(fid):
    obj = facebook_login(fid)
    fetch = obj.log()
    if fetch == False:
        return 'notExist'
    else:
        return fetch    
@app.route('/fetch/follow/<uid>', methods=["POST",'GET'])
def fetch_follow(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    try:
        obj = user_class(secure_uid)
        fetch = obj.followers_bubbles_own()
        fetch.reverse()
        if len(fetch) < 7:
            return json.dumps(fetch)
        else:
            
            return json.dumps(fetch[1:7])
    except: 
        return json.dumps([])
    
@app.route('/fetch/library/<uid>',methods=["POST","GET"])
def fetch_library(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    obj = user_class(secure_uid)
    fetch = obj.library()
    fetch.reverse()
    return json.dumps(fetch)
    
@app.route('/fetch/explore/<uid>', methods=["POST", 'GET'])
def fetch_explore(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    try:
        obj = ml_models(secure_uid)
        fetch = obj.naive_render(obj.feature_naive_bayes())
        fetch.reverse()
        if len(fetch) < 7:
            return json.dumps(fetch)
        else:
            
            return json.dumps(fetch[1:7])
    except: 
        return json.dumps([])

@app.route('/fetch/friends/<uid>', methods=['POST','GET'])
def fetch_home(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    ob = user_class(secure_uid)
    try:
        fetch = ob.bubbles_access(ob.friends_bubbles_index())
        
        return json.dumps(fetch) 
    except:
        return 'not valid'    
           
@app.route('/fetch/recommendation/friends')
def fetch_reco():
    return 'fetch'

@app.route('/fetch/notes/<bid>', methods=["POST","GET"])
def fetch_notes(bid):
    sec = secure_class(bid)
    secure_bid = sec.filter_integer()
    obj = bubble(secure_bid)
    fetch = obj.bubble_notes()
    fetch.reverse()
    return json.dumps(fetch)

@app.route('/fetch/notes/blows/<uid>', methods=["POST","GET"])    
def fetch_comments_blows(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    obj = user_class(secure_uid)
    fetch = obj.notes_blows()
    return json.dumps(fetch)

@app.route("/fetch/user/profile/<uid>", methods=["POST","GET"])
def fetch_user_profile(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    obj = user_class(secure_uid)
    fetch = obj.profile()
    return(json.dumps(fetch))    

@app.route('/add_image/<uid>', methods=["POST","GET"])
def add_image(uid):
    sec = secure_class(uid)
    secure_uid = sec.filter_integer()
    if request.method == 'POST':
        
        image_url = request.form['photo']
       
      
        obj = user_class(secure_uid)
        obj.add_image(image_url)
        return json.dumps({'im': image_url})
          
            
        
@app.route("/add/request/<toid>/<fromid>", methods=["POST","GET"])
def add_request(toid,fromid):
    sec_toid = secure_class(toid)
    secure_toid = sec_toid.filter_integer()
    sec_fromid = secure_class(fromid)
    secure_fromid = sec_fromid.filter_integer()
    obj = reid(secure_toid,secure_fromid)
    obj.add_request(obj.check_request())
    return "done"
    
@app.route("/add/request/contact/<toid>/<fromid>", methods=["POST", "GET"])
def add_request_contact(toid,fromid):
    sec_toid = secure_class(toid)
    secure_toid = sec_toid.filter_integer()
    sec_fromid = secure_class(fromid)
    secure_fromid = sec_fromid.filter_integer()
    obj = reid(secure_toid,secure_fromid)
    obj.add_request_contact(obj.check_request())
    return "done"
@app.route('/add/friend/<rid>', methods=["POST","GET"])
def add_friend0(rid):
    sec_rid = secure_class(rid)
    secure_rid = sec_rid.filter_integer()
    obj = frid(secure_rid)
    obj.add_friend()
    return 'done' 
@app.route('/fetch/user/info/<uid>', methods=["POST", "GET"])
def fetch_user_info(uid):
    sec_uid = secure_class(uid)
    secure_toid = sec_uid.filter_integer()
    obj = user_static()
    fetch = obj.user_any_info(secure_toid)
    return json.dumps(fetch)

@app.route('/add/record', methods=['POST','GET'])
def add_record():
    if request.method == "POST":
        file = request.form['photo']
        conn = pymysql.connect(host='localhost',port=8889,user='mamp',password='Mahmoudfadel123',database='db')
        ins = "INSERT INTO img (image) VALUES('{0}')".format(file)
        cursor = conn.cursor()
        cursor.execute(ins)
        conn.commit()
        conn.close()
        return 'done'

@app.route('/trial/<uid>')
def trial(uid):
    obj = bubble(3)
    fetch = obj.bubble_config()['notes']
    return json.dumps(fetch)


@app.route('/auth/phone/<phone_num>', methods=["POST","GET"])
def auth_phone(phone_num):
    sec_phone_num = secure_class(phone_num)
    secure_phone_num = sec_phone_num.filter_string()
    ob = login(secure_phone_num)
    fetch = ob.phone()
    return json.dumps(fetch)

@app.route('/auth/gmail/<gmail>', methods=["POST","GET"])
def auth_gmail(gmail):
    sec_gmail = secure_class(gmail)
    secure_gmail = sec_gmail.filter_integer()
    ob = login(secure_gmail)
    fetch = ob.gmail()
    return json.dumps(fetch)
        
@app.route('/fetch/user/image/<uid>', methods=["POST","GET"])
def fetch_user_image(uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    ob = user_static()
    fetch = ob.get_image(secure_uid)
    
    return json.dumps({'im': fetch})
    
@app.route("/fter/<int:uid>", methods=["POST","GET"])
def fter(uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    ob = user_static()
    fetch = ob.get_image(secure_uid)
    encoded_image = base64.b64encode(fetch).decode('utf-8')
    return Response(encoded_image, content_type='image/png')
@app.route('/frt', methods=["POST","GET"])
def retr():
    return make_response(render_template('index2.html'))
@app.route('/fetch/community/image/<cid>', methods=["POST","GET"])
def fetch_community_image(cid):
    sec_cid = secure_class(cid)
    secure_cid = sec_cid.filter_integer()
    ob = community_class(cid)
    fetch = ob.get_image()
    return json.dumps({"im": fetch})

    #path2 = BytesIO(fetch)
  #  return json.dumps({'im': fetch})#send_file(fetch[0], as_attachment=True,attachment_filename='gh.png')
        
    
@app.route('/create/account/<name>/<bio>/<uid>', methods=['POST',"GET"])    
def add_account(name,bio,uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    sec_name = secure_class(name)
    secure_name = sec_name.filter_string()
    ob = user_class(secure_uid)
    sec_bio = secure_class(bio)
    secure_bio = sec_bio.filter_string()
    ob.add_account(secure_name,secure_bio)
    return "dome"

@app.route('/try_one/<uid>', methods=["POST","GET"])
def try_one(uid):
    obj = user_class(uid)
    fetch = obj.communities_users()
    return json.dumps(fetch)

@app.route('/add/community/request/<uid>/<cid>', methods=["POST","GET"])
def add_community_request(uid,cid):
    obj = community_class_uid(uid,cid)
    obj.add_community_request()
    return json.dumps({'fetch': 'done'})
    
@app.route("/fetch/friends/tokens/<uid>", methods=['POST','GET'])
def fetch_friends_tokens(uid):
    obj = user_class(uid)
    fetch = obj.friends_uids_notification_token(obj.friends_uids())
    return json.dumps(fetch)
    
@app.route('/requester/<uid>', methods=["POST","GET"])
def requester(uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    obj1 = user_class(secure_uid)
    fetch1 = obj1.requests_to()
    obj2 = requests_not_accepted(fetch1, {'table': 'friend_requests_accepts', 'index': 'rid'})
    fetch2 = obj2.find_requests_not_accepted()
    fetch3 = obj1.requests_config(obj1.requests_config(fetch2))
    return json.dumps(fetch3)

@app.route('/fetch/requests/uids/<uid>', methods=["POST","GET"])
def requests_uids(uid):
    obj = user_class(uid)
    fetch = obj.requests_not_accepted_uids(obj.requests_not_accepted(obj.requests_to()))
    return json.dumps(fetch)
@app.route('/requester/count/<uid>', methods=["POST","GET"])
def requester_count(uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    obj = user_class(secure_uid)
    fetch = obj.requests_from()
    return len(fetch)   
    
@app.route('/add/bubble/<uid>/<bubble>', methods=["POST", "GET"])
def add_bubble(uid,bubble):
    if request.method == 'POST':
        bubbles = request.form['bubble']
        obj = bubble_creation(uid,bubbles,'user_bubbles')
        obj.add_bubble()
    return "done"    
    
@app.route('/friends/<uid>', methods=["POST","GET"])
def friends(uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    obj = user_class(secure_uid)
    fetch2 = obj.requests_config(obj.friends())
    return json.dumps(fetch2)   
@app.route('/add/library/<bid>/<uid>', methods=["POST","GET"])
def add_library_breakpiont(bid,uid):
    sec_uid = secure_class(uid)
    secure_uid = sec_uid.filter_integer()
    sec_bid = secure_class(bid)
    secure_bid = sec_bid.filter_integer()
    obj = user_class_bid(int(secure_bid),int(secure_uid))
    obj.add_library()
    return bid
    
@app.route('/add/report/<bid>/<uid>', methods=["POST","GET"])
def add_report(bid,uid):
    obj = user_class_bid(int(bid),int(uid))
    obj.add_report()
    return bid    



if __name__ == "__main__":
    #socketio.run(app,port=7000,debug=True)   
    serve(app,port=7000)


































'''from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return 'hello'
    
if __name__ == "__main__":
    app.run()
    
    
    
#from crypt import methods
from datetime import datetime
import json
from flask import Flask, request
from importlib_metadata import re
#from production import produce
from user import user_class, user_class_bid, user_class_bid_bluid, user_class_fid, frid
from user_static import user_static
from bubbles import *
from user import ml_models
from auth import login
import pymysql
import sys
from flask_cors import CORS ,cross_origin
from waitress import serve
import logging
 
app = Flask(__name__)
 
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
@app.route('/blogs')
def blog():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog"
 
logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return ["Hello!"]
    
from flask_socketio import *
app.config['SECRET_KEY'] = 'ffff11bh1jjj52'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
@socketio.on('notes')
def notes(msg):
    bid = msg['bid']
    obj = bubble(bid)
    fetch = obj.bubble_config()
    join_room(bid)
    #send({'data': fetch['notes']})
    emit('get_notes', {'data': fetch['notes']}, to=bid)
    
    #emit('get_notes', {'data': 'msg'})

@app.route('/create/account/<name>/<bio>/<uid>', methods=['POST','GET'])
def create_account(name,bio,uid):
    obj = user_class(uid)
    obj.add_account(name,bio)
    return 'done'
@app.route('/add/bubble')
def create_bubble():
    return 'create bubble'
@app.route('/fetch/follow/index', methods=["POST","GET"])
def fetch_follow_index():
    obj = user_class(3)
    fetch = obj.followers_graph_count_index_config()
    if len(fetch) < 7:
        return json.dumps(fetch)
    else:
        return json.dumps(fetch[1:6])
    
        
@app.route('/add/bubble/note/<bid>/<uid>/<text>/<nuid>', methods=['POST','GET'])
def add_note(bid,uid,text,nuid):
    obj = user_class_bid(int(bid),int(uid))
    obj.add_bubble_note(text,int(nuid))
    return bid

@app.route('/add/note/blow/<bid>/<bluid>/<nid>', methods=['POST','GET'])
#@cross_origin()
def add_note_blow(bid,bluid,nid):
    get_bubble_class = bubble(bid)
    uid = get_bubble_class.extract_uid_of_bid()
    if uid != 'not_done':
        get_user_bid_bluid_class = user_class_bid_bluid(bid,bluid,uid)
        get_user_bid_bluid_class.add_bubble_note_blow(nid)
        return 'done'
    else: return 'not_ok'    
@app.route('/add/follow/<fid>/<uid>', methods=["GET", "POST"])
def add_follow0(fid,uid):
    obj = user_class_fid(uid,fid)
    obj.add_bubble_blow()
    return "done"
@app.route('/add/blow/<bid>/<bluid>/<uid>', methods=["POST","GET"])
def add_blow(bid,bluid,uid):
    ob = user_class_bid_bluid(bid,bluid,uid)
    ob.add_bubble_blow()
    return "done"

@app.route('/fetch/blows/<uid>', methods=['POST','GET'])
def fetch_blows(uid):
    ob = user_static()
    fetch = ob.blows_bid(uid)
    return json.dumps(fetch)

@app.route('/fetch/cafe/<uid>', methods=["POST","GET"])
def fetch_cafe(uid):
    obj = user_class(uid)
    fetch = obj.friends_of_friends_common_explore_bubbles_exctract_bubbles_index()
    
    return json.dumps(fetch)
    

@app.route('/auth/phone/<query>', methods=["POST","GET"])
def auth_phone(query):
    obj = login(query)
    fetch = obj.phone()
    return json.dumps([fetch])
@app.route('/fetch/follow/<uid>', methods=["POST",'GET'])
def fetch_follow(uid):
    obj = user_class(uid)
    fetch = obj.followers_bubbles_own()
    return json.dumps(fetch)
@app.route('/fetch/library/<uid>',methods=["POST","GET"])
def fetch_library(uid):
    obj = user_class(uid)
    fetch = obj.library()
    fetch2 = fetch[1:6]
    if len(fetch2) < 6:
        return json.dumps(fetch)
    else:
        return json.dumps(fetch2)
    
@app.route('/fetch/explore/<uid>', methods=["POST", 'GET'])
def fetch_explore(uid):
    obj = ml_models(uid)
    fetch = obj.naive_render(obj.feature_naive_bayes())
    fetch2 = fetch[1:6]
    if len(fetch2) < 6:
        return json.dumps(fetch)
    else:
        return json.dumps(fetch2)
   
@app.route('/fetch/friends/<uid>', methods=['POST','GET'])
def fetch_home(uid):
    ob = user_class(uid)
    try:
        fetch = ob.friends_bubbles_index()
        fetch2 = fetch[1:6]
        if len(fetch) < 6:
            return json.dumps(fetch)
        else:
            return json.dumps(fetch2)
    except:
        return 'not valid'    
           
@app.route('/fetch/recommendation/friends')
def fetch_reco():
    return 'fetch'

@app.route('/fetch/notes/<bid>', methods=["POST","GET"])
def fetch_notes(bid):
    obj = bubble(bid)
    fetch = obj.bubble_config()['notes']
    return json.dumps(fetch)

@app.route('/add/bubble/<uid>/<bubble>', methods=["POST", "GET"])
def add_bubble(uid,bubble):
    obj = user_class(uid)
    obj.add_bubble(bubble)
    return "done"
@app.route('/fetch/notes/blows/<uid>', methods=["POST","GET"])    
def fetch_comments_blows(uid):
    obj = user_class(uid)
    fetch = obj.notes_blows()
    return json.dumps(fetch)

@app.route("/fetch/user/profile/<uid>", methods=["POST","GET"])
def fetch_user_profile(uid):
    obj = user_class(uid)
    fetch = obj.profile()
    return(json.dumps(fetch))    


       

@app.route('/fetch/user/info/<uid>', methods=["POST", "GET"])
def fetch_user_info(uid):
    obj = user_static()
    fetch = obj.user_any_info(uid)
    return json.dumps(fetch)


@app.route('/request/<uid>', methods=["POST","GET"])
def request(uid):
    obj = user_class(uid)
    fetch2 = obj.requests_config(obj.requests_from())
    return json.dumps(fetch2)
    
@app.route('/friends/<uid>', methods=["POST","GET"])
def friends(uid):
    obj = user_class(uid)
    fetch2 = obj.friends0()
    return json.dumps(fetch2)    
    
@app.route('/add/friend/<rid>', methods=["POST","GET"])
def add_friend0(rid):
    obj = frid(rid)
    obj.add_friend()
    return 'done' 
    
@app.route('/add/record', methods=['POST','GET'])
def add_record():
    if request.method == "POST":
        file = request.form['photo']
        conn = pymysql.connect(host='localhost',port=8889,user='mamp',password='Mahmoudfadel123',database='db')
        ins = "INSERT INTO img (image) VALUES('{0}')".format(file)
        cursor = conn.cursor()
        cursor.execute(ins)
        conn.commit()
        conn.close()
        return 'done'


@app.route('/fetch/bubble/note/blows/<nid>', methods=["POST","GET"])
def bubble_note_blows(nid):
    obj = bubble_note(nid)
    fetch = obj.notes_blows()
    return json.dumps(fetch)


@app.route('/add/library/<bid>/<uid>', methods=["POST","GET"])
def add_library_breakpiont(bid,uid):
    obj = user_class_bid(int(bid),int(uid))
    obj.add_library()
    return bid



@app.route('/trial/<uid>')
def trial(uid):
    return uid
    obj = bubble(3)
    fetch = obj.bubble_config()['notes']
    return json.dumps(fetch)

@app.route('/')
def index():
    obj = bubble(3)
    fetch = obj.bubble_config()
    return json.dumps(fetch)
    obj = bubble(3)
    fetch = obj.bubble_config()['notes']
    return json.dumps(fetch)


  


    


    



if __name__ == "__main__":
   # app.run(debug=True)
    serve(app,host='184.168.104.3',threads=2,url_prefix='flask-app')   '''     
   