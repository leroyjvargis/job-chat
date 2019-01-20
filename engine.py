from google.cloud import datastore
from collections import Counter

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

def calcExp(years):
    if int(years) > 8:
        return "senior"
    elif int(years) > 3:
        return "medium"
    else:
        return "fresher"

def parseWebhookRequest(req):
    parsed = {
        "role": req["queryResult"]["outputContexts"][0]["parameters"]["job_role"],
        "jobType": req["queryResult"]["outputContexts"][0]["parameters"]["job_role"],
        "experience": calcExp(req["queryResult"]["outputContexts"][0]["parameters"]["experience"]),
        "skills": req["queryResult"]["outputContexts"][0]["parameters"]["skills.original"],
        "education": req["queryResult"]["outputContexts"][0]["parameters"]["educationLevel.original"]
    }
    return parsed

def constructWebhookResponse(results):
    recommendations = []
    for each in results:
        print (each['company'], each['similarityScore'])
    for each in results:
        obj = {
            "optionInfo": {"key": each["company"]+each["role"] },
            "title": each["company"],
            "description": each["role"],
            "openUrlAction": {
                    "url": each["uri"]
                  }
        }
        recommendations.append(obj)
        
    response = {
        "fulfillmentText": "This is the recommendation list",
        "fulfillmentMessages": [
            {
            "card": {
                "title": "Recommendations",
                "subtitle": "Here are the recommendations based on your profile",
                "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                "buttons": [
                {
                    "text": "View recommendations",
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
                            "textToSpeech": "These are your top 5 recommendations",
                            "displayText":  "These are your top 5 recommendations"
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
def findsum(d,userdict):
    totalsum = 0
    for value in userdict.values():
        for value1 in d.values():
            if value == value1 :
                totalsum = totalsum + 1
    return totalsum

def findsumwordcount(d,userjobdesc):
    count = {}
    for skill in userjobdesc:
        for k,v in d.items():
            if skill in k:
                count[skill] = v
    sumwordcount = 0
    for val in count.values():
        sumwordcount = sumwordcount + int(val)
    return sumwordcount

def getResults(searchQuery):
    allRecords = getRecordsFromDB(searchQuery)
    userSkills = searchQuery["skills"].split()

    for eachJob in allRecords:
        count_of_tokens_job = Counter(eachJob["description"].split())
        d = dict(count_of_tokens_job)

        eachJob['similarityScore'] = findsumwordcount(d, userSkills) + findsum(eachJob, searchQuery)

    allRecords = sorted(allRecords, key=lambda k: k['similarityScore'], reverse = True)

    return constructWebhookResponse(allRecords[:5])