import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from models.db import Base
from sqlalchemy import Text, CheckConstraint, ForeignKey, Integer, Boolean, DateTime, func, text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from models.task_group import TaskGroup

class Task(Base):
    __tablename__ = "task"

    tsk_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuidv7(monotonic=True))
    grp_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task_group.grp_id", ondelete="CASCADE"), nullable=False)
    tsk_name : Mapped[str] = mapped_column(Text, nullable=False)
    tsk_desc : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority_lvl : Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    is_complete : Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    tsk_due_date : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    task_group: Mapped["TaskGroup"] = relationship("TaskGroup", back_populates="task")


    __table_args__ = (
        CheckConstraint("priority_lvl <= 5 AND priority_lvl >= 0", name="check_valid_priority"),
    )

