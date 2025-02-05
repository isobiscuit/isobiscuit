from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BiscuitState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BISCUIT_STATE_UNSPECIFIED: _ClassVar[BiscuitState]
    BISCUIT_STATE_IDLE: _ClassVar[BiscuitState]
    BISCUIT_STATE_RUNNING: _ClassVar[BiscuitState]
    BISCUIT_STATE_WAITING: _ClassVar[BiscuitState]
    BISCUIT_STATE_READY: _ClassVar[BiscuitState]
    BISCUIT_STATE_TERMINATED: _ClassVar[BiscuitState]
    BISCUIT_STATE_ZOMBIE: _ClassVar[BiscuitState]
    BISCUIT_STATE_SUSPENDED: _ClassVar[BiscuitState]
BISCUIT_STATE_UNSPECIFIED: BiscuitState
BISCUIT_STATE_IDLE: BiscuitState
BISCUIT_STATE_RUNNING: BiscuitState
BISCUIT_STATE_WAITING: BiscuitState
BISCUIT_STATE_READY: BiscuitState
BISCUIT_STATE_TERMINATED: BiscuitState
BISCUIT_STATE_ZOMBIE: BiscuitState
BISCUIT_STATE_SUSPENDED: BiscuitState

class BiscuitListResponse(_message.Message):
    __slots__ = ("biscuits",)
    BISCUITS_FIELD_NUMBER: _ClassVar[int]
    biscuits: _containers.RepeatedCompositeFieldContainer[BiscuitInfoResponse]
    def __init__(self, biscuits: _Optional[_Iterable[_Union[BiscuitInfoResponse, _Mapping]]] = ...) -> None: ...

class BiscuitInfoRequest(_message.Message):
    __slots__ = ("biscuit_id",)
    BISCUIT_ID_FIELD_NUMBER: _ClassVar[int]
    biscuit_id: str
    def __init__(self, biscuit_id: _Optional[str] = ...) -> None: ...

class BiscuitInfoResponse(_message.Message):
    __slots__ = ("path", "workdir", "state")
    PATH_FIELD_NUMBER: _ClassVar[int]
    WORKDIR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    path: str
    workdir: str
    state: BiscuitState
    def __init__(self, path: _Optional[str] = ..., workdir: _Optional[str] = ..., state: _Optional[_Union[BiscuitState, str]] = ...) -> None: ...

class RegisterBiscuitResponse(_message.Message):
    __slots__ = ("biscuit_id", "biscuit_token")
    BISCUIT_ID_FIELD_NUMBER: _ClassVar[int]
    BISCUIT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    biscuit_id: str
    biscuit_token: str
    def __init__(self, biscuit_id: _Optional[str] = ..., biscuit_token: _Optional[str] = ...) -> None: ...

class RegisterBiscuitRequest(_message.Message):
    __slots__ = ("biscuit_name", "biscuit_path")
    BISCUIT_NAME_FIELD_NUMBER: _ClassVar[int]
    BISCUIT_PATH_FIELD_NUMBER: _ClassVar[int]
    biscuit_name: str
    biscuit_path: str
    def __init__(self, biscuit_name: _Optional[str] = ..., biscuit_path: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
