from flask import Flask, render_template, request, jsonify, make_response, url_for
from mysqldb import DB
import pandas as pd
app = Flask(__name__)

user_history = dict()

@app.route('/')
def index():
    db = DB()
    temp = url_for('static', filename='style.css')
    return render_template('webpage.html', titles = "search engine")

@app.route("/search", methods=["POST"])
def search() :
    value = request.form.get('value')
    by = int(request.form.get('by'))
    print(value, by)
    db = DB()
    table = pd.DataFrame()
    if by == 0 :
        table = db.search_article_by_id(value)
        print(table)
    elif by == 1 :
        table = db.search_article_by_author(value)
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
        print(table.shape)
    if table.empty == True :
        return {"status" : "fail"}
    temp = {"status" : "success", "data" : table.to_html(classes = 'data')}
    return jsonify(temp)

@app.route("/insert", methods=["POST"])
def insert() :
    author = request.form.get('author')
    affiliation = request.form.get('affiliation')
    citedby = request.form.get('citedby')
    title = request.form.get('pub_title')
    year = request.form.get('pub_year')
    journal = request.form.get('journal')
    db = DB()
    result = db.insert_article(author, affiliation, citedby, title, year, journal)
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
    by = request.form.get('by')
    id = request.form.get('id')
    value = request.form.get('value')
    db = DB()
    result = 0
    if by == 1 :
        result = db.update_article_on_citedby(id, value)
    elif by == 2:
        result = db.update_article_on_puburl(id, value)
    else :
        result = db.update_article_on_journal(id, value)
    if result == False:
        return jsonify({"status": "fail"})
    else:
        return jsonify({"status": "success"})

'''
@app.route("/recom", methods=["POST"])
def recommendation() :
    by = request.form.get("temp")
    if by == 1 : #author
        user_history[by]
        '''






if __name__ == '__main__':
    app.run(port=8080, debug=True)