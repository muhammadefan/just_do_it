import pickle
import numpy as np
import os
from flask import Flask, render_template, request

# load model
model = pickle.load(open('iris.pkl','rb'))

# define template (html file) location
app = Flask(__name__, template_folder=os.getcwd())

# route to home page
@app.route('/')
def main():
    return render_template('home.html')

# route to result page
@app.route('/prediction',methods=['POST'])
def predict():
    sepalLength = request.form['a']
    sepalWidth = request.form['b']
    petalLength = request.form['c']
    petalWidth = request.form['d']

    features = np.array([[sepalLength,sepalWidth,petalLength,petalWidth]])
    prediction = model.predict(features)
    return render_template('result.html', data=prediction)

if __name__ == "__main__":
    app.run(debug=True)