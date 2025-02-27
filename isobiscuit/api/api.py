import grpc
from concurrent import futures
from . import api_pb2, api_pb2_grpc

"""Client for IsoBiscuit Daemon"""
class Client:
    """Create IsoBiscuit Daemon Client"""
    def __init__(self, *, 
        channel="localhost:50051"    
    ):
        self.channel    = grpc.insecure_channel(channel)
    """Returns a ManagerServiceClient"""
    def getMangerService(self):
        return ManagerServiceClient(self)
    
"""Client for the ManagerService"""
class ManagerServiceClient:
    def __init__(self, client: Client):
        self.client     = client
        self.channel    = client.channel
        self.stub       = api_pb2_grpc.ManagerServiceStub(self.channel)
    """Register Biscuit to daemon, returns a response"""
    def registerBiscuit(self, biscuit_name: str, biscuit_path: str) -> api_pb2.RegisterBiscuitResponse:
        request = api_pb2.RegisterBiscuitRequest(biscuit_name=biscuit_name, biscuit_path=biscuit_path)
        response: api_pb2.RegisterBiscuitResponse = self.stub.RegisterBiscuit(request)
        return response
    """Get Biscuit Info from biscuit_id"""
    def biscuitInfo(self, biscuit_id) -> api_pb2.BiscuitInfoResponse:
        request = api_pb2.BiscuitInfoRequest(biscuit_id=biscuit_id)
        response: api_pb2.BiscuitInfoResponse = self.stub.BiscuitInfo(request)
        return response
    """List all Biscuits"""
    def biscuitList(self) -> api_pb2.BiscuitListResponse:
        request = api_pb2.Empty()
        response : api_pb2.BiscuitListResponse = self.stub.BiscuitList(request)
        return response
