from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import schemas
from fastapi.responses import JSONResponse
import json
import requests as rq
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI()



@app.exception_handler(Exception)
async def exception_handler(request, exc):

    return JSONResponse(
        status_code=500, content={"message": request.url.path + " " + str(exc)}
    )


api_key = environ.get("PLACES_API_KEY")

"""
format of input
{
    "type": "Picnic",
    "township": "Jurong"
}
format of output of Places API
    {
        "places": [
            {
                "displayName": {
                    "languageCode": "en",
                    "text": "Legendary Hong Kong Restaurant @ Jurong Point 香港傳奇餐廳"
                },
                "formattedAddress": "63 Jurong West Central 3, #03-80 Jurong Point, Singapore 648331",
                "photos": [
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Ivan Lee",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjUvaKxszLtanzz9hG5wf65ikSaypDR_zWVAw9D233g17fJ9=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/101135338517333595967"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJYKMQurCGp_GqLeNFIMf8zLwD6rt9U0Iu7Iz0O3l2jLNTHWZPQkm8alGMym998W0Go4gyF0SbjrbvTxlYqSB_fNAV5NhNbmP2169SAwgZ983CErInGozxTdH_waiB1CcXQM7YMJQ9fzJ1PDP2nAOSfzE1cxhVrYWUny",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Keith",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWUssYieNJnbDxjyDfyIqDZFs-WDVlx8xlkZg5vCXpSEOa-=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/110168692495164481446"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZi4oTz5z2zBIBq6toDrz7AMbNIAeZJpR7Fs5ZGEhgBPl2LSNHtFxrcqNf_ba7d_FgFQ7Dj-xPi7V_SK701DQyYvdVMUTWe9NufqFc1Db4Sf4t6gUwFAiYBiLZpL9M_vFQL8zThSWybiwvziMedqUZ5h6kzK4uNBB_A",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Wayne Yap",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWPFlXSIhUx58_1i-ZXoQrvGICzv803vF7WGKNY_SbIqRQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111810540736089563526"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJb4Wro0zz84NNOQKgXP1DrXaI1kodOHbmh1BtHd9eZ541BeNf_O4kn7zCe-OFhJ7jswoBxTSQhcmIzq5rij7CkdHLRm9-8o9rzmOd0liHx0yii-C79FTZ36t53OphMVsVqYeBiUeTNJXFd43-K8scp0YTba5cD_dnMf",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Scribbling Geek",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjV07GEEH4qvC3SNxbLyuTpn6AVm4yRNnpOOr89etwhG9MI=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111562642484326521942"
                            }
                        ],
                        "heightPx": 1351,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJYTfCY3WStV7lJJVq_f3twcq3m4P1qNSarzOP0HmZnNQygZ2VAAVsfWlNARJtPmv04-v6voqYnr-1EFlLO1jBfRpQPm5jD-IG5jFZ5zpxxDWtI3eDGETaEBmQXGci761-Hcz4POWsMf17bHaxACvBwCAn-NrOy3NOi6",
                        "widthPx": 2400
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "john hooi",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjUMLsDabJbvlkRyvciCS8ephq3zDPmMrVlKqwS7Dw2DnWw=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/109443203021442431817"
                            }
                        ],
                        "heightPx": 3000,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZwlTm-mpa3lPojyS0601ZBfmpI2t4UzZaXGfWNrqXrtQ5oxDYvL53IPuHQ4M7OuuqZnwMKRuKoytVVAT1MIZxjl4l5xFlrLQNsz9Y3qOiP7e4C4LQtEYPFv4sHwuMX830Q_gGQWpKo3G2E0IVj6K3ygJ9FjyxkM4B4",
                        "widthPx": 4000
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Sandy Ng",
                                "photoUri": "//lh3.googleusercontent.com/a/ACg8ocKZISO5-8OFYfL8nT9Ewur0YQynw-jYEhmTqc2XHGX05w=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/106641330710883048209"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJab9JwXe0PlrkhoH593DVeaMl1t-0mRXIIQY75RLyZQOHm6dXv92bg9pWSCvSBjAzhmtOFSaXLayS6Z6Mb_JIHsxae7cPtVjTkKilqbp4MhSrUpcyfw2U0tOatJay4aYlkiNjUNhT6RGYG5sSgPU_a-njpNJIPyoOf3",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "J T",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVygnZWfna5sgtCM5JIA4u1ENXXBtLok2iVfe1MXsjWwJU=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/102370977106040806036"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZYcPg7-K-gFEEU3TmyMPsHx5eIOPqdXMu-h7k_QaUO_4cQpqNexNt4G3Yzi-ivEqD1uSNhhl-j2F9B6nNvCj0dDFXPvMg635wc0l75y3X4jjLMn-FUZfwmQm0dZPtaPy7ksbiSWsWK30lbOCpflJAaM1LaBuCPZsFl",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Wayne Yap",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWPFlXSIhUx58_1i-ZXoQrvGICzv803vF7WGKNY_SbIqRQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111810540736089563526"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJa-qd7_o_WCF9eSYqb9UC4FgIm288asuE4hl0sr2kBxNcNPhDzzrBDLz_VTmbwKjHxVrkLhTU9j4yxNNp4aVsrMF9xrpANsTPjv7pCFGY9CcdjSxj6kbbiH5fVPeUDkttXA_GEiEt_uQqclu7AbwU0Kq0Lz9EbE9vTd",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Florence Wong",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVCLcK2XbnxfeSanNRKuDrx1OkpfEgiMT0j8QOT1fYGUQrQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/116520981894085487207"
                            }
                        ],
                        "heightPx": 3000,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJb6St4Co4WvCq4_tC20Uofd4WywqT0dQciY2Xf5yZKf-eMKuaGSVbwJmroJUtcK6iLwk-mfIj9l1j_uvbbLkG_fOAmqeXkyPlTy3ZDZ51i2llFWIJDnY8U84MUXu86qTJQCHy5ofGCMJ5_TuAsCI93mT2CRCOki0KU5",
                        "widthPx": 4000
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "swee sin eng",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVlC7RNCIQsGtSx02rzKKoN_XM0d8ivHUa3Tggth8B0hQOB=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/113684571018749328949"
                            }
                        ],
                        "heightPx": 2736,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJa9KjZVkq25j57XTbLhPQUmaBV9OwwLezhPCgcMmM0UDPFprS1Qdkx0xs7Uhq8v-zUFYDxl8wHqpgslWaOXEXwYtA6LmB7epCKVBAW6oJiThm09AkoCC-1QO6s4G6-4MUqu89Y_Uz6SjderObagNXnlkYg8CmYvyNOo",
                        "widthPx": 3648
                    }
                ],
                "priceLevel": "PRICE_LEVEL_MODERATE",
                "rating": 4.1
            }
        ]
     }

format of output of recommendation
{
    "code": 201,
    "data": {
        "places": [
            {
                "displayName": {
                    "languageCode": "en",
                    "text": "Legendary Hong Kong Restaurant @ Jurong Point 香港傳奇餐廳"
                },
                "formattedAddress": "63 Jurong West Central 3, #03-80 Jurong Point, Singapore 648331",
                "photos": [
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Ivan Lee",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjUvaKxszLtanzz9hG5wf65ikSaypDR_zWVAw9D233g17fJ9=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/101135338517333595967"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJYKMQurCGp_GqLeNFIMf8zLwD6rt9U0Iu7Iz0O3l2jLNTHWZPQkm8alGMym998W0Go4gyF0SbjrbvTxlYqSB_fNAV5NhNbmP2169SAwgZ983CErInGozxTdH_waiB1CcXQM7YMJQ9fzJ1PDP2nAOSfzE1cxhVrYWUny",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Keith",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWUssYieNJnbDxjyDfyIqDZFs-WDVlx8xlkZg5vCXpSEOa-=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/110168692495164481446"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZi4oTz5z2zBIBq6toDrz7AMbNIAeZJpR7Fs5ZGEhgBPl2LSNHtFxrcqNf_ba7d_FgFQ7Dj-xPi7V_SK701DQyYvdVMUTWe9NufqFc1Db4Sf4t6gUwFAiYBiLZpL9M_vFQL8zThSWybiwvziMedqUZ5h6kzK4uNBB_A",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Wayne Yap",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWPFlXSIhUx58_1i-ZXoQrvGICzv803vF7WGKNY_SbIqRQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111810540736089563526"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJb4Wro0zz84NNOQKgXP1DrXaI1kodOHbmh1BtHd9eZ541BeNf_O4kn7zCe-OFhJ7jswoBxTSQhcmIzq5rij7CkdHLRm9-8o9rzmOd0liHx0yii-C79FTZ36t53OphMVsVqYeBiUeTNJXFd43-K8scp0YTba5cD_dnMf",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Scribbling Geek",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjV07GEEH4qvC3SNxbLyuTpn6AVm4yRNnpOOr89etwhG9MI=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111562642484326521942"
                            }
                        ],
                        "heightPx": 1351,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJYTfCY3WStV7lJJVq_f3twcq3m4P1qNSarzOP0HmZnNQygZ2VAAVsfWlNARJtPmv04-v6voqYnr-1EFlLO1jBfRpQPm5jD-IG5jFZ5zpxxDWtI3eDGETaEBmQXGci761-Hcz4POWsMf17bHaxACvBwCAn-NrOy3NOi6",
                        "widthPx": 2400
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "john hooi",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjUMLsDabJbvlkRyvciCS8ephq3zDPmMrVlKqwS7Dw2DnWw=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/109443203021442431817"
                            }
                        ],
                        "heightPx": 3000,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZwlTm-mpa3lPojyS0601ZBfmpI2t4UzZaXGfWNrqXrtQ5oxDYvL53IPuHQ4M7OuuqZnwMKRuKoytVVAT1MIZxjl4l5xFlrLQNsz9Y3qOiP7e4C4LQtEYPFv4sHwuMX830Q_gGQWpKo3G2E0IVj6K3ygJ9FjyxkM4B4",
                        "widthPx": 4000
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Sandy Ng",
                                "photoUri": "//lh3.googleusercontent.com/a/ACg8ocKZISO5-8OFYfL8nT9Ewur0YQynw-jYEhmTqc2XHGX05w=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/106641330710883048209"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJab9JwXe0PlrkhoH593DVeaMl1t-0mRXIIQY75RLyZQOHm6dXv92bg9pWSCvSBjAzhmtOFSaXLayS6Z6Mb_JIHsxae7cPtVjTkKilqbp4MhSrUpcyfw2U0tOatJay4aYlkiNjUNhT6RGYG5sSgPU_a-njpNJIPyoOf3",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "J T",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVygnZWfna5sgtCM5JIA4u1ENXXBtLok2iVfe1MXsjWwJU=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/102370977106040806036"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJZYcPg7-K-gFEEU3TmyMPsHx5eIOPqdXMu-h7k_QaUO_4cQpqNexNt4G3Yzi-ivEqD1uSNhhl-j2F9B6nNvCj0dDFXPvMg635wc0l75y3X4jjLMn-FUZfwmQm0dZPtaPy7ksbiSWsWK30lbOCpflJAaM1LaBuCPZsFl",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Wayne Yap",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjWPFlXSIhUx58_1i-ZXoQrvGICzv803vF7WGKNY_SbIqRQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/111810540736089563526"
                            }
                        ],
                        "heightPx": 3024,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJa-qd7_o_WCF9eSYqb9UC4FgIm288asuE4hl0sr2kBxNcNPhDzzrBDLz_VTmbwKjHxVrkLhTU9j4yxNNp4aVsrMF9xrpANsTPjv7pCFGY9CcdjSxj6kbbiH5fVPeUDkttXA_GEiEt_uQqclu7AbwU0Kq0Lz9EbE9vTd",
                        "widthPx": 4032
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "Florence Wong",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVCLcK2XbnxfeSanNRKuDrx1OkpfEgiMT0j8QOT1fYGUQrQ=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/116520981894085487207"
                            }
                        ],
                        "heightPx": 3000,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJb6St4Co4WvCq4_tC20Uofd4WywqT0dQciY2Xf5yZKf-eMKuaGSVbwJmroJUtcK6iLwk-mfIj9l1j_uvbbLkG_fOAmqeXkyPlTy3ZDZ51i2llFWIJDnY8U84MUXu86qTJQCHy5ofGCMJ5_TuAsCI93mT2CRCOki0KU5",
                        "widthPx": 4000
                    },
                    {
                        "authorAttributions": [
                            {
                                "displayName": "swee sin eng",
                                "photoUri": "//lh3.googleusercontent.com/a-/ALV-UjVlC7RNCIQsGtSx02rzKKoN_XM0d8ivHUa3Tggth8B0hQOB=s100-p-k-no-mo",
                                "uri": "//maps.google.com/maps/contrib/113684571018749328949"
                            }
                        ],
                        "heightPx": 2736,
                        "name": "places/ChIJHcaYLpMP2jERjhDMRZ9A7-k/photos/ATplDJa9KjZVkq25j57XTbLhPQUmaBV9OwwLezhPCgcMmM0UDPFprS1Qdkx0xs7Uhq8v-zUFYDxl8wHqpgslWaOXEXwYtA6LmB7epCKVBAW6oJiThm09AkoCC-1QO6s4G6-4MUqu89Y_Uz6SjderObagNXnlkYg8CmYvyNOo",
                        "widthPx": 3648
                    }
                ],
                "priceLevel": "PRICE_LEVEL_MODERATE",
                "rating": 4.1
            }
        ]
     }
}
"""
def processSearch(search):
    url = "https://places.googleapis.com/v1/places:searchText"

    search = jsonable_encoder(search)
    searchstr = search["type"] + "near" + search["township"]

    data = {"textQuery" : searchstr, "maxResultCount": 3}
    json_data = json.dumps(data)
    headers = {'Content-Type':'application/json', 'X-Goog-Api-Key':api_key, 
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.photos,places.rating'}
    print('\n-----calling places API-----')
    reply = rq.post(url, data = json_data, headers=headers)
    response = reply.json()

    print('\nSearch_result:', response)
    return response

def processImage(resource_name):
    url = "https://places.googleapis.com/v1/" + resource_name + "/media?maxHeightPx=400&maxWidthPx=400&key=" + api_key
    return url
   

@app.get("/online")
def online():
    return {"message": "Recommendation service is online."}

# Get recommendations from Places API
@app.post("/recommendation", response_model=list[schemas.Recommendation])
def get_recommendation( search: schemas.Search):

    # Simple check of input format and data of the request are JSON
    print("\nReceived search terms in JSON:", search)

    # 1. Send search info

    result = processSearch(search)
    print("\nReceived search results in JSON:", result)
    # 2. Save the result to the database
    result = jsonable_encoder(result)
    
    res = []

    for i in result['places']:
        print("\nPlace:", i)
        recommendation_name = i['displayName']['text']
        recommendation_address = i['formattedAddress']
        recommendation_photo = processImage(i['photos'][0]['name'])
  
        
        recommendation = {
            "recommendation_name": recommendation_name,
            "recommendation_address": recommendation_address,
            "recommendation_photo" : recommendation_photo,
        
        }

        recommendation = schemas.Recommendation(**recommendation)
    
        res.append(recommendation)
        print("\nRecommendation:", recommendation)
    return res

    

    


