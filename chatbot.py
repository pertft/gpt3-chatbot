from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)

chat_history = [
            ["Hva er Kjerneverdiene til Bouvet?", 
            "Hei! Kjerneverdiene er troverdighet, jordnærhet, delingskultur, frihet og entusiasme. #"],
            ["Hva er hovedstaden i Norge", "hovedstaden i Norge er Oslo, tidligere her det Kristiania :) #"],
            ["Hvor mange mennesker bor i Norge?", "hmm tror det er ca 5000000, mindre en Sverige #"],
            ["Kan du si meg hva hovedstaden i Norge er", "Det er Oslo, tidligere her det Kristiania :) #"],
            ]

context = "Chatbot som syntes det er bare hyggelig å hjelpe og svarer gjerne på spørsmål. Jeg er en chatbot basert på GPT-3. Kjerneverdiene til Bouvet er troverdighet, jordnærhet, delingskultur, frihet og entusiasme. hovedstaden i Norge er Oslo, det bor 5000000 mennesker i Norge." 


def gpt3_no_doc(question):
    global chat_history, context
    response = openai.Answer.create(
        search_model="curie",
        model="davinci", 
        question=question,
        documents = ["Det er ledige stilinger, søk her www.bouvet.no/jobb. Lederen i PIA er Mark West, Kontakt info til Mark West er mark.west@bouvet.no. Liste over hva data science kan gjøre: analysere data for å skape innsikt\nbruke maskinlæring for å skape nye muligheter\nGjøre bedrifter data drevene"],
        examples_context=context,
        examples=chat_history, 
        max_rerank=5,
        max_tokens=300,
        temperature=0,
        return_metadata = False,
        stop=["<|endoftext|>", "#", "---"]
    )
    res = response.answers[0]
    return res
    
def gpt3(question):
    global chat_history, context
    return_metadata = True
    urls = None
    url = None
    try:
        response = openai.Answer.create(
            search_model="curie",
            model="davinci", 
            question=question,
            file="file-zoAmPASFyyviEGWQ9tYYH7u2",
            examples_context=context,
            examples=chat_history, 
            max_rerank=5,
            max_tokens=300,
            temperature=0,
            return_metadata = return_metadata,
            stop=["<|endoftext|>", "#", "---", "==="]
        )

        print(response)
        res = response.answers[0]
        if return_metadata:
            urls = [d.metadata for d in response.selected_documents]
            scores = [d.score for d in response.selected_documents]
            max_score = max(scores)
            url = urls[scores.index(max_score)]
            print(url)

        if "\n" in res:
            print(list(set(res.split("\n"))))
            res = "<br>".join(list(set(res.split("\n"))))

        res = res.replace("Context: ", "")
        res = res.replace("Ã¦", "æ").replace("Ã¥", "å").replace("Ã¸", "ø").replace("Ã˜", "Ø").replace("Ã…", "Å")
        print(res)

        if urls and max_score > 140:
            more_info = ". Du kan kanskje finne mer info her: " + url
            return res + more_info
        else:
            print(url)
            return res

    except Exception as e:
        print("Exception", e)
        return gpt3_no_doc(question)

@app.route("/", methods = ['POST'])
def index():
    question_json = json.loads(request.get_data())
    answer = {"a": gpt3(question_json["a"])}
    return answer

if __name__ == "__main__":
    app.run(debug = True)