import flask
from flask import Flask, render_template, request
import requests
from CorgAPI.database.rds_conn import create_conn

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET', 'POST'])

def index():
    #if the request is sent using post
    if request.method == 'POST':
        #if we find age in the api:
        ui_age  = int(request.form['ui_age'])
        ui_weight = int(request.form['ui_weight'])
        ui_breed = request.form['ui_breed']
        ui_gender = request.form['ui_gender']
        print(f"received user input: {ui_age}, {ui_weight}, {ui_breed}, {ui_gender}")
        #initiate RDS connection
        conn = create_conn()
    
        if conn:
            #call function to process user input
            processed_data = process_data(user_input, conn)
            conn.close()
            return render_template('index.html', data=processed_data, user_input=user_input)
        else:
            return render_template('index.html', error="Error: Unable to connect to the database.")
    #if get request or another error, render template without data
    return render_template('index.html', data=None, user_input=None, error=None)
def process_data(user_input, conn):
    cursor = conn.cursor()
    sql = f"""
    with cte_age as (
    select corgid
    from corgi
    where age = {user_input}
    )
    select round(avg(racetime),2) 
    from outcome o
    join cte_age a on o.corgid = a.corgid
    ;
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

if __name__ == '__main__':
    app.run(debug=True)
