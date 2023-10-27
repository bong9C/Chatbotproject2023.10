from flask import Blueprint, render_template, request, current_app
import json, os
# import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'chatbot'}

@chatbot_bp.before_app_request
def before_app_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'data/wellness_dataset.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding = wdf.embedding.apply(json.loads)
    print('Wellness initialization is done.')

            

@chatbot_bp.route('/chatbot', methods=['GET', 'POST'])
def chat_bot():
    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        user_input = request.form['userInput']
        embedding = model.encode(user_input)
        wdf['유사도'] = wdf.embedding.map(lambda x: cosine_similarity([embedding], [x]).squeeze())
        answer = wdf.loc[wdf.유사도.idxmax()]
        result = {
            'category': answer.구분, 'user': user_input, 'chatbot': answer.챗봇, 'similarity': answer.유사도
        }
        return json.dumps(result)


``