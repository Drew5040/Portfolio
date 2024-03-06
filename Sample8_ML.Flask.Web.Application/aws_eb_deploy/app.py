import logging
from flask import request, render_template, Flask
from gunicorn.app.base import Application
import numpy as np
import pickle
import json

# Set Logger
logging.basicConfig(filename='logs/flask/error.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %('
                                                                                 'levelname)s - %(message)s')

# Set app instance
app = Flask(__name__)


# Set homepage route
@app.route('/')
def home_page():
    return render_template('welcome.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/model')
def model_page():
    return render_template('model.html')


# @app.route('/contact')
# def contact_page():
#     return render_template('contact.html')


# Model Prediction
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


def validate_form_entries(form_data):
    errors = {}
    required_fields = ["age", "w_class", "edu", "marital_stat", "occupation", "relation", "race", "gender",
                       "c_gain", "c_loss", "hours_per_week", "native-country"]

    is_valid = True
    for field in required_fields:
        if form_data.get(field, "") in ["", "-"]:
            is_valid = False
            break

    # Add any additional validation checks here, for example, checking if age is a number
    if "age" in form_data and (not form_data["age"].isdigit() or not 17 <= int(form_data["age"]) <= 90 or isinstance(form_data["age"], float)):
        errors["age"] = "**Age must be a valid number**"
        is_valid = False
    if "w_class" in form_data and form_data["w_class"] == "-":
        errors["w_class"] = "**Please choose a category**"
    if "edu" in form_data and form_data["edu"] == "-":
        errors["edu"] = "**Please choose a category**"
    if "marital_stat" in form_data and form_data["marital_stat"] == "-":
        errors["marital_stat"] = "**Please choose a category**"
    if "occupation" in form_data and form_data["occupation"] == "-":
        errors["occupation"] = "**Please choose a category**"
    if "relation" in form_data and form_data["relation"] == "-":
        errors["relation"] = "**Please choose a category**"
    if "race" in form_data and form_data["race"] == "-":
        errors["race"] = "**Please choose a category**"
    if "gender" in form_data and form_data["gender"] == "-":
        errors["gender"] = "**Please choose a category**"
    if "c_gain" in form_data and (not form_data["c_gain"].isdigit() or not 0 <= int(form_data["c_gain"]) <= 99999 or isinstance(form_data, float)):
        errors["c_gain"] = "**Please choose a category**"
        is_valid = False
    if "c_loss" in form_data and (not form_data["c_loss"].isdigit() or not 0 <= int(form_data["c_loss"]) <= 4356 or isinstance(form_data["c_loss"], float)):
        errors["c_loss"] = "**Please choose a category**"
        is_valid = False
    if "hours_per_week" in form_data and (not form_data["hours_per_week"].isdigit() or not 1 <= int(form_data["hours_per_week"]) <= 99 or isinstance(form_data["hours_per_week"], float)):
        errors["hours_per_week"] = "**Please enter a valid number**"
        is_valid = False
    if "native-country" in form_data and form_data["native-country"] == "-":
        errors["native-country"] = "**Please select a category**"


    return is_valid, errors, form_data


# Display prediction
@app.route('/model', methods=['POST'])
def result():
    logging.info('result page accessed...')

    if request.method == 'POST':

        form_data = request.form.to_dict()
        boole, errors, form_data = validate_form_entries(form_data)

        if not boole:
            errors_json = json.dumps(errors)
            print("errors_json: ", errors_json)
        else:
            errors_json = json.dumps({})

        if boole:
            to_predict_list = list(form_data.values())
            print(to_predict_list)
            to_predict_list = list(map(int, to_predict_list))
            print(to_predict_list)
            logging.debug(f"Received input for prediction: {to_predict_list}")

            results = value_predictor(to_predict_list)

            if int(results) == 1:
                prediction = "**Income more than 50K**"
            else:
                prediction = "**Income less than 50K**"

            logging.debug(f"Prediction result: {prediction}")

            return render_template('model.html', prediction=prediction)

        else:
            logging.debug('error_message accessed...')
            form_data = request.form.to_dict()
            print('form_data that gets passed to error in entry template: ', form_data)
            print('errors json fields: ', errors_json)
            return render_template('model.html',
                                   form_data=form_data,
                                   errors_json=errors_json,
                                   error_message='**Please fill out all required fields**')


class FlaskApplication(Application):
    def __init__(self, parser, opts, *args):
        super(FlaskApplication, self).__init__(parser, opts)
        self.parser = parser
        self.opts = opts
        self.args = args


if __name__ == '__main__':
    # Log that main() is accessed
    logging.debug('main() accessed ...')

    # Start application
    FlaskApplication(None, None).run()

    # Development server
    # app.run(debug=True, port=5000)