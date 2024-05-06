import os
import pymongo as pm
import bcrypt

LOCAL = "0"
CLOUD = "1"

USER_DB = 'userDB'
VECTOR_DB = 'vectorDB'
USER_NAME = 'SWEES'

client_existing = None
client_vector = None

MONGO_ID = '_id'

URI_FRONT = 'mongodb+srv://WilliamYuxinXu:'
URI_BACK = '@swees.mumkgcx.mongodb.net/?retryWrites=true&w=majority'
URI_EXISTING = URI_FRONT + URI_BACK

URI_VECTOR_BACK = '@articleembeddings.c1muytb.mongodb.net/?retryWrites=true&w=majority&appName=articleEmbeddings'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client_existing, client_vector
    if client_existing is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO") == CLOUD:
            # currently both mongo passwords are the same
            password = os.environ.get("MONGODB_PASSWORD")
            vector_password = os.environ.get("MONGODB_PASSWORD")
            if not password and vector_password:
                raise ValueError('You must set both passwords '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client_existing = pm.MongoClient(URI_FRONT + password + URI_BACK)
            client_vector = pm.MongoClient(
                URI_FRONT + vector_password + URI_VECTOR_BACK)
        else:
            print("Connecting to Mongo locally.")
            vector_password = os.environ.get("MONGODB_PASSWORD")
            if not vector_password:
                raise ValueError('Missing MongoDB vector '
                                 + 'database password.')
            client_existing = pm.MongoClient()
            
            # vector search can only be performed on Atlas, not locally
            client_vector = pm.MongoClient(
                URI_FRONT + vector_password + URI_VECTOR_BACK)


def insert_one(collection, doc, db=USER_DB):
    """
    Insert a single doc into collection.
    """
    client = client_existing if db == USER_DB else client_vector
    try:
        result = client[db][collection].insert_one(doc)
        return result.inserted_id  # Return the ID of the inserted document
    except pm.PyMongoError as e:
        pm.logging.error(f"Error inserting doc into {db}.{collection}: {e}")
        return None


def fetch_one(collection, filt, case_sensitive=False, db=USER_DB):
    """
    Find with a filter and return the first doc found.

    Parameters:
        collection (str): The name of the collection to search in.
        filt (dict): The filter to apply to the search.
        case_sensitive (bool, optional): Whether the search should be case-sensitive. Default is False.
        db (str, optional): The name of the database to search in. Default is USER_DB.

    Returns:
        dict: The first document found matching the filter.
    """
    client = client_existing if db == USER_DB else client_vector
    if not case_sensitive:
        filt = {key: {'$regex': pattern, '$options': 'i'} if isinstance(pattern, str) else pattern for key, pattern in filt.items()}

    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client = client_existing if db == USER_DB else client_vector
    return client[db][collection].delete_one(filt)


def del_many(collection, filt, db=USER_DB):
    client = client_existing if db == USER_DB else client_vector
    return client[db][collection].delete_many(filt)


def del_first(collection, db=USER_DB):
    """
    Deletes first element it finds.
    """
    client = client_existing if db == USER_DB else client_vector
    return client[db][collection].delete_one({})


def del_all(collection, db=USER_DB):
    """
    Removes all elements in a collection.
    """
    client = client_existing if db == USER_DB else client_vector
    client[db][collection].drop()
    return collection


def update_doc(collection, filters, update_dict, db=USER_DB):
    client = client_existing if db == USER_DB else client_vector
    return client[db][collection].update_one(filters, {'$set': update_dict})


def fetch_all(collection, db=USER_DB):
    client = client_existing if db == USER_DB else client_vector
    ret = []
    for doc in client[db][collection].find():
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret


# In dbc.py

def fetch_all_with_filter(collection, filt={}, projection={}, db=USER_DB):
    """
    Fetch all documents matching the filter with specified projection.
    """
    client = client_existing if db == USER_DB else client_vector
    ret = []
    for doc in client[db][collection].find(filt, projection=projection):
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret


def fetch_all_with_constrained_filter(collection, filt={}, projection={}, db=USER_DB):
    """
    Fetch all documents matching a broader filter (using $or) with specified projection.
    """
    # Construct the broader query with $or
    or_conditions = [{'$or': [{key: value} for key, value in filt.items()]}] if filt else []
    query = {'$or': or_conditions} if or_conditions else {}

    client = client_existing if db == USER_DB else client_vector
    ret = []
    for doc in client[db][collection].find(query, projection=projection):
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=USER_DB):
    client = client_existing if db == USER_DB else client_vector
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        temp = doc[key]
        ret[temp] = doc
    return ret


def hash_str(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# returns collection names
def fetch_collection_name(db=USER_DB):
    client = client_existing if db == USER_DB else client_vector
    return client[db].list_collection_names()


def update_or_insert_one(collection, filt, update_dict, db=USER_DB):
    """
    Update an existing document or insert a new one if it doesn't exist.

    Parameters:
        collection (str): The name of the collection to perform the operation in.
        filt (dict): The filter to match the document to update.
        update_dict (dict): The dictionary with fields to update or insert.
        db (str, optional): The name of the database to perform the operation in. Default is USER_DB.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """
    try:
        # The $set operator replaces the value of a field with the specified value.
        # The upsert=True option creates a new document if no document matches the filter.
        result = client[db][collection].update_one(filt, {'$set': update_dict}, upsert=True)
        if result.upserted_id:
            print("Inserted a new document with ID:", result.upserted_id)
        else:
            print("Updated existing document(s). Matched:", result.matched_count)
        return result
    except pm.PyMongoError as e:
        pm.logging.error(f"Error in update_or_insert operation for {db}.{collection}: {e}")
        return None
