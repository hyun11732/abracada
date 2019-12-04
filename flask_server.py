from flask import Flask, render_template, request, jsonify, make_response, url_for
from mysqldb import DB
import pandas as pd
import pymongo as pm
app = Flask(__name__)

USER_MODE = False
USER_ID = ""
myclient = pm.MongoClient("mongodb://localhost:27017/")
mydb = myclient["userhistory"]
mycol = mydb["cs411"]

@app.route('/')
def index():
    db = DB()
    temp = url_for('static', filename='style.css')
    return render_template('webpage.html', titles = "search engine")

@app.route('/login', methods=["POST"])
def user() :
    global USER_MODE, USER_ID
    USER_MODE = True
    USER_ID = request.form.get('username')
    print(USER_ID)
    if mycol.find({"_id" : USER_ID}).count() == 0 :
        mycol.insert({"_id" : USER_ID, "field" : [], "author" : []})
    return {'status' : 'success'}


@app.route("/search", methods=["POST"])
def search() :
    value = request.form.get('value')
    by = int(request.form.get('by'))
    db = DB()
    table = pd.DataFrame()
    if by == 0 :
        table = db.search_article_by_id(value)
    elif by == 1 :
        table = db.search_article_by_author(value)
        if USER_MODE :
            newvalues = {"$push": {"author": value}}
            mycol.update({"_id": USER_ID}, newvalues)
    elif by == 2:
        table = db.search_article_by_university(value)
    elif by == 3:
        table = db.search_article_by_title(value)
    elif by == 4 :
        table = db.search_article_by_year(value)
    elif by == 5:
        table = db.search_article_by_journal(value)
    else :
        table = db.search_by_field(value)
        if USER_MODE :
            newvalues = {"$push": {"field": value}}
            mycol.update({"_id": USER_ID}, newvalues)
    if table.empty == True :
        return {"status" : "fail"}
    temp = {"status" : "success", "data" : table.to_html(classes = 'data')}
    return jsonify(temp)

@app.route("/insert", methods=["POST"])
def insert() :
    author = request.form.get('author')
    affiliation = request.form.get('aff')
    citedby = request.form.get('num_citations')
    title = request.form.get('name')
    year = request.form.get('pub_year')
    journal = request.form.get('j_name')
    pub_url = request.form.get('pub_url')
    db = DB()
    result = db.insert_article(author, affiliation, citedby, title, year, pub_url, journal)
    if result == False :
        return jsonify({"status" : "fail"})
    else :
        return jsonify({"status" : "success"})



@app.route("/delete", methods=["POST"])
def delete() :
    value = request.form.get('id')
    db = DB()
    result = db.delete_article_by_id(value)
    if result == False:
        return jsonify({"status": "fail"})
    else:
        return jsonify({"status": "success"})

@app.route("/update", methods=["POST"])
def update() :
    by = int(request.form.get('choice'))
    id = request.form.get('id')
    value = request.form.get('value')
    db = DB()
    result = 0
    if by == 0 :
        result = db.update_article_on_citedby(id, value)
    elif by == 1:
        result = db.update_article_on_puburl(id, value)
    elif by == 2 :
        result = db.update_article_on_journal(id, value)
    if result == False:
        return jsonify({"status": "fail"})
    else:
        return jsonify({"status": "success"})

@app.route("/recom", methods=["POST"])
def recommendation() :
    by = request.form.get("by")
    if USER_MODE :
        temp = mycol.find_one({"_id": USER_ID})
        print(by)
        print(temp)
        db = DB()
        table = pd.DataFrame()
        result = list()
        if by == str(0) : #author
            result = temp["author"]
            name  = max(result, key= result.count)
            print(name)
            table =  db.search_article_by_author(name)
        else :
            result = temp["field"]
            field  = max(result, key= result.count)
            table =  db.search_by_field(field)
        print(table)
        if table.empty :
            return {'status' : 'fail'}
        else :
            return  {"status": "success", "data": table.to_html(classes='data')}
    else :
        return {"status": "fail"}


@app.route("/rank_author", methods=["POST"])
def rank_author() :
    print("sdfdsafsdfdsa")
    db = DB()
    author = db.show_rank_author()
    if len(author) < 3 :
        return jsonify({"status" : "fail"})
    result = {1 : author[0], 2 : author[1], 3 : author[2]}
    return jsonify({"status" : "success", "data" : result})

@app.route("/rank_journal", methods=["POST"])
def rank_journal() :
    print("dsfasdf")
    db = DB()
    journal = db.show_rank_journal()
    print(journal)
    if len(journal) < 3 :
        return jsonify({"status" : "fail"})
    result = {1 : journal[0], 2 : journal[1], 3 : journal[2]}
    return jsonify({"status": "success", "data": result})










if __name__ == '__main__':
    app.run(port=8080, debug=True)