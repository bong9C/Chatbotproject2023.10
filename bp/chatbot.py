from flask import Blueprint, render_template, request, current_app
import json, os
# import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import util.chatbot_util as cu

chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'chatbot':1}

@chatbot_bp.before_app_request
def before_app_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'data/dataframe_embedded.csv')
    wdf = pd.read_csv(filename)
    wdf.Cos_Sim_is = wdf.Cos_Sim_is.apply(json.loads)
    print('Wellness initialization is done.')

            

@chatbot_bp.route('/counsel', methods=['GET', 'POST'])
def counsel():
    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        user_input = request.form['userInput']
        print(user_input)
        embedding_is = model.encode(user_input)
        wdf['Cos_Sim_is'] = wdf.embedding_case_names.map(lambda x: cosine_similarity([embedding_is],[x]).squeeze())
        answer1_ik_is = wdf.loc[wdf['Cos_Sim_ik_is'].idxmax()]
        cos_sim_max_val_index_answer1_ik_is = wdf['Cos_Sim_ik_is'].idxmax()
        result = {
            '유사한 판례 일련번호': answer1_ik_is.판례,  '유사한 사건명': answer1_ik_is.사건명, '유사한 판시사항': answer1_ik_is.판시사항, '가장 유사한 판례의 인덱스 값': answer1_ik_is.cos_sim_max_val_index_answer1_is
        }
        return json.dumps(result)


