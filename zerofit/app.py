import jwt
import datetime
import hashlib
from functools import wraps
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for, g

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

SECRET_KEY = 'hello world'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 쿠키에서 token_give 가져오기
        token_receive = request.cookies.get('token_give')
        print('token_receive :', token_receive)

        if token_receive is None:
            # token이 없는 경우
            return redirect(url_for('login'))

        try:
            # 전달받은 token이 위조되었는지 확인 (단방향이기 때문에 비밀번호와 마찬가지로 해쉬처리하여 동일한지 비교)
            # SECRET_KEY를 모르면 동일한 해쉬를 만들 수 없음
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            # 토큰 없거나 만료되었거나 올바르지 않은 경우 로그인 페이지로 이동
            return redirect(url_for('login'))

            # g는 각각의 request 내에서만 값이 유효한 스레드 로컬 변수입니다.
            # 사용자의 요청이 동시에 들어오더라도 각각의 request 내에서만 g 객체가 유효하기 때문에 사용자 ID를 저장해도 문제가 없습니다.
        g.user = db.user.find_one({'id': payload["id"]})

        # 로그인 성공시 다음 함수 실행
        return f(*args, **kwargs)

    return decorated_function

# HTML 응답 API
@app.route('/')
@login_required
def main():
    return render_template('main.html', user=g.user)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

# JSON 응답  :: 리뷰 페이지네이션으로 가져오기
@app.route('/pagingreviews', methods=['GET'])
def show_pagination_reviews():
    size = int(request.args.get('size', 3))
    page = int(request.args.get('page', 1))

    n_skip = size * (page - 1)
    print(f'size : {size} / page : {page} / skip : {n_skip}')

    review_list = list(db.reviews.find({}, {'_id': False}).skip(n_skip).limit(size))
    total = db.reviews.count()
    print(f'total : {total}')
    print(review_list)
    return jsonify({'result': 'success', 'total': total, 'data': review_list})

# JSON 응답 API :: 회원가입
@app.route('/api/join', methods=['POST'])
def api_join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    user = db.user.find_one({'id': id_receive})
    if user is not None:
        return jsonify({'result': 'fail', 'msg': '아이디가 중복되었습니다 😅'})

    # pw를 sha256 방법(단방향)으로 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash})

    return jsonify({'result': 'success', 'msg': '🎉 회원 가입을 축하합니다 🎉'})


# 로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # pw를 sha256 방법(단방향)으로 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된 pw을 가지고 해당 유저를 찾기
    user = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if user is not None:
        # jwt 토큰 발급
        payload = {
            'id': user['id'],  # user id
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 5)  # 만료 시간 (10초 뒤 만료)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(f'token : {token}')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디와 비밀번호를 확인해주세요 😓'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    jwt.invalidate()
    return render_template('main.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)