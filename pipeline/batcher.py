import asyncio
from collections import deque

from models import get_llm


class InferenceBatcher:
    def __init__(self, batch_size=5, timeout=100):
        self.queue = deque()
        self.batch_size = batch_size
        self.timeout = timeout
        asyncio.create_task(self._process_batcher())

    async def add_request(self, prompt: str):
        future = asyncio.Future()
        self.queue.append((prompt, future))
        return await future

    async def _process_batcher(self):
        llm = get_llm(provider="gemini")
        while True:
            await asyncio.sleep(self.timeout / 1000)

            batch = []
            while len(batch) < self.batch_size and self.queue:
                batch.append(self.queue.popleft())

            if batch:
                prompts = [item[0] for item in batch]
                futures = [item[1] for item in batch]

                responses = await llm.abatch(prompts)

                for response, future in zip(responses, futures):
                    if not future.done() and response.content:
                        future.set_result(response.content)


batcher = InferenceBatcher()
