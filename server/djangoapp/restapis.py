import requests
import json
from .models import CarModel, CarMake, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json', 'User-Agent': 'Test'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_d = response.json()
    json_data = json.loads(response.text)
    
    return json_d


def reviewcount(url, **kwargs):
    result = get_request(url)
    
    return result['doc_count']

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, params=kwargs, json=json_payload)
    except:
        print('Netwoek error')
        status_code = response.status_code
        print("status code: ", status_code)
    
    return response



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['dbs']['rows']
        print("DEALERS: ")
        print(dealers)
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    
    json_result = get_request(url, {"state": state})
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['dbs']['rows']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealer_id):
# - Call get_request() with specified arguments
    results = []
#    json_result = get_request(url, {dealerId: dealer_id})
    json_result = get_request(url, dealerId=dealer_id)
# - Parse JSON results into a DealerView object list
    print("PERKAUS")
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['dbs']['rows']
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            if dealer_doc['id'] == dealer_id:

                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], zip=dealer_doc["zip"])
                results = dealer_obj
    print(results)
    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):

    results = []
    # Call get_request with a URL parameter
    
    json_result = get_request(url, dealerId=dealerId)
    
    print("PERKAUS")
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result['dbs']
        # For each dealer object
        for rev in reviews:
            # Get its content in `doc` object
            r = rev["doc"]
            if r['dealership'] == dealerId:
                pd = None
                model = None
                make = None
                year = None
                sentimnt = None
                
                if 'purchase_date' in r:
                    pd = r['purchase_date']
                if 'car_make' in r:
                    make = r['car_make']
                if 'car_model' in r:
                    model = r['car_model']
                if 'car_year' in r:
                    year = r['car_year']
                
                snt = analyze_review_sentiments(r['review'])
                
                obj = DealerReview(dealership=r['dealership'], 
                                    name=r['name'], 
                                    purchase=r['purchase'], 
                                    review=r['review'], 
                                    id=r['id'],
                                    purchase_date=pd,
                                    car_make = make,
                                    car_model=model,
                                    car_year=year,
                                    sentiment=snt
                    )   
                                    
                #'purchase_date', r['car_make'], 'model4', '1998', 'senitment', 'id4')
                results.append(obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c30575b5-bfcd-4fd4-b9c5-4ea2cbd5b0ad/v1/analyze"
    watsonapi = "IQZ5n7WJPIEstxVMMDOkGZozTPZmYPY2GrHGFeaYp7yr"
    
    params = {
        'text': text,
        'version': '2020-08-01',
        'features': 'sentiment',
        'return_analyzed_text': True

    }
    resp = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', watsonapi))
    sent = resp.json()
    return sent['sentiment']['document']['label']




