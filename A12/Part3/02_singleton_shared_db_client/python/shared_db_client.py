"""Singleton: Shared Prisma Database Client (globalThis holder that survives hot reloads)."""

ENVS = {"development", "test", "production"}


class ProcessGlobals:
    """Process-wide state that outlives module re-evaluation (globalThis)."""

    def __init__(self) -> None:
        self.prisma = None
        self.constructed = 0


class DatabaseClient:
    """Stand-in for PrismaClient; counts how many instances the process created."""

    def __init__(self, process: ProcessGlobals) -> None:
        process.constructed += 1


class DbModule:
    """One evaluation of db.ts."""

    def __init__(self, process: ProcessGlobals, node_env: str) -> None:
        if node_env not in ENVS:
            raise ValueError("invalid NODE_ENV")
        self.prisma = process.prisma or DatabaseClient(process)
        if node_env != "production":
            process.prisma = self.prisma
