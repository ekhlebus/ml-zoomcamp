# Here we are turning ping function into a web service using Flask

from flask import Flask

app = Flask('ping')

# Add decorator to add extra functionality to ping function (here it allows us to turn function into web service)
@app.route('/ping', methods=['GET'])  # This function will be accessible at address /ping using GET method

# Making ping function
def ping():
    return "PONG"

# We are using "__main__" top-level script environment to run the app
if __name__ == "__main__":
    # Run the app on port 9696 at localhost in debug mode
    app.run(debug=True, host='0.0.0.0', port=9696) 