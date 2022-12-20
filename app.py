from flask import Flask, make_response, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import train_test_split
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler  
from datetime import datetime
import requests
from bs4 import BeautifulSoup
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
# main code
def runner():
    print(f'{datetime.now()}:runner')


sched = BackgroundScheduler()

# main job
runner_job = sched.add_job(runner, 'interval', hours=1)#seconds=10)

# start job
def start_runner():
    print(f'{datetime.now()}:start_runner')
    url = "https://www.weather.go.kr/w/weather/forecast/short-term.do?stnId=109" 
    res = requests.get(url) 
    res.raise_for_status() # 정상 200
    soup = BeautifulSoup(res.text, "lxml")
    #print(soup.body)
    tem = soup.find('ul',attrs={"class":"item vs-item  v-item-first"})
    print(tem)
    temlist = tem.find('span')
    print(temlist)
    runner_job.resume()

# stop job
def stop_runner():
    print(f'{datetime.now()}:stop_runner')
    runner_job.pause()

# to delay main job
stop_runner()

# schedules for main job
sched.add_job(start_runner, 'cron', minute='1,6,17,19,28,51')
sched.add_job(stop_runner, 'cron', minute='5,18,25,35,45,55')

sched.start()

@api.route('/test', methods=['GET', 'POST'])
class test(Resource):
    
    def get(self):
        url = "https://www.weather.go.kr/w/weather/forecast/short-term.do?stnId=109" 
        res = requests.get(url) 
        res.raise_for_status() # 정상 200
        soup = BeautifulSoup(res.text, "html.parser")
        #print(soup)
        tem = soup.find('div',attrs={"class":"lay"})
        
        print(tem)
        tem1 = soup.find_all(class_='slide-wrap snow-exists rain-exists')

        print(tem1)

        

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)




