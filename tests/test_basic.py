import pytest

from jarvis_ipybox import ExecutionClient, ExecutionContainer

TEST_IMAGE_TAG = "ghcr.io/gradion-ai/jarvis_ipybox:minimal"

@pytest.fixture(scope="module")
async def executor(workspace: str):
    async with ExecutionContainer(
        tag=TEST_IMAGE_TAG,
        binds={workspace: "workspace"},
    ) as container:
        async with ExecutionClient(host="localhost", port=container.port) as client:
            yield client


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_functionality(executor):
    result = await executor.execute("print('Hello, world!')")
    assert result.text == "Hello, world!"
