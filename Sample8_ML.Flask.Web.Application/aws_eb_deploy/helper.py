"""
This module contains helper functions for model prediction and form validation
in a sample machine learning Flask web application.
"""

from log_config import logger
from pickle import load
from numpy import array


# Model Prediction
def value_predictor(to_predict_list):
    """
    Predicts the value based on the model loaded from a .pkl file and input features list.

    :param to_predict_list: List of features for the model to predict
    :return: The predicted result or None if an error occurs
    """
    # Log value predictor was accessed
    logger.debug("value_predictor accessed ...")

    try:
        with open("model.pkl", "rb") as file:
            loaded_model = load(file)
    except FileNotFoundError:
        logger.error("model file not found...")
        return None

    if len(to_predict_list) != 12:
        return None

    to_predict = array(to_predict_list).reshape(1, 12)
    logger.debug("Prediction rendered")

    try:
        results = loaded_model.predict(to_predict)

        # Log that the results are returned
        logger.debug(f'Prediction made from value_predictor()...: {results}')

    except Exception as e:

        # Log that an exception has taken place
        logger.error(f"Error during prediction: {e}")

        return None

    return results[0]


def validate_form_entries(form_data):
    """
    Validates the form data against required fields and rules.

    :param form_data: Dictionary containing form data to validate
    :return: Tuple containing a boolean validation result, errors dictionary, and form_data
    """

    # Log the form validation function was accessed
    logger.info('Form validation accessed...')

    errors = {}
    required_fields = ["age", "w_class", "edu", "marital_stat", "occupation", "relation",
                       "race", "gender", "c_gain", "c_loss", "hours_per_week", "native-country"]

    is_valid = True
    for field in required_fields:
        if form_data.get(field, "") in ["", "-"]:
            is_valid = False
            logger.debug('Error in form data ...')
            errors[field] = "**Please choose a category**"

    numerical_fields_checks = {
        "age": (17, 90),
        "c_gain": (0, 99999),
        "c_loss": (0, 4356),
        "hours_per_week": (1, 99),
    }

    for field, (min_val, max_val) in numerical_fields_checks.items():
        value = form_data.get(field, "0")
        if not value.isdigit() or not min_val <= int(value) <= max_val:
            logger.debug("Form entries not valid ...")
            is_valid = False
            errors[field] = f"**{field.replace('_', ' ').title()} must be a valid number**"
    logger.info("Form data is valid...")
    return is_valid, errors, form_data
