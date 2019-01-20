from google.cloud import datastore

### Datastore 
def getRecordsFromDB(searchQuery):
    #connect to datastore
    client = datastore.Client()
    query = client.query(kind='jobs')
    return (list(query.fetch()))

def addRecord(record):
    client = datastore.Client()
    key = client.key('jobs')

    job = datastore.Entity(
        key, exclude_from_indexes=['description'])

    job.update(record)

    client.put(job)
### END DataStore 

### Webhook

def parseWebhookRequest(req):
    # code goes here
    s = ''

def constructWebhookResponse():
    results = getResults('')
    recommendations = []
    for each in results:
        obj = {
            "optionInfo": {"key": each["company"] },
            "title": each["company"],
            "description": each["uri"]
        }
        recommendations.append(obj)
        
    response = {
        "fulfillmentText": "This is the recommendation list",
        "fulfillmentMessages": [
            {
            "card": {
                "title": "card title",
                "subtitle": "card text",
                "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                "buttons": [
                {
                    "text": "button text",
                    "postback": "https://assistant.google.com/"
                }
                ]
            }
            }
        ],
        "source": "hackaz-229118.appspot.com/",
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                "items": [
                    {
                    "simpleResponse": {
                        "textToSpeech": "These are your top 5 recommendations"
                    }
                    }
                ]
                },
                "systemIntent": {
                "intent": "actions.intent.OPTION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                    "listSelect": {
                    "title": "Jobs",
                    "items": recommendations
                    }
                }
                }
            }
        }
    }

    return response

### END Webhook

### Business Logic

def getResults(searchQuery):
    allRecords = getRecordsFromDB(searchQuery)
    return allRecords

