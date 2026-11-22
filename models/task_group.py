import uuid
import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Text, ForeignKey, CheckConstraint, DateTime, func, text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from models.db import Base

if TYPE_CHECKING:
    from models.users import User
    from models.task import Task

class TaskGroup(Base):
    __tablename__="task_group"

    grp_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuidv7(monotonic=True))
    usr_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.usr_id", ondelete="CASCADE"), nullable=False)
    grp_name: Mapped[str] = mapped_column(Text, nullable=False, server_default="Default Group")
    grp_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    grp_due_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="task_groups")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="task_group")



    __table_args__ = (
        CheckConstraint("char_length(grp_name) <= 255", name="check_grp_name_length"),
    )

