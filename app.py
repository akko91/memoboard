from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient

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

    print(date);

    doc = {
        'title': title,
        'content': content,
        # 'writer': 현재 작성자 명 받아와야됨
        # 'date': 현재 시간 받아와야됨
    }
    
    # db.memoboard.insert_one(doc);

    return jsonify({'result': 'success', 'msg': '메모 완료!'})

# 목록 읽기
@app.route('/memo-list', methods=['GET'])
def get_memolist():
    return jsonify({'result': 'success', 'msg': '목록 불러오기 완료!'})

# 메모 읽기
@app.route('/memo', methods=['GET'])
def get_memo():
    return jsonify({'result': 'success', 'msg': '메모 불러오기 완료!'})

# 삭제
@app.route('/memo', methods=['DELETE'])
def delete_memo():
    return jsonify({'result': 'success', 'msg': '메모 삭제 완료!'})

# 수정
@app.route('/memo', methods=['PUT'])
def put_memo():
    return jsonify({'result': 'success', 'msg': '메모 수정 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
