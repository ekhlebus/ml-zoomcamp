import pickle

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'churn_prediction_model_C=1.0.bin'

# Loading previously saved pre-trained model and DictVectorizer
with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('churn') # Creating a Flask web service named 'churn'

@app.route('/predict', methods=['POST']) # WE use POST method to be able to send customer data
# Defining predict function which will get customer data from request and return churn probability
def predict():
    customer = request.get_json() # Getting customer data from json request as a python dictionary

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    
    # Make a churn decision based on probability and defined threshold
    churn = y_pred >= 0.5 

    # Preparing the result as a json response
    result = {
        'churn_probability': float(y_pred), ## we need to cast numpy float type to python native float type
        'churn': bool(churn) # Converting numpy types to native Python types
    }

    return jsonify(result)  # Returning the result as a json response (send back the data in json format to the user)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)