from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask, render_template, request, flash, url_for, session
import jieba

app = Flask(__name__)

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='',
    db='satellite',
    charset='utf8'
)
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/show')
def hello_world():
    cur = conn.cursor()
    # get annual sales rank
    sql = "select * from satellite_data"
    cur.execute(sql)
    content = cur.fetchall()
	# 获取表头
    sql = "SHOW FIELDS FROM satellite_data"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    return render_template('index.html', labels=labels, content=content)

@app.route('/gets/',methods=['POST'])
def search():
    conn = pymysql.connect(user='root', host='localhost', passwd='', db='satellite',cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    S = request.values.get('question')
    sql = "select * from satellite_data where id like '%"+S+"%' or name like '%"+S+"%' or a_name like '%"+S+"%' or state like '%"+S+"%'"
    cur.execute(sql)
    datas = cur.fetchall()
    return render_template('result.html',items=datas)

@app.route('/help')
def help():
    return render_template('md.html')



