import grpc
from concurrent import futures
import time
import numpy as np
import pandas as pd
import uuid
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

    # def SetPlaces(self, request_iterator, context):
    #     response = ACMSolver_pb2.SetResult()
    #     places =[]
    #     insert_threshold = 1000
    #     count = 0
    #     for place in request_iterator:
    #         count = count + 1
    #         dict_place = MessageToDict(place)
    #         places.append(dict_place)
    #         if count % insert_threshold ==0: #insert to db every 'insert_threshold' records
    #             data_manipulate.set_db(places,self.connection_str,self.db_name,self.place_stat_collection)
    #             places =[]

    #     if places[0]:
    #         data_manipulate.set_db(places,self.connection_str,self.db_name,self.place_stat_collection) #insert the remainders
    #     response.set_result = True
    #     return response
    def SetPlaces(self, request_iterator, context):
        response = ACMSolver_pb2.SetResult()
        data_manipulate.mass_insert_to_db(request_iterator,self.connection_str,self.db_name,self.place_stat_collection,request_type ='place')
        response.set_result = True
        return response

    def SetShareRate(self,request,context):
        response = ACMSolver_pb2.SetResult()
        share_rate_info = MessageToDict(request)
        data_manipulate.set_db(
            share_rate_info,self.connection_str,self.db_name,self.share_rate_collection,insert_many=False)
        response.set_result = True
        return response
    
    def SetCampaign(self,request_iterator,context): #Thiết lập danh sách campaign trong trường hợp SP, đồng thời đóng vai trò campaign domain nếu là NP
        response = ACMSolver_pb2.SetResult()
        data_manipulate.mass_insert_to_db(request_iterator,self.connection_str,self.db_name,self.campaign_collection,request_type ='campaign')
        response.set_result = True
        return response
    
    def SetNetworkCampaign(self,request_iterator,context): 
        response = ACMSolver_pb2.SetResult()
        data_manipulate.mass_insert_to_db(request_iterator,self.connection_str,self.db_name,self.campaign_collection,request_type ='campaign')
        response.set_result = True
        return response

    def InitProblem(self,request,context):
        prefix_sp = 'SP_'
        prefix_np = 'NP_'
        id_generated = uuid.uuid4()
        if request.type == 'SP':
            id_to_return = prefix_sp + str(id_generated)
        if request.type == 'NP':
            id_to_return = prefix_np + str(id_generated)
        response = ACMSolver_pb2.ProblemId()
        response.problem_id = id_to_return
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