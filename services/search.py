from nltk import word_tokenize, pos_tag, ne_chunk
from db import get_location_outlets, read_kl_outlets, find_latest_closing
import nltk, datetime
from nltk.corpus import wordnet
from fastapi.responses import JSONResponse
from nltk.tree import Tree
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    return tokens

def extract_location_entities(text):
    tokens = word_tokenize(text) 
    tagged_tokens = pos_tag(tokens)
    ne_tree = ne_chunk(tagged_tokens)
    locations = []
    for subtree in ne_tree:
        if isinstance(subtree, Tree) and (subtree.label() == 'GPE' or subtree.label() == 'LOC'):
            locations.append(' '.join([token[0] for token in subtree.leaves()]))
    print("Locations: ", locations)
    return locations

def determine_intent(query):
    tokens = preprocess_text(query)
    loc_entities = extract_location_entities(query) # find location enitites in input

    # Synonyms for the latest closing queries
    latest_closing_keywords = ['latest', 'closing', 'close']
    synonyms=[]
    for word in latest_closing_keywords:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
    latest_closing_keywords.extend(synonyms)

    if any(key in tokens for key in latest_closing_keywords):
        return ['latest_closing', '']
    elif loc_entities:
        return ['outlets_in_location', loc_entities[0]]
    else:
        return 'unknown'
    
def find_latest_closing_outlets():
    kl_outlets = read_kl_outlets()
    latest_time = None
    latest_outlet_coor = ""
    latest_ls = []

    for outlet in kl_outlets:
        try: # to handle outlets without operating hour (opening soon)
            operating_hour = str(outlet[2]).replace("-", "to")
            closing_time_str = operating_hour.lower().replace('(', '').replace(')', '').split('to')[-1].strip()
            
            closing_time = datetime.datetime.strptime(closing_time_str, '%I:%M%p')

            if latest_time == None or closing_time > latest_time:
                latest_time = closing_time_str                
        except Exception as e:
            pass
    
    latest_outlets = find_latest_closing(latest_time.replace(" ", "")) # rm space because there is outlet with "10 PM" and "10PM"
    for outlet in latest_outlets:
        latest_outlet_coor = (outlet[-1], outlet[-2]) # latitude, longitude
        latest_ls.append({"name": outlet[0], "operating_hour": outlet[2], "coordinate": latest_outlet_coor})
    
    return latest_ls

def find_location_outlets(location):
    location_outlets = get_location_outlets(location)
    location_outlets_ls = []
    for outlet in location_outlets:
        outlet_coor = (outlet[-1], outlet[-2]) # latitude, longitude
        location_outlets_ls.append({"name": outlet[0], "coordinate": outlet_coor})
    return location_outlets_ls

def query_handler(query):
    intent = determine_intent(query)

    if intent[0] == 'latest_closing':
        print("latest Closing Outlets")

        latest_closing_outlets = find_latest_closing_outlets()

        resp ={
            "data": latest_closing_outlets
        }
        status = 200
                    
    elif intent[0] == 'outlets_in_location':
        location = intent[1]
        count = 0
        print("Outlets in Location:",location)

        if location:
            q_result = find_location_outlets(location) 
            print(q_result)
            count = len(q_result)
            print("Number of outlets in {}: {}".format(location, count))
        else:
            print("No location found in the query")

        resp ={
            "data": q_result
        }
        status = 200

    else:
        print("unsupported")
        print("intent: ", intent)
        print("query", query)
        resp ={
            "data": ""
        }
        status = 400

    resp["type"] = intent[0] 
    return JSONResponse(content=resp, status_code=status)