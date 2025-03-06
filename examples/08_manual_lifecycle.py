"""
Example demonstrating how to use environment variables in the execution container.
"""

import asyncio

from jarvis_ipybox import ExecutionClient, ExecutionContainer


async def main():
    # --8<-- [start:run-container]
    container = ExecutionContainer(port=7777)  # (1)!
    await container.run()  # (2)!
    assert container.port == 7777
    # --8<-- [end:run-container]

    async with ExecutionClient(port=container.port):
        await asyncio.sleep(1)

    # --8<-- [start:kill-container]
    await container.kill()  # (3)!
    # --8<-- [end:kill-container]


if __name__ == "__main__":
    asyncio.run(main())
