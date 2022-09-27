from flask import Flask, render_template, request, send_file
from datetime import datetime
import converter1s
import converter5m
import os

app = Flask(__name__)
FORMAT = "%Y-%m-%dT%H:%M"

def appender(par, param):
    if par == "on":
        param.append(1)
    else:
        param.append(0)

@app.route('/')
def index():
    return render_template('ZEDI_form.html')

@app.route('/', methods = ['POST'])
def getvalue():
    # start_date_time = request.form['s_date']
    # end_date_time = request.form['e_date']
    start_date_time_1s = datetime.strptime(request.form['s_date_1s'], FORMAT)
    end_date_time_1s = datetime.strptime(request.form['e_date_1s'], FORMAT)
    node = request.form.get('node_no_field')
    #print(node)
    params_1s = []
    appender(request.form.get('curr_field'), params_1s)
    appender(request.form.get('volt_field'), params_1s)
    appender(request.form.get('freq_field'), params_1s)
    appender(request.form.get('pow_field'), params_1s)
    #print(params_1s)

    converter1s.create_file_1s(start_date_time_1s, end_date_time_1s, params_1s, node)

    start_date_time_5m = datetime.strptime(request.form['s_date_5m'], FORMAT)
    end_date_time_5m = datetime.strptime(request.form['e_date_5m'], FORMAT)
    params_5m = []
    appender(request.form.get('temp_field'), params_5m)
    appender(request.form.get('hum_field'), params_5m)
    appender(request.form.get('pres_field'), params_5m)
    appender(request.form.get('aqi_field'), params_5m)
    appender(request.form.get('co2_field'), params_5m)
    appender(request.form.get('pir1_field'), params_5m)
    appender(request.form.get('pir2_field'), params_5m)

    converter5m.create_file_5m(start_date_time_5m, end_date_time_5m, params_5m, node)
    return render_template("ZEDI_pass.html")


@app.route('/download_1s')
def download_1s():
    file = "data1s.csv"
    return send_file(file, as_attachment = True)


@app.route('/download_5m')
def download_5m():
    file = "data5m.csv"
    return send_file(file, as_attachment = True)


if __name__ == '__main__':
    app.run(debug = True)
