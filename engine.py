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
    # toFind = ["job_role", "experience", "skills.original", "educationLevel.original"]
    # stringified = str(req)
    # for each in toFind:
    #     stringified.index(each)

    ops = {"job_role": "hasnotyetbeenadded", "experience": 0, "skills.original": "hasnotyetbeenadded", "educationLevel.original": "hasnotyetbeenadded", }
    for each in req["queryResult"]["outputContexts"]:
        for key, value in each["parameters"].items():
            if key == "job_role" and ops["job_role"] == "hasnotyetbeenadded":
                ops[key] = value
            if key == "experience" and ops["experience"] == "hasnotyetbeenadded":
                ops[key] = value
            if key == "skills.original" and ops["skills.original"] == "hasnotyetbeenadded":
                ops[key] = value
            if key == "educationLevel.original" and ops["educationLevel.original"] == "hasnotyetbeenadded":
                ops[key] = value

    parsed = {
        "role": ops["job_role"],
        "jobType": ops["job_role"],
        "experience": calcExp(ops["experience"]),
        "skills": ops["skills.original"],
        "education": ops["educationLevel.original"]
    }
    return parsed

def constructWebhookResponse(results):
    recommendations = []
    for each in results:
        print (each['company'], each['similarityScore'])
    for each in results:
        obj = {
            #"optionInfo": {"key": each["company"]+each["role"] },
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
            "google":{  
                "expectUserResponse":True,
                "richResponse":{  
                    "items":[
                        {
                            "simpleResponse": {
                                "textToSpeech": "Alright! Here are a few web jobs you might want to check out."
                            }
                        },

                        {  
                            "carouselBrowse":{  
                                "items":recommendations
                            }
                        }
                    ]
                },
                "userStorage":"{\"data\":{}}"
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