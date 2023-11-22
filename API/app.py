#LEMBRETE: $ export FLASK_APP=<nomeDesteArquivoSem.py>
# passar isso de parametro do Dockerfile: flask run --host=0.0.0.0
#IMPORTANTE: especificar a versão do python que rodamos o modelo e o flask, precisa ser a mesma senão o pickle dá erro

from flask import Flask, request, jsonify, render_template
import dill
import os

app = Flask(__name__)

@app.route("/api/recommender", methods=['POST'])
def recommend():
    model = dill.load(open(os.getenv("MODEL_PATH"), "rb"))
    data_json = request.get_json()
    songs = data_json["songs"]
    recommendation = model.predict(songs)
    resp = {
       "playlist_ids":recommendation[:10],
       "version": 1,
       "model_date": 1 
    }
    return jsonify(resp)

@app.route("/api/recommender", methods=['GET'])
def recommendation_page():
   return render_template("client.html")

if __name__ == '__main__':
  app.run()