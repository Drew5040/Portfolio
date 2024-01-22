from flask import request, render_template, Flask
import numpy as np
import pickle

app = Flask(__name__)


def value_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 12)
    loaded_model = pickle.load(open("model.pkl", "rb"))
    results = loaded_model.predict(to_predict)
    return results[0]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        results = value_predictor(to_predict_list)
        if int(results) == 1:
            prediction = 'Income more than 50K'
        else:
            prediction = 'Income less that 50K'
        return render_template("result.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
