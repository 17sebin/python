from flask import Flask, render_template, request, send_file
import feedparser, os
import pandas as pd
import Merger
import logging
from flask_cors import CORS
from datetime import datetime

file_name = ""
app = Flask(__name__)
CORS(app)
# 로깅 레벨을 DEBUG로 설정
app.logger.setLevel(logging.DEBUG)

# 파일 핸들러를 추가하여 모든 로그를 파일에 기록
file_handler = logging.FileHandler('access.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

@app.route('/')
def index():
    client_ip = request.remote_addr
    
    app.logger.debug(f'IP : {client_ip} TimeStamp: {timestamp}')
    return render_template("index3.html")


@app.route('/process', methods=['POST','GET'])
def process():
    global file_name,timestamp
    file = request.files['file']
    if file is None:
        return render_template("index3.html")
    
    file_name = file.filename
    File = Merger.File(file,file.filename)
    File.extension()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    if file.filename.endswith(".log"):
        return render_template('download.html')
    
    return render_template('index3.html')


@app.route('/indata', methods=["POST","GET"])
def insert_data():
    query = request.form.get('input_data')
    if query is None:
        return render_template('sql_injection.html')
    QR = Merger.DBConnect().inData(query, datetime.now().strftime('%Y-%m-%d'))
    print(query)
    return render_template('index.html')

@app.route('/index3', methods=["POST","GET"])
def index3():
    return render_template('index3.html')

@app.route('/download', methods=["GET", "POST"])
def download():
    print(os.path.join(f'{timestamp}_{file_name}_report.pdf'))
    return send_file(os.path.join(f'{timestamp}_{file_name}_report.pdf'),as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
