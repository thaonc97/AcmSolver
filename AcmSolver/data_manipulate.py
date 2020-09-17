import numpy as np
import math
import pymongo
import json
from docplex.mp.model import Model
import pandas as pd
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict

# def set_place_to_db(data_list,connection,db_name,collection_name):
#     client = pymongo.MongoClient(connection)
#     working_db = client[db_name]
#     working_collection = working_db[collection_name]
#     working_collection.insert_many(data_list)


# def set_share_rate(data,connection,db_name,collection_name):
#     client = pymongo.MongoClient(connection)
#     working_db = client[db_name]
#     working_collection = working_db[collection_name]

def set_db(data,con,db,collection,insert_many =True):
    client = pymongo.MongoClient(con)
    working_db = client[db]
    working_collection = working_db[collection]
    
    if insert_many ==False:
        working_collection.insert_one(data)
    if insert_many == True:
        working_collection.insert_many(data)
    print('Insert sucessfully!')