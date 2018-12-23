# Main entry.

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import pymysql
import datetime
import html


app = Flask(__name__) # Main app object.
app.secret_key = 'jF1dCbD'

@app.route('/', methods=['GET', 'POST'])
def home():

     host = "localhost"
     user = "root"
     password = ""
     database = "avowal"

     con = pymysql.connect(host=host, user=user, password=password, db=database, cursorclass=pymysql.cursors.DictCursor)
     cur = con.cursor()

     cur.execute("SELECT databaseId, postedby, story, date FROM stories LIMIT 100")
     result = cur.fetchall()

     cur.execute("SELECT databaseId, postedby, postid, comment FROM comments LIMIT 100")
     commentResult = cur.fetchall()

     if request.method == 'POST':
         if request.form['myStory'] != "":
            now = datetime.datetime.now()
            query = "INSERT INTO stories(postedby, story, date) VALUES(%s, %s, %s)"
            if cur.execute(query, (request.form['name'], request.form['myStory'], now.strftime("%Y-%m-%d %H:%M"))):
                cur.execute('COMMIT')
                flash('Story has been posted.')
                return redirect(url_for('home'))
            else:
                flash("Something went wrong!")
                return redirect(url_for('home'))


     return render_template('index.html', commentResult=commentResult, storiesResult=result, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)