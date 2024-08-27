from ..models import entities
from .helpers import get_db
from ..util import metrics


class DBManager:
    """A higher-level abstraction over the database interface. 
    
    Interaction with the DB should only be done via the manager. That way changing the database is contained to one place.
    And for testing the manager can easily be mocked.
    """

    def __init__(self):
        pass

    def persist_entity(self, entity: entities.SomeEntity):
        with get_db() as db:
            db.add(entity)
            db.commit()
            metrics.DB_INSERT_COUNT.inc()

    def get_entity_count(self) -> int:
        with get_db() as db:
            return db.query(entities.SomeEntity).count()
