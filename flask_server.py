from flask import Flask, render_template, request, jsonify, make_response, url_for
from mysqldb import DB
app = Flask(__name__)

@app.route('/')
def index():
    db = DB()
    temp = url_for('static', filename='style.css')
    return render_template('webpage.html', titles = table.columns.values)

@app.route("/postmethod", methods=["GET", "POST"])
def search() :
    id = request.form.get('temp')
    db = DB()
    table = db.search_article_by_id(id)
    if table.empty == True :
        return {"status" : "fail"}
    temp = {"status" : "success", "data" : table.to_html(classes = 'data')}
    return jsonify(temp)


if __name__ == '__main__':
    app.run(port=8080, debug=True)