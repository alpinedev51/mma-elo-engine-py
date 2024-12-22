from .fighters import router as fighters_router
from .events import router as events_router
from .elo_records import router as elo_records_router
from .fighters import router as fights_router

__all__ = ["fighters_router", "events_router", "elo_records_router", "fights_router"]