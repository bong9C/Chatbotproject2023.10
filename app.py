from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')     
def home():
    return " "

@app.route('/contact2')
def index():
    return render_template('contact2.html')





if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)



