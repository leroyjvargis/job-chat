from google.cloud import datastore

def logRequest(jsonR):
    client = datastore.Client()
    key = client.key('log')
    record = {
        "response": str(jsonR)
    }

    log = datastore.Entity(key)

    log.update(record)
    client.put(log)