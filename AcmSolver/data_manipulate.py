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

def mass_insert_to_db(data_stream,connection_str,db_name,collection_name,request_type): # insert places,campaigns to db
    client = pymongo.MongoClient(connection_str)
    working_db = client[db_name]
    working_collection = working_db[collection_name]
    to_insert_list = []
    insert_threshold = 1000
    count = 0
    for data in data_stream:
        #print("data is ",data)
        count += 1
        problem_id = data.problem_id.problem_id
        #print(problem_id)
        dict_data =MessageToDict(data,including_default_value_fields=True)
        data_to_insert = dict_data[request_type]
        data_to_insert['problemId'] = problem_id
        to_insert_list.append(data_to_insert)
        if count % insert_threshold ==0:
            working_collection.insert_many(to_insert_list)
            
    if to_insert_list[0]:
        working_collection.insert_many(to_insert_list) #insert the remainders