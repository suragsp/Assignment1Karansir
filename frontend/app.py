from flask import Flask,render_template,request,jsonify, logging
import requests

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info("--------------------- index.html")
    return render_template('index.html')

@app.route('/add-data',methods=['POST'])
def add_data():
    app.logger.info("frontend -----------------")
    # app.logger.info(request.json)
    print(jsonify(request.json))
    r = requests.post("http://dbapp-service:5000/add-data",json= request.json)
    
    return r.json()
              
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)