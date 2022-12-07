from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import train_test_split

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


@api.route('/recommand')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        
        # 내장 데이터인 무비렌즈 데이터 로드하고 학습/테스트 데이터로 분리
        data = Dataset.load_builtin('ml-100k', prompt=False)
        train, test = train_test_split(data, test_size=0.25,
                              random_state=42)


        algo = SVD()
        algo.fit(train)

        prediction = algo.test(test)

        print('prediction 결과값 5개 미리보기')
        print(prediction[:5])

        return {"items": prediction}

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)




