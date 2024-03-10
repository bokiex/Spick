import requests as rq
from flask_cors import CORS
from flask import Flask, request, jsonify
import os, sys
import json

app = Flask(__name__)
CORS(app)

@app.route("/recommend", methods=['POST'])
def getrecc():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            search = request.get_json()
            print("\nReceived search terms in JSON:", search)

            # 1. Send search info
            result = processSearch(search)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "recommendation.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processSearch(search):
    url = "https://places.googleapis.com/v1/places:searchText"
    # placeholder data
    searchstr = search["type"] + "near" + search["township"]
    data = {"textQuery" : searchstr}
    json_data = json.dumps(data)
    headers = {'Content-Type':'application/json', 'X-Goog-Api-Key':'AIzaSyCs9PnPDv3KmsDySwW_7SHwG2vLeBwyJJ4', 
               'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel'}
    print('\n-----calling places API-----')
    reply = rq.post(url, data = json_data, headers=headers)
    response = reply.json()

    print('search_result:', response)
    
    try:
        code = response["places"]
        return {
        "code": 201,
        "data": response
        }

    except:
        return response["error"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)