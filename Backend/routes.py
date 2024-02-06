from flask import Flask, request, jsonify
from serverModel import RobotCommServer

app = Flask(__name__)

@app.route("/",  methods = ["GET", "POST"])
def FaceSimilarity():
    requestData = request.form if request.method == "POST" else request.args
    server = RobotCommServer()
    response, retry = server.PredictionProcedure(requestData)
    return jsonify({
        'message':response,
        'retry':retry,
        'status':200  
    })


if __name__ == '__main__':
    app.run()