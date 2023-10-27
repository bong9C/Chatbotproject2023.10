import requests, json, os



def get_legal_answer(static_folder, question):
    openApiURL = "http://localhost:5000/chatbot"
    filename = os.path.join(static_folder, 'keys/')
    with open(filename) as f:
        accessKey = f.read()
    headers = {"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey}
    requestJson = { "argument": { "question": question } }
    result = requests.post(openApiURL, headers=headers, data=json.dumps(requestJson)).json()
    if len(result['return_object']['LegalInfo']['AnswerInfo']) == 0:
        return {'result': 0, 'answer': '앗! 다음에 더 준비해 볼게요ㅠㅠ.'}
    else:
        res_dict = result['return_object']['LegalInfo']['AnswerInfo'][0]
        res_dict['result'] = 1
        return res_dict