from flask import Flask, make_response, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import train_test_split
from flask_cors import CORS
import os
# from dotenv import load_dotenv
# import pymysql

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
CORS(app)

@api.route('/recommand', methods=['GET', 'POST'])  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        # 내장 데이터인 무비렌즈 데이터 로드하고 학습/테스트 데이터로 분리

        params = request.get_json()
        id = params['id']
        data = Dataset.load_builtin('ml-100k', prompt=False)
        train, test = train_test_split(data, test_size=0.25,
                              random_state=42)

        
        algo = SVD()
        algo.fit(train)

        prediction = algo.test(test)

        recommandList = []

        for i in prediction:
            if int(i.uid) == id :
                recommandList.append({"uid": i.uid, "iid" : i.iid, "est" : str(i.est)})


        print(recommandList)
        # print(prediction)

        return {"items": recommandList}

        #디비 연동하는 법입니다
        #db = pymysql.connect(host=os.environ.get("FLASK_HOST"),user = os.environ.get("FLASK_USER"), db = os.environ.get("FLASK_DB"), password=os.environ.get("FLASK_PW") , charset=os.environ.get("FLASK_CHARSET"))
        #curs = db.cursor()

        #sql = "select * from user"

        #curs.execute(sql)
        #rows = curs.fetchall()
        #print(rows)

        #db.commit()
        #db.close()
       

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)




