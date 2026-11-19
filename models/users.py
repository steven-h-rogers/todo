import uuid
import datetime

from sqlalchemy import Text, DateTime, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from models.db import Base

# TODO: make sure to validate pwd_hash and email in schema
class Users(Base):
    __tablename__ = "users"
    usr_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuidv7(monotonic=True))
    usr_name : Mapped[str] = mapped_column(Text, nullable=False)
    pwd_hash : Mapped[str] = mapped_column(Text, nullable=False)
    email : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now()) 

    __table_args__ = (
        CheckConstraint("char_length(usr_name) <= 63", name="check_usr_name_length"),
        CheckConstraint("char_length(pwd_hash) <= 511", name="check_pwd_hash_length"),
        CheckConstraint("email = lower(email)", name="check_email_lower"),
        CheckConstraint("char_length(email) <= 320 AND char_length(email) >= 3", name="check_email_length"),
    )