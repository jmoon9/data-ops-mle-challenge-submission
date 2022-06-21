# data-ops-mle-challenge

Hi there!

Here's a quick challenge for you to demonstrate your skills as a DataOps or Machine Learning Engineer. This is intended to be quick, light, easy, and fun - don't stress or spend too much time here! When done, feel free to share your solution via Github or other version control system.

## Problem

We have a sample model for predicing the price of Bitcoin in the next second based on the prices from the last 60 seconds whipped up by one of our data scientists - this is a quick and dirty model, wrapped in a quick and dirty API, packaged into a quick and dirty container, and we've decided to YOLO and test in prod.

Tasks:
* This is really quick and dirty - how would you do this better?
    Changes made to app.py:
        - Loaded h5 model in place of protocol buffer
            ○ Predict method of protobuf model was unrecognized in flask

        - Flask input updated to multipart/form-data to support input csv
            ○ Smaller payloads --> generate tensors in flask app
            
        - Response Payload changed:
            ○ evaluation --> RMSE
            ○ prediction --> serialized tensor

        - Input data quality tests:
            ○ Accuracy --> check for expected fields and at least 60 records 
            ○ Completeness --> check for missing values or records
            ○ Uniqueness --> check for duplicate/overlapping values for time period input variables
            
        - Slack notifications for data quality check failures
            ○ Slack webhook integration

    Changes to Dockerfile:
    	- Expose port 5000
	    - Copy /model/ directory to docker volume

    EC2 Hosting:
        - Create Docker image on EC2
        - Run container with port map to 5000
        - Container availability testing:
            ○ Linux cron job to execute python script
            ○ Ping test on container GET method
            ○ Data persistence in instance EBS to avoid duplicate notifications in event of container failure (24 hour periods)

    Invoking the endpoint (Postman collection included):
        - Container hosted on EC2 with public IP http://3.144.206.118:5000/
            - /predict --> 
                - accepts csv file with content type multipart/form-data
                    - Must include column headers: ['time_period_start', 'time_period_end', 'time_open', 'time_close', 'price_open', 'price_high', 'price_low', 'price_close', 'volume_traded', 'trades_count']
                    - Must contain at least 60 records
                    - Must contain no duplicates in either column time_period_start or time_period_end
                - returns RMSE and serialized prediction ndarray

    Alternate approach (production deployment strategy):
        - Full CI/CD pipelines for dev/uat/prod environments
            - Jenkins pipeline to run Terraform deployments for AWS Sagemaker Endpoints
        - Sagemaker configuration --> signed requests to endpoint
            - Inference Endpoint --> two options
                - Real-time inference --> if sending csv data under 5 MB as request payload
                    - Preprocessing script runs input data validations, constructs prediciton input tensors
                - Async inference --> if sending tensor data over 5 MB as 
                    - Inputs and outputs to specified s3 location
                    - Use case limited since results are required in near real time

        - A/B testing for Prod release --> split model traffic in production between new and legacy endpoints
            - Gradually increase traffic to new endpoint as more valid results come in
            - Decommission legacy endpoint when 100% of traffic is routed to new endpoint

    ** I've included a quick mock up of the terraform configuration that would be used to deploy these instances located in the branch "terraform-config" **

* Come up with tests for container or requests failure 
    - EC2 --> cron job runs on 5 minute cadence, sends notification if unavailable. Data persistence on instance will validate our 
    - SageMaker runs automated health checks to endpoints
    
* Come up with tests for data quality in this context 
    - Accuracy --> Are we getting what we expect?
    - Completeness --> Are there null or incomplete records in the input data?
    - Uniqueness --> Are duplicate values or records provided?

* Introduce slack alerts for failure of either of the above. Here's some sample code:
    - Utilized slack incoming webhook App to construct custom error messages based on which test fails
    - Notification includes a request ID which can be referrenced in Flask logs on EC2 instance


Questions for you to consider:

* Does this data set even make sense? What's wrong with it?
* What makes this model unsuitable for inferencing in prod?
    - Security --> no signed requests
    - Validation --> A/B Testing
    - Training data is limited
* How would you validate the model inputs in this container?
    - Custom class for input data validation implements availability, accuracy, completeness, and uniqueness tests
* What happens with this container if the model and API take more than a second to return a response?
    - Results will already be somewhat insignificant as we are trying to predict the price of bitcoin in the next second.

* What would happen if the price of bitcoin suddenly shot up by $10k at 3am? Would this model still be good? How would we catch this?
    - Model would respond poorly to outlier cases due to limited training data
    - We can cache previous predictions and set a specific variance threshold for new results, send a slack notification if threshold hit