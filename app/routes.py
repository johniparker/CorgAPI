import sys
import os
import flask
from flask import Flask, render_template, request
import requests
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from CorgAPI.database.rds_conn import create_conn
from CorgAPI.model.reg_model import RacetimePredictor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

predictor = RacetimePredictor()

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_racetime = None
    #if the request is sent using post
    if request.method == 'POST':
        #if we find age in the api:
        ui_age  = int(request.form['ui_age'])
        ui_weight = int(request.form['ui_weight'])
        ui_breed = request.form['ui_breed']
        ui_gender = request.form['ui_gender']
        user_features = pd.DataFrame({
            'age': [ui_age], 
            'weight':[ui_weight], 
            'breed': [ui_breed], 
            'gender': [ui_gender]
        })
        print(f"received user input: {ui_age}, {ui_weight}, {ui_breed}, {ui_gender}")
        
        #retrieve average racetime from database
        conn = create_conn()
        avg_query = """
        select avg(racetime)
        from outcome;
        """
        avg_result = pd.read_sql(avg_query, conn)
        avg_racetime = int(avg_result.values)
        conn.close()
        
        #predict racetime based on user input
        predicted_racetime = predictor.predict_racetime(user_features)
        
        #calculate difference between average and prediction
        diff = predicted_racetime - avg_racetime
        diff = round(diff, 2)
        
        #configure what the user sees
        if diff > 0:
            over_under = f"above average by {diff} seconds."
        elif diff < 0:
            over_under = f"below average by {abs(diff)} seconds."
        else:
            over_under = f"close to average."
        
        return render_template('index.html', predicted_racetime=predicted_racetime, over_under=over_under)
    #if get request or another error, render template without data
    return render_template('index.html', data=None, user_input=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)
