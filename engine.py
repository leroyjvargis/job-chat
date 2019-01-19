from google.cloud import datastore

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

def getResults(searchQuery):
    allRecords = getRecordsFromDB(searchQuery)
    return allRecords


#getRecordsFromDB('')

#addRecord(record)