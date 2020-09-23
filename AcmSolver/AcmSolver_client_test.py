import grpc
import sys
sys.path.append('./generated')
# import the generated classes
import ACMSolver_pb2
import ACMSolver_pb2_grpc
# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = ACMSolver_pb2_grpc.ACMSolverStub(channel)

# create a valid request message
# request = campaign_pb2.EmptyMessage()
request = ACMSolver_pb2.ASCampaign()
request.problem_id ='thao_test_send_from_client'
request.is_network = False
request.start_date = 4
request.expired_date =10
request.priority = 1
#request = acm_base_pb2.Int64List(values = [1573])
# make the call
request2 = ACMSolver_pb2.ASCampaign()
request2.problem_id ='thao_test_send_from_client'
request2.is_network = True
request2.start_date = 4
request2.expired_date =10
request2.priority = 1
def generate_iterator(stream_wannabe_list):
    for num in stream_wannabe_list:
        yield num
print(request)
print(request2)
all_requests = generate_iterator([request,request2])
response = stub.SetCampaign(all_requests)
# et voilà
print(response)