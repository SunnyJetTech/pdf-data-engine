from db.database import ORMBase
from .mixins.timestamp_mixin import TimestampMixin
from .mixins.uuid_mixin import UUIDMixin
from .mixins.soft_delete_mixin import SoftDeleteMixin

class BaseModel(ORMBase, UUIDMixin, TimestampMixin):
    __abstract__ = True

class SoftDeleteModel(BaseModel, SoftDeleteMixin):
    __abstract__ = True