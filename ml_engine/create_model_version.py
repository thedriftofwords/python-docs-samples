#!/bin/python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Creating model and version resources in Cloud ML Engine.

For prerequisites, setup and more details:
https://cloud.google.com/ml-engine/docs/tensorflow/python-guide

API reference for models and versions:

https://cloud.google.com/ml-engine/reference/rest/v1/projects.models
https://cloud.google.com/ml-engine/reference/rest/v1/projects.models.versions
'''

from googleapiclient import discovery
from googleapiclient import errors
# Time is for waiting until the request finishes, 
# and (optionally) for naming models and versions.
import time

# To authenticate set the environment variable
# GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>

# Fill in your project name, model name and version name.
projectID = 'projects/{}'.format('<your_project_name>')
modelName = '<your_model_name>' + time.strftime("%Y%m%d_%H%M%S")
modelID = '{}/models/{}'.format(projectID, modelName)
versionName = '<your_version_name>' + time.strftime("%Y%m%d_%H%M%S")

# The version description is optional.
versionDescription = '<your_version_description>'

# Specify the directory in your GCS bucket that contains your model.
trainedModelLocation = 'gs://<gcs_path_to_model_directory>/'

runtimeVersion = '1.10'

ml = discovery.build('ml', 'v1')

# Create a dictionary with the fields from the request body.
requestDict = {'name': modelName,
    'description': 'Another model for testing.'}

# Create a request to call projects.models.create.
# Skip this if you want to use an existing model.
request = ml.projects().models().create(parent=projectID,
                            body=requestDict)
                            
# Make the call.
try:
    response = request.execute()

    # Any additional code on success goes here (logging, etc.)

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the model.' +
        ' Check the details:')
    print(err._get_reason())
    
    # Clear the response for next time.
    response = None

# Specify 'framework' if you are using scikit-learn or XGBoost.
# For example, 'framework': 'SCIKIT_LEARN'
# Info on other settings: 
# https://cloud.google.com/ml-engine/reference/rest/v1/projects.models.versions#resource-version
requestDict = {'name': versionName,
    'description': versionDescription,
    'deploymentUri': trainedModelLocation,
    'runtimeVersion': runtimeVersion}

# Create a request to call projects.models.versions.create
request = ml.projects().models().versions().create(parent=modelID,
              body=requestDict)

# Make the call.
try:
    response = request.execute()

    # Get the operation name.
    operationID = response['name']

    # Any additional code on success goes here (logging, etc.)

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the version.' +
          ' Check the details:')
    print(err._get_reason())

    # Handle the exception as makes sense for your application.

done = False
request = ml.projects().operations().get(name=operationID)

while not done:
    response = None

    # Wait for 300 milliseconds.
    time.sleep(0.3)

    # Make the next call.
    try:
        response = request.execute()

        # Check for finish.
        done = response.get('done', False)

    except errors.HttpError as err:
        # Something went wrong, print out some information.
        print('There was an error getting the operation.' +
              'Check the details:')
        print(err._get_reason())
        done = True
