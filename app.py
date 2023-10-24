from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')     
def home():
    return " "

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat')
def chat():
        return render_template('chat.html')



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)



