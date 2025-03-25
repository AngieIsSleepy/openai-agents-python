import pytest

from agents.exceptions import UserError
from agents.mcp.server import _MCPServerWithClientSession


class CrashingClientSessionServer(_MCPServerWithClientSession):
    def __init__(self):
        super().__init__(cache_tools_list=False)
        self.cleanup_called = False

    def create_streams(self):
        raise ValueError("Crash!")

    async def cleanup(self):
        self.cleanup_called = True
        await super().cleanup()


@pytest.mark.asyncio
async def test_server_errors_cause_error_and_cleanup_called():
    server = CrashingClientSessionServer()

    with pytest.raises(ValueError):
        await server.connect()

    assert server.cleanup_called


@pytest.mark.asyncio
async def test_not_calling_connect_causes_error():
    server = CrashingClientSessionServer()

    with pytest.raises(UserError):
        await server.list_tools()

    with pytest.raises(UserError):
        await server.call_tool("foo", {})
