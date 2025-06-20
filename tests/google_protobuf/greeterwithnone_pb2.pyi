from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WithNone(_message.Message):
    __slots__ = ("none",)
    NONE_FIELD_NUMBER: _ClassVar[int]
    none: _struct_pb2.NullValue
    def __init__(self, none: _Optional[_Union[_struct_pb2.NullValue, str]] = ...) -> None: ...
