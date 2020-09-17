import numpy as np
import math
import pymongo
import json
from docplex.mp.model import Model
import pandas as pd
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict

def set_place_to_db(data_list,connection,db_name,collection_name):
    client = pymongo.MongoClient(connection)
    working_db = client[db_name]
    working_collection = working_db[collection_name]
    working_collection.insert_many(data_list)

def insert_share_rate_to_db(r,problem_id,connection,db_name,collection_name):
    client = pymongo.MongoClient(connection)
    working_db = client[db_name]
    working_collection = working_db[collection_name]
    df = pd.data_fram
    df = docplex_sol.get_value_df(x_var,key_column_names=['campaignID','date','location'])
    df = df[df.value != 0] #Drop all records with value = 0
    output = df.to_json(orient = "records")
    data = json.loads(output)
    working_collection.insert_many(data)