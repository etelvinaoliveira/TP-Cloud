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
       "version": model.version,
       "model_date": model.model_date 
    }
    return jsonify(resp)

@app.route("/api/recommender", methods=['GET'])
def recommendation_page():
   return render_template("client.html")

if __name__ == '__main__':
  app.run()
  