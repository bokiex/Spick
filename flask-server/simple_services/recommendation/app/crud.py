from sqlalchemy.orm import Session
import models, schemas
import requests as rq
from flask_cors import CORS
from flask import Flask, request, jsonify
import os, sys
import json
from fastapi.encoders import jsonable_encoder
api_key = "AIzaSyBVwaHGbGTnc-cQHpIM6qqMbGIb7C-xKVA"

"""
format of input
{
    "type": "Picnic",
    "township": "Jurong"
}
format of output of Places API
{
    "code": 201,
    "data": {
        "places": [
            {
                "displayName": {
                    "languageCode": "en",
                    "text": "Pandan Reservoir Park"
                },
                "formattedAddress": "700 W Coast Rd, Singapore 608785"
            },            
            {
                "displayName": {
                    "languageCode": "en",
                    "text": "Jurong Lake Gardens"
                },
                "formattedAddress": "Yuan Ching Rd, Singapore"
            },
        ]
    }
}    

format of output of recommendation
{
    "data": 
    [
        {
            "recommendation_id": 1,
            "event_id": 1,
            "recommendation_name": "Pandan Reservoir Park",
            "recommendation_address": "700 W Coast Rd, Singapore 608785"
        },            
        {
            "recommendation_id": 2,
            "event_id": 1,
            "recommendation_name": "Jurong Lake Gardens",
            "recommendation_address": "Yuan Ching Rd, Singapore"
        },
    ]
}
"""
def get_recommendation( search):
    # Simple check of input format and data of the request are JSON
  
        try:
            
            print("\nReceived search terms in JSON:", search)

            # 1. Send search info
            result = processSearch(search)

            # 2. Save the result to the database
            result = jsonable_encoder(result)
            res = []
            for i in result['data']['places']:
                recommendation_name = i['displayName']['text']
                recommendation_address = i['formattedAddress']
                recommendation = {
                    "recommendation_name": recommendation_name,
                    "recommendation_address": recommendation_address
                }
                recommendation = schemas.Recommendation(**recommendation)
                res.append(recommendation)
            return res
            #     create_recommendation(db, recommendation)

            # # 3. Return the result
            # return db.query(models.Recommendation).all()

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonable_encoder({
                "code": 500,
                "message": "recommendation.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    # return jsonify({
    #     "code": 400,
    #     "message": "Invalid JSON input: " + str(request.get_data())
    # }), 400

def processSearch(search):
    url = "https://places.googleapis.com/v1/places:searchText"
    # placeholder data
    search = jsonable_encoder(search)
    searchstr = search["type"] + "near" + search["township"]
  
    data = {"textQuery" : searchstr}
    json_data = json.dumps(data)
    headers = {'Content-Type':'application/json', 'X-Goog-Api-Key':api_key, 
               'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel'}
    print('\n-----calling places API-----')
    reply = rq.post(url, data = json_data, headers=headers)
    response = reply.json()

    print('search_result:', response)
    
    try:
        return {
            "code": 201,
            "data": response
        }

    except:
        return response["error"]
    

def create_recommendation(db: Session, recommendation: schemas.Recommendation):
    if db.query(models.Recommendation).filter(models.Recommendation.location_name == recommendation.location_name).first() \
    and db.query(models.Recommendation).filter(models.Recommendation.event_id == recommendation.event_id).first():
        return None
    db_recommendation = models.Recommendation(**recommendation.dict())
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

def get_recommendation_by_id(db: Session, event_id: int):
    return db.query(models.Recommendation).filter(models.Recommendation.event_id == event_id).first()

def delete_recommendation(db: Session, event_id: int):
    db_recommendation = db.query(models.Recommendation).filter(models.Recommendation.event_id == event_id).all()
    for i in db_recommendation:
        db.delete(i)
    db.commit()
    return db_recommendation