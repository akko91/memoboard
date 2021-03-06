from bson import objectid
from flask import Flask, render_template, jsonify, request, json
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# 글쓰기
@app.route('/memo', methods=['POST'])
def post_memo():
    title = request.form['title']
    content = request.form['content']
    date = request.form['date']
    writer = "글쓴이"

    # print(date);

    doc = {
        'title': title,
        'content': content,
        'writer': writer,
        'date': date
    }

    db.memoboard.insert_one(doc);

    return jsonify({'result': 'success', 'msg': '메모 완료!'})


# 목록 읽기
@app.route('/memolist', methods=['GET'])
def get_memolist():
    page = request.args.get('page')
    nowpage = (int(page)-1)*10
    # print(nowpage)

    memo_list = list(db.memoboard.find({}, {"_id": False}).skip(nowpage).limit(10).sort('date', -1))
    id = list(db.memoboard.find({}, {"title": False, "content": False, "writer": False, "date": False}).skip(nowpage).limit(10).sort('date', -1))
    memo_count = db.memoboard.count()

    # print(memo_count)

    id_list = [str(i["_id"]) for i in id]
    # print(id_list)

    memo_json = {"response": "success", "memoList": memo_list, "memoId": id_list, "memoCount": memo_count}

    return jsonify(memo_json)


# 메모 읽기
@app.route('/memo', methods=['GET'])
def get_memo():
    # id = request.form['id']
    id = request.args.get('id')

    memo = list(db.memoboard.find({"_id": ObjectId(id)},{"_id": False}))

    # print(memo)

    return jsonify({'result': 'success', 'memo': memo, 'id': id})


# 삭제
@app.route('/memo', methods=['DELETE'])
def delete_memo():
    id = request.form['id']
    # print(id)

    db.memoboard.delete_one({"_id": ObjectId(id)})


    return jsonify({'result': 'success', 'msg': '메모 삭제 완료!'})


# 수정
@app.route('/memo', methods=['PUT'])
def put_memo():
    id = request.form['id']
    title = request.form['title']
    content = request.form['content']

    db.memoboard.update({"_id": ObjectId(id)},{'$set': {"title": title, "content":content}})
    return jsonify({'result': 'success', 'msg': '메모 수정 완료!'})

# 카카오로그인
@app.route('/loginkakao', methods=['GET'])
def login_kakao():
    code = str(request.args.get('code'))
    token_request = requests.get("https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id=df475ca2677579b0061637b140098f01&redirect_uri=http://localhost:5000/loginkakao&code="+str(code))
    token_json = token_request.json()

    access_token = token_json.get("access_token")

    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": "Bearer " + access_token} )
    profile_json = profile_request.json()

    kakao_account = profile_json.get("kakao_account")

    profile = kakao_account['profile']
    kakao_id = profile_json.get("id")

    # email = kakao_account.get("email", None)
    # print("id:"+kakao_id+", "+"nickname: "+ nickname)

    return jsonify({'result': 'success', 'profile': profile, 'kakao_id': kakao_id })





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
