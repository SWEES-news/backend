import os
import pymongo as pm
import bcrypt

LOCAL = "0"
CLOUD = "1"

USER_DB = 'userDB'

USER_NAME = 'SWEES'

client = None

MONGO_ID = '_id'

URI_FRONT = 'mongodb+srv://WilliamYuxinXu:'
URI_BACK = '@swees.mumkgcx.mongodb.net/?retryWrites=true&w=majority'
URI = URI_FRONT + URI_BACK


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO") == CLOUD:
            password = os.environ.get("MONGODB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(URI_FRONT + password + URI_BACK)
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
            # password = os.environ.get("MONGODB_PASSWORD")
            # client = pm.MongoClient(URI_FRONT + password + URI_BACK)


def insert_one(collection, doc, db=USER_DB):
    """
    Insert a single doc into collection.
    """
    try:
        result = client[db][collection].insert_one(doc)
        return result.inserted_id  # Return the ID of the inserted document
    except pm.PyMongoError as e:
        pm.logging.error(f"Error inserting doc into {db}.{collection}: {e}")
        return None


def fetch_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    return client[db][collection].delete_one(filt)


def del_first(collection, db=USER_DB):
    """
    Deletes first element it finds.
    """
    return client[db][collection].delete_one({})


def del_all(collection, db=USER_DB):
    """
    Removes all elements in a collection.
    """
    client[db][collection].drop()
    return collection


def update_doc(collection, filters, update_dict, db=USER_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


def fetch_all(collection, db=USER_DB):
    ret = []
    for doc in client[db][collection].find():
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret


def fetch_all_with_constrained_filter(collection, filt={}, db=USER_DB):
    ret = []
    for doc in client[db][collection].find(filter=filt):
        # Convert ObjectId fields to string
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret

def fetch_all_with_filter(collection, filt={}, db=USER_DB):
    """
    Relaxed (Broad) Querying: This refers to a search or query condition where multiple criteria are combined with an OR logic.
    It's "looser" because it returns records that meet any one of the specified conditions,
    broadening the result set. The modification you made to use the $or operator in MongoDB shifts
    the querying approach from constrained to relaxed.
    """
    # Create an array for $or operation
    or_conditions = []

    for key, value in filt.items():
        # Each key-value pair in filt becomes a separate condition in the $or array
        or_conditions.append({key: value})

    # Construct the final query
    query = {'$or': or_conditions} if or_conditions else {}

    ret = []
    for doc in client[db][collection].find(query):
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=USER_DB):
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
    return client[db].list_collection_names()
