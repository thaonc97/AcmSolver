import grpc
from concurrent import futures
import time
import numpy as np
import pandas as pd
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict

import ACMSolver_pb2
import ACMSolver_pb2_grpc
import data_manipulate

class ACMSolverServicer(ACMSolver_pb2_grpc.ACMSolverServicer):
    def __init__(self):
        self.connection_str = "mongodb://118.70.206.204:27017/"
        self.db_name = "ThaoLearnDB"
        self.place_stat_collection = "inputLocation"
        self.share_rate_collection = "shareRate"
        self.campaign_collection = "inputCampaign"

    def SetPlaces(self, request_iterator, context):
        response = ACMSolver_pb2.SetResult()
        places =[]
        insert_threshold = 1000
        count = 0
        for place in request_iterator:
            count = count + 1
            dict_place = MessageToDict(place)
            places.append(dict_place)
            if count % insert_threshold ==0: #insert to db every 'insert_threshold' records
                data_manipulate.set_db(places,self.connection_str,self.db_name,self.place_stat_collection)
                places =[]

        data_manipulate.set_db(places,self.connection_str,self.db_name,self.place_stat_collection) #insert the remainders
        response.set_result = True
        return response
    
    def SetShareRate(self,request,context):
        response = ACMSolver_pb2.SetResult()
        share_rate_info = MessageToDict(request)
        data_manipulate.set_db(
            share_rate_info,self.connection_str,self.db_name,self.share_rate_collection,insert_many=False)
        response.set_result = True
        return response
    
    def SetCampaign(self,request_iterator,contex): #Thiết lập danh sách campaign trong trường hợp SP, đồng thời đóng vai trò campaign domain nếu là NP
        response = ACMSolver_pb2.SetResult()
        campaigns =[]
        insert_threshold = 1000
        count = 0
        for campaign in request_iterator:
            count = count + 1
            # campaign.is_network = False
            dict_campaign = MessageToDict(campaign)
            campaigns.append(dict_campaign)
            if count % insert_threshold ==0: #insert to db every 'insert_threshold' records
                data_manipulate.set_db(campaigns,self.connection_str,self.db_name,self.campaign_collection)
                campaigns =[]

        data_manipulate.set_db(campaigns,self.connection_str,self.db_name,self.campaign_collection) #insert the remainders
        response.set_result = True
        return response
    
    def SetNetworkCampaign(self,request_iterator,contex): #Thiết lập danh sách campaign trong trường hợp SP, đồng thời đóng vai trò campaign domain nếu là NP
        response = ACMSolver_pb2.SetResult()
        campaigns =[]
        insert_threshold = 1000
        count = 0
        for campaign in request_iterator:
            count = count + 1
            # campaign.is_network = True
            dict_campaign = MessageToDict(campaign)
            campaigns.append(dict_campaign)

            if count % insert_threshold ==0: #insert to db every 'insert_threshold' records
                data_manipulate.set_db(campaigns,self.connection_str,self.db_name,self.campaign_collection)
                campaigns =[]

        data_manipulate.set_db(campaigns,self.connection_str,self.db_name,self.campaign_collection) #insert the remainders
        response.set_result = True
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
ACMSolver_pb2_grpc.add_ACMSolverServicer_to_server(
        ACMSolverServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)