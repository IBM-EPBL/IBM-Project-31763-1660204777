import numpy as np
from flask import Flask, request, jsonify, render_template , redirect
import pickle
import inputScript

#   importing the inputScript file used to analyze the URL


#   load model
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))

#   Redirects to Webpage
@app.route('/')
def predict():
    return render_template("index.html")


#  fetches given URL and passes to inputScript
@app.route('/predict', methods=["POST"])
def y_predict():
    url = request.form['url']
    checkpredition =inputScript.main(url)
    print(checkpredition)
    prediction = model.predict(checkpredition)

    print(prediction)
    result = prediction[0]
    print(result)

    if (prediction == 1):
        pred = "This is a Legimate Website "
    elif (prediction == -1):
        pred = "You are in a phishing site"

    return render_template("index.html", pred_text='{}'.format(pred), url=url)


#   Takes input parameters from URL by inputScript and returns the predictions
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)