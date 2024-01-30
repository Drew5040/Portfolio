import logging
from sys import stdout
from flask import request, render_template, Flask, redirect, url_for, send_from_directory
import numpy as np
import pickle
import os

# from gunicorn.app.base import Application

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, stream=stdout, format='%(asctime)s - %(name)s - %('
                                                               'levelname)s - %(message)s')

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/')
def home_page():
    return render_template('profile.html')


def value_predictor(to_predict_list):
    try:
        loaded_model = pickle.load(open("model.pkl", "rb"))
    except FileNotFoundError:
        logging.error("Model file not found.")
        return None

    if len(to_predict_list) != 12:
        logging.error("Incorrect number of features in input data.")
        return None

    to_predict = np.array(to_predict_list).reshape(1, 12)
    logging.debug(f"Input data for prediction: {to_predict}")

    try:
        results = loaded_model.predict(to_predict)
        logging.info('Results Returned')
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return None

    return results[0]


@app.route('/result', methods=['POST'])
def result():
    logging.info('result page accessed')

    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Check if any required fields are empty
        required_fields = ['age', 'w_class', 'edu', 'martial_stat', 'occupation', 'relation', 'race', 'gender',
                           'hours_per_week', 'native-country']

        for field in required_fields:
            if form_data[field] == '' or form_data[field] == '-':
                # Render the template with the error message
                return render_template('profile.html', error_message='*Please fill out all required fields')

        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))

        # Add a print statement
        logging.debug(f"Received input for prediction: {to_predict_list}")

        results = value_predictor(to_predict_list)
        if int(results) == 1:
            prediction = 'Income more than 50K'
        else:
            prediction = 'Income less than 50K'

        # Add a print statement
        logging.debug(f"Prediction result: {prediction}")

        return redirect(url_for('show_result', prediction=prediction))


@app.route('/show_result/<prediction>')
def show_result(prediction):
    return render_template('result.html', prediction=prediction)


# class FlaskApplication(Application):
#     def __init__(self, parser, opts, *args):
#         super(FlaskApplication, self).__init__(parser, opts)
#         self.parser = parser
#         self.opts = opts
#         self.args = args
#

if __name__ == '__main__':
    # FlaskApplication(None, None).run()
    app.run(debug=True, port=5000)
