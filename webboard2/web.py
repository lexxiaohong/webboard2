import os, json
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('story.html')

@app.route('/show_topic/<id_room>')
def show_topic(id_room):
    #print("id_room is",id_room)
    with open('topic_db.json')as k:
        all_topic_data = json.load(k)
    select_data = []
    for row in all_topic_data:
        if row["id_room"] == id_room:
            select_data.append(row)
        
        
    #print("select_data is",select_data)
    return render_template('show_topic.html',select_data = select_data,id_room = id_room)
    
@app.route('/add_topic1/<id_room>')
def add_topic1(id_room):
    return render_template('add_topic_page.html',id_room=id_room)

@app.route('/add_topic2',methods=["POST"])
def add_topic2():
    if request.method == "POST":
        id_room = request.form["id_room"]
        topic = request.form["topic"]
        content = request.form["content"]
    
    with open('topic_db.json')as k:
        all_topic_data = json.load(k)
    if len(all_topic_data) == 0:
        id_latest = "1"
    else :
        last_row = all_topic_data[len(all_topic_data)-1]
        id_latest = int(last_row["id_topic"]) +1
        id_latest = str(id_latest)
        print("type id_latest is",type(id_latest))
    new_data = {
        "id_topic" : id_latest,
        "id_room"  : id_room,
        "topic"    : topic,
        "content"  : content
    }
    #print("new_data ",new_data)
    all_topic_data.append(new_data)
    with open('topic_db.json','w')as k:
        k.write(json.dumps(all_topic_data))
    return redirect('/show_topic/'+id_room)
    
@app.route('/update1/<id_topic>')
def update1(id_topic):
    with open('topic_db.json')as k:
        all_topic_data = json.load(k)
    update_data = {}
    for row in all_topic_data:
        if row["id_topic"] == id_topic:
            update_data = row
    return render_template('update_topic_page.html',update_data=update_data)

@app.route('/update2',methods=["POST"])
def update2():
    if request.method == "POST":
        id_topic = request.form["id_topic"]
        update_topic = request.form["topic"]
        update_content = request.form["content"]
        
    with open('topic_db.json')as k:
         all_topic_data = json.load(k)
    
    for row in all_topic_data:
        if row["id_topic"] == id_topic:
            row["topic"] = update_topic
            row["content"] = update_content
            id_room = row["id_room"]
    with open('topic_db.json','w')as k:
        k.write(json.dumps(all_topic_data))
    
    return redirect('/show_topic/'+id_room)
    
@app.route('/delete_topic/<id_topic>/<id_room>')
def delete(id_topic,id_room):
    with open('topic_db.json')as k:
        all_topic_data = json.load(k)
    new_data = []
    for row in all_topic_data:
        if row["id_topic"] != id_topic:
            new_data.append(row)
    
    #print("new_data is",new_data)
    with open('topic_db.json','w')as k:
        k.write(json.dumps(new_data))
    return redirect('/show_topic/'+id_room)
    
@app.route('/show_comment/<id_topic>')
def show_comment(id_topic):
    with open('topic_db.json')as k:
        all_topic_data = json.load(k)
    select_topic_data = {}
    for row in all_topic_data :
        if row["id_topic"] ==  id_topic:
            select_topic_data = row
    
    #print("select_data is",select_topic_data)
    select_comment_data = []
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    for row in all_comment_data:
        if row["id_topic"] == id_topic:
            select_comment_data.append(row)
    #print("select_comment_data is",select_comment_data)
        
    return render_template('show_comment.html',select_topic_data=select_topic_data,select_comment_data=select_comment_data)
    
@app.route('/insert_comment',methods =["POST"])
def insert_comment():
    if request.method == "POST":
        id_topic = request.form["id_topic"]
        comment = request.form["comment"]
    
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    if len(all_comment_data) == 0:
        id_latest = "1"
    else :
        last_row = all_comment_data[len(all_comment_data)-1]
        id_latest = int(last_row["id_comment"])+1
        id_latest = str(id_latest)
        
    new_comment = {
        "id_comment": id_latest,
        "id_topic" : id_topic,
        "comment": comment
    }
    #print("new_comment ",new_comment)
    all_comment_data.append(new_comment)
    with open('comment_db.json','w')as k:
        k.write(json.dumps(all_comment_data))
        
    return redirect('/show_comment/'+id_topic)
    
@app.route('/update_comment1/<id_comment>')   
def update_comment1(id_comment):
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    select_update_comment_data = {}
    for row in all_comment_data:
        if row["id_comment"]== id_comment:
            select_update_comment_data["id_comment"] = id_comment
            select_update_comment_data["id_topic"] = row["id_topic"]
            select_update_comment_data["comment"] = row["comment"]
    
    return render_template('edit_comment_page.html',select_update_comment_data=select_update_comment_data)
    
@app.route('/update_comment2',methods=["POST"])
def update_comment2():
    if request.method == "POST":
        id_comment = request.form["id_comment"]
        id_topic = request.form["id_topic"]
        update_comment = request.form["comment"]
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    
    for row in all_comment_data :
        if row["id_comment"]== id_comment:
            row["comment"] = update_comment
            
    
    #print("all_comment_data is",all_comment_data)
    with open('comment_db.json','w')as k:
        k.write(json.dumps(all_comment_data))
    
    return redirect('/show_comment/'+id_topic)
    
@app.route('/delete_comment/<id_comment>/<id_topic>')    
def delete_comment(id_comment,id_topic):
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    new_comment_data = []
    for row in all_comment_data:
        if row["id_comment"]!= id_comment:
            new_comment_data.append(row)
    print("new_comment_data is",new_comment_data)    
    
    with open('comment_db.json','w')as k:
        k.write(json.dumps(new_comment_data))
    
    
    return redirect('/show_comment/'+id_topic)
    
    
    
if __name__ == "__main__":
    app.debug = True
    host = os.getenv('IP','0.0.0.0')
    port = os.getenv('PORT','0.0.0.0')
    app.run(host=host, port=port)