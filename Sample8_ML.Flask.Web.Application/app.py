import logging
from flask import request, render_template, Flask
from gunicorn.app.base import Application
import numpy as np
import pickle

# Set up logging configuration
logging.basicConfig(filename='logs/flask/error.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %('
                                                                                 'levelname)s - %(message)s')

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('profile.html')


def value_predictor(to_predict_list):
    try:
        loaded_model = pickle.load(open("model.pkl", "rb"))
    except FileNotFoundError:
        logging.error("model file not found...")
        return None

    if len(to_predict_list) != 12:
        return None

    to_predict = np.array(to_predict_list).reshape(1, 12)

    try:
        results = loaded_model.predict(to_predict)
        logging.info('results returned...')
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return None

    return results[0]


@app.route('/result', methods=['POST'])
def result():
    logging.info('result page accessed...')

    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Check if any required fields are empty
        required_fields = ['age', 'w_class', 'edu', 'martial_stat', 'occupation', 'relation', 'race', 'gender',
                           'c_gain', 'c_loss', 'hours_per_week', 'native-country']
        print(form_data)
        for field in required_fields:

            if form_data[field] == '' or form_data[field] == '-':
                logging.debug('error_message accessed...')
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

        return render_template('result.html', prediction=prediction)


class FlaskApplication(Application):
    def __init__(self, parser, opts, *args):
        super(FlaskApplication, self).__init__(parser, opts)
        self.parser = parser
        self.opts = opts
        self.args = args


if __name__ == '__main__':
    logging.debug('main() accessed ...')
    FlaskApplication(None, None).run()
