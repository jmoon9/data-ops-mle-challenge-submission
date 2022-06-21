from flask import make_response
from modules.encoder import NumpyEncoder
import socket
import tensorflow as tf
import numpy as np
import json


class Prediction:
    def __init__(self) -> None:
        pass
    
    target = None
    last_sixty_seconds = None
    loaded_model = None
    host_ip = socket.gethostbyname(socket.gethostname())
    
    @classmethod
    def load_model(self):
        # Load model from /model/yolo_model.h5 if docker
        print(self.host_ip)
        if(self.host_ip == '172.17.0.2'):
            self.loaded_model = tf.keras.models.load_model('/model/yolo_model.h5')
            
        # Load model from ../model/yolo_model.h5 if any other deployment
        else:
            self.loaded_model = tf.keras.models.load_model('../model/yolo_model.h5')
    
    @classmethod
    def lookback(self, dataset, timesteps = 60):
        # this uses the shift method of pandas dataframes to shift all of the columns down one row
        # and then append to the original dataset
        data = dataset
        for i in range(1, timesteps):
            step_back = dataset.shift(i).reset_index()
            step_back.columns = ['index'] + [f'{column}_-{i}' for column in dataset.columns if column != 'index']
            data = data.reset_index().merge(step_back, on='index', ).drop('index', axis=1)
        return data.dropna()
    
    # Generate features and target tensors
    @classmethod
    def create_tensors(self, data):
        data = data.drop(['time_period_start', 'time_period_end', 'time_open', 'time_close'], axis=1)
        self.last_sixty_seconds = self.lookback(data)
        self.target = self.last_sixty_seconds['price_high'].values
        self.last_sixty_seconds = self.last_sixty_seconds.drop('price_high', axis=1).values
        return
    
    @classmethod
    def predict_result(self, last_sixty_seconds_of_prices):
        return self.loaded_model.predict(last_sixty_seconds_of_prices)
    
    @classmethod
    def calculate_rmse(self, target, prediction):
        return np.sqrt(np.mean(np.square((target.reshape(-1, 1) - prediction))))
    
    @classmethod
    def predict(self, data):
        try: 
            self.create_tensors(data)
            prediction = self.predict_result(self.last_sixty_seconds)
        except ValueError:
            return make_response('Value Error encountered', 400)
        except Exception as e:
            return make_response('Something went wrong: ' + e.args[0], 400)
        rmse = self.calculate_rmse(self.target, prediction)
        
        return json.dumps({'evaluation': rmse, 'prediction': prediction}, cls=NumpyEncoder)