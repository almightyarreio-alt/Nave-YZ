import asyncio

class ReentrantLock:
    """
    A reentrant lock for asyncio, allowing the same asyncio Task to acquire
    the lock multiple times recursively without deadlocking.
    """
    def __init__(self):
        self._lock = asyncio.Lock()
        self._owner: asyncio.Task | None = None
        self._count = 0

    async def acquire(self) -> None:
        current_task = asyncio.current_task()
        if self._owner == current_task:
            self._count += 1
            return
        await self._lock.acquire()
        self._owner = current_task
        self._count = 1

    def release(self) -> None:
        current_task = asyncio.current_task()
        if self._owner != current_task:
            raise RuntimeError("Cannot release a lock you do not own")
        self._count -= 1
        if self._count == 0:
            self._owner = None
            self._lock.release()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()
