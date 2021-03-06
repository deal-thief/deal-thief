from sqlalchemy import (
    Index,
    Date,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText
)
from sqlalchemy.orm import relationship
from .meta import Base
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime


class User(Base):
    """User schema."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    sign_up_date = Column(Date())
    city = Column(Unicode(255), nullable=False)
    state = Column(Unicode(5), nullable=False)
    note = Column(UnicodeText())
    searches = relationship('Search')

    def verify_credential(self, email, password):
        """Verify email and password."""
        is_authenticated = False
        if self.email == email:
            try:
                is_authenticated = pwd_context.verify(
                    password, self.password
                )
            except ValueError:
                pass
        return is_authenticated


class Search(Base):
    """Search schema."""

    __tablename__ = 'searches'
    id = Column(Integer, primary_key=True)
    creation_date = Column(Date, default=datetime.now)
    location = Column(UnicodeText())
    checkin = Column(Date())
    checkout = Column(Date())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='searches')

Index('index_user_email', User.email, unique=True, mysql_length=255)
