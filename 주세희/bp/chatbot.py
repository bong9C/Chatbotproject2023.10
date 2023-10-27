from flask import Blueprint, render_template, request, current_app
import json, os
# import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import util.chatbot_util as cu
from flask import Blueprint



chatbot_bp = Blueprint('chatbot_bp', __name__)
menu = {'chatbot':1}

@chatbot_bp.before_request
def before_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'data/dataframe_embedded.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding_case_abstracts = wdf.embedding_case_abstracts.apply(json.loads)
    print('Wellness initialization is done.')

            

@chatbot_bp.route('/counsel', methods=['GET', 'POST'])
def counsel():
    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        user_input = request.form['userInput']
        print(user_input)
        Cos_Sim_ik = model.encode(user_input)
        print("1")
        wdf['Cos_Sim_is'] = wdf.embedding_case_abstracts.map(lambda x: cosine_similarity([Cos_Sim_ik],[x]).squeeze())
        print("2")
        answer1_is = wdf.loc[wdf['Cos_Sim_is'].idxmax()]
        print("3")
       ## answer1_is_max = wdf['Cos_Sim_is'].idxmax()
        result = {
            '판시사항': answer1_is['판시사항']
        }
        return json.dumps(result)


