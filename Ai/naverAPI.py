from flask import Flask, render_template


app = Flask(__name__)
                    # htp://127.0.0.1:5000/ (/ 생략)
     # localhost:5000/ 을 서비스하기 위한 코드 

@app.route('/Index')
def hello():
    return render_template('Index.html')



