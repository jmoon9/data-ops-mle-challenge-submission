import sys
import json
import requests
from flask import make_response

class Validation:
    def __init__(self) -> None:
        pass
    
    url = "https://hooks.slack.com/services/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"
    title = (f"Bitcoin Predictor Validation Failure")
    slack_data = {}
    columns = ['time_period_start', 'time_period_end', 'time_open', 'time_close', 'price_open', 'price_high', 'price_low', 'price_close', 'volume_traded', 'trades_count']
    unique_columns = ['time_period_start', 'time_period_end']
        
    @classmethod
    def slack_notification(self, error_msg, requestId):
        self.slack_data = {
            "username": "BitcoinPredictorBot",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": self.title + " - Request ID: " + requestId,
                            "value": error_msg,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(self.slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(self.url, data=json.dumps(self.slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        
    @classmethod
    def validate_input_data(self, input_data):
        missing_columns = []
        
        for header in self.columns: 
            if header not in input_data.columns: 
                missing_columns.append(header) 

        # Accuracy Checks
        if missing_columns:
            missing_columns_str = ", ".join(str(x) for x in missing_columns)
            raise Exception("missing columns - " + missing_columns_str)
        
        if input_data.shape[0] < 60:
            raise Exception("not enough input rows provided")
        
        # Completeness Check
        if input_data.isnull().values.any():
            raise Exception("missing values detected in request file")
        
        # Uniqueness Check
        for header in self.unique_columns:
            if input_data[header].duplicated().any():
                raise Exception("duplicate values detected in column " + header)
            
    @classmethod
    def exception_generator(self, error_msg, requestId, app):
        self.slack_notification(error_msg, requestId)
        app.logger.error(error_msg + ", Request ID: " + requestId)
        return make_response({"requestId": requestId, "message": error_msg}, 400)