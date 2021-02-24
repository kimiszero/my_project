
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

reviews = [
    {
        'image': 'review_image1.png',
        'user_info': '직장인 강ㅇ정님',
        'title': '홈핏 코치님과 운동하며, 바디프로필 성공했어요!',
        'desc': '워낙 근육이 없고 복부 경도 비만이었는데, 코치님과 3개월간 홈핏 방문 PT를 시작하며 바디프로필 준비도 할 수 있었어요!',
    },
    {
        'image': 'review_image2.png',
        'user_info': '직장인 김ㅇ정님',
        'title': '부담없는 가격의 맞춤형 운동이라 좋아요!',
        'desc': '방문 수업과 실시간 비대면 수업을 볗앵하니 시간도 절약하고 가격 부담 없이 1:1맞춤형 운동을 할 수 있어서 만족해요!',
    },
    {
        'image': 'review_image3.png',
        'user_info': '산모 박ㅇ리님',
        'title': '아기랑 집에서 산후 관리하고 싶다면 추천해요!',
        'desc': '아기는 바운서에 태워 놓고 수업받았어요. 골반의 틀어짐을 바로잡고 목과 어깨의 스트레칭과 바른 자세에 중점으로 운동하니 너무 시원하네요!',
    },
]

for review in reviews:
    db.reviews.insert_one(review)