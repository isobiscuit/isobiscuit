



python -m grpc_tools.protoc -Iisobiscuit/protos --python_out=isobiscuit/api \
     --pyi_out=isobiscuit/api --grpc_python_out=isobiscuit/api \
    isobiscuit/protos/api.proto