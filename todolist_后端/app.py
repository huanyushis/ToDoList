from flask import Flask, request
import json
import pymysql
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

@app.route("/")
def index():
    return "<h1>hello world</h1>"


@app.route('/api/findAll', methods=['get'])
def hello_world():
    db = pymysql.connect("localhost", "root", "123456", "todolist")
    cursor = db.cursor()
    sql = "select * from todolist"
    cursor.execute(sql)
    col = cursor.description
    colums = [item[0] for item in col]
    informations = cursor.fetchall()
    dicts = {
        "message": "操作成功",
        "success": True,
        "data": {
            "list": {
                "complete": {

                },
                "incomplete": {

                }
            },
            "page": {
                "totalCount": len(informations)
            }

        }

    }
    complete = 0
    incomplete = 0
    for information in informations:
        if information[2] == "0":
            dicts["data"]["list"]["incomplete"][incomplete] = dict(zip(colums, information))
            incomplete += 1
        else:
            dicts["data"]["list"]["complete"][complete] = dict(zip(colums, information))
            complete += 1
    dicts['data']['page']['completeCount'] = len(dicts["data"]["list"]["complete"])
    dicts['data']['page']['incompleteCount'] = len(dicts["data"]["list"]["incomplete"])
    cursor.close()
    db.close()
    return json.dumps(dicts, cls=DateEncoder), 200


@app.route('/api/delete', methods=['get'])
def delete():
    try:
        id = request.args['id']
        db = pymysql.connect("localhost", "root", "123456", "todolist")
        cursor = db.cursor()
        sql = "delete from todolist where id=%s" % (id)
        cursor.execute(sql)
        db.commit()

        dicts = {
            "message": "操作成功",
            "success": True
        }
        cursor.close()
        db.close()
        return json.dumps(dicts), 200

    except:
        dicts = {
            "message": "操作失败",
            "success": False
        }
        return json.dumps(dicts), 503


@app.route('/api/add', methods=['get'])
def add():
    try:
        content = request.args['content']
        db = pymysql.connect("localhost", "root", "123456", "todolist")
        cursor = db.cursor()
        datenow = datetime.datetime.now().date()
        sql = "insert into todolist (content,isover,datetime) values (\"%s\",\"%s\",\"%s\")" % (
            content, 0, datenow)
        cursor.execute(sql)
        id = db.insert_id()
        db.commit()

        dicts = {
            "message": "操作成功",
            "success": True,
            "data": {
                "id": id,
                "content": content,
                "datetime": datenow
            }
        }
        cursor.close()
        db.close()
        return json.dumps(dicts, cls=DateEncoder), 200
    except:
        dicts = {
            "message": "操作失败",
            "success": False,

        }
        return json.dumps(dicts), 503


@app.route("/api/update")
def update():
    try:
        type = int(request.args['type'])
        id = request.args['id']
        db = pymysql.connect("localhost", "root", "123456", "todolist")
        cursor = db.cursor()
        sql = "update todolist set isover=%s where id=%s" % (type, id)
        cursor.execute(sql)
        db.commit()
        dicts = {
            "message": "操作成功",
            "success": True
        }
    except:
        dicts = {
            "message": "操作失败",
            "success": False,

        }
    return json.dumps(dicts)
@app.route("/favicon.ico")
def ico():
    return app.send_static_file("logo.ico")
if __name__ == '__main__':
    app.run()