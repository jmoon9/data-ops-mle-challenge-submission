import flask
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request

model = tf.keras.models.load_model('/model/yolo_model')

def predict_result(last_sixty_seconds_of_prices):
    return model.predict(last_sixty_seconds_of_prices)

app = Flask(__name__)

@app.route('/invocations', methods=['POST'])
def predict():   
    last_sixty_seconds = request.get('data')
    return jsonify(prediction=predict_result(last_sixty_seconds))   

@app.route('/', methods=['GET'])
def index():
    return 'Bitcoin Price Inference'

# Sagemaker Inference Health Check
@app.route('/ping', methods=['GET'])
def index():
    return 'Healthy'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')