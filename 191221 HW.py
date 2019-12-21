from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('191220 homework.html')


## API 역할을 하는 부분
@app.route('/post', methods=['POST'])
def test_post():
    name_receive = request.form['order_name']
    count_receive = request.form['order_count']
    address_receive = request.form['order_address']
    phone_receive = request.form['order_phone']
    print(name_receive, count_receive, address_receive, phone_receive)

    article = {'name': name_receive, 'count': count_receive, 'address': address_receive,
               'phone': phone_receive}

    db.orders.insert_one(article)

    return jsonify({'result': 'success'})


@app.route('/post', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.orders.find({}, {'_id': 0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'orders': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
