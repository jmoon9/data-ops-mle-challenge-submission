from distutils.log import ERROR
import pandas as pd
from flask import Flask, request
import logging
import uuid

from modules.validation import Validation
from modules.prediction import Prediction

app = Flask(__name__)
logging.basicConfig(filename='error.log', level=ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Load prediction class object and model from h5
predictor = Prediction()
predictor.load_model()

@app.route('/predict', methods=['POST'])
def predict():      
    # Data Validation class object
    validator = Validation()
    
    file = request.files['file']
    requestId = str(uuid.uuid4())
    
    # Accessibility check - Input CSV Availability
    try:
        data = pd.read_csv(file)
    except Exception as err:
        error_msg = "Input data quality check failed: data unavailable"
        return validator.exception_generator(error_msg, requestId, app)
    
    # Data Validation checks
    try:
        validator.validate_input_data(data)
    except Exception as err:
        error_msg = "Input data quality check failed: " + err.args[0]
        return validator.exception_generator(error_msg, requestId, app)
    
    return predictor.predict(data)

@app.route('/', methods=['GET'])
def index():
    return 'Bitcoin Price Inference'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')