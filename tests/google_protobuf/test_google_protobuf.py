from datetime import datetime, timedelta, timezone
from types import NoneType

import pytest
from google.protobuf.duration_pb2 import Duration
from google.protobuf.struct_pb2 import NullValue
from google.protobuf.timestamp_pb2 import Timestamp

from pydantic_rpc.core import Message, generate_and_compile_proto, python_value_to_proto


class WithTimestamp(Message):
    timestamp: datetime


class WithDuration(Message):
    duration: timedelta


class WithNone(Message):
    none: None


class GreeterWithTimestamp:
    async def say_hello(self, request: WithTimestamp) -> WithTimestamp:
        return WithTimestamp(timestamp=request.timestamp + timedelta(seconds=1))


class GreeterWithDuration:
    async def say_hello(self, request: WithDuration) -> WithDuration:
        return WithDuration(duration=request.duration + timedelta(seconds=1))


class GreeterWithNone:
    async def say_hello(self, request: WithNone) -> WithNone:
        return WithNone(none=None)


class TestGreeterWithTimestamp:
    @pytest.mark.asyncio
    async def test_greeter_with_timestamp(self):
        generate_and_compile_proto(GreeterWithTimestamp())

    @pytest.mark.asyncio
    async def test_greeter_with_timestamp_python_to_protobuf_generation(self):
        # Use UTC timezone to avoid timezone ambiguity
        datetime_value = datetime(
            year=2025, month=1, day=1, hour=1, minute=1, second=1, tzinfo=timezone.utc
        )
        converted_value = python_value_to_proto(
            datetime,
            datetime_value,
            None,
        )

        timestamp_value = int(datetime_value.timestamp())
        expected_value = Timestamp(seconds=timestamp_value)
        assert converted_value == expected_value


class TestGreeterWithDuration:
    @pytest.mark.asyncio
    async def test_greeter_with_duration(self):
        generate_and_compile_proto(GreeterWithDuration())

    @pytest.mark.asyncio
    async def test_greeter_with_duration_python_to_protobuf_generation(self):
        converted_value = python_value_to_proto(
            timedelta, timedelta(hours=1, minutes=1, seconds=1), None
        )
        expected_value = Duration(seconds=3661)
        assert converted_value == expected_value


class TestGreeterWithNone:
    @pytest.mark.asyncio
    async def test_greeter_with_none_protobuf_generation(self):
        generate_and_compile_proto(GreeterWithNone())

    @pytest.mark.asyncio
    async def test_greeter_with_none_python_to_protobuf_generation(self):
        converted_value = python_value_to_proto(NoneType, None, None)
        assert converted_value == NullValue.NULL_VALUE

    @pytest.mark.asyncio
    async def test_greeter_with_none_protobuf_to_python_generation(self):
        generate_and_compile_proto(GreeterWithNone())
