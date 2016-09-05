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


class User(Base):
    """User schema"""
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


class Search(Base):
    """Search schema"""
    __tablename__ = 'searches'
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    description = Column(UnicodeText())
    user_id = Column(Integer, ForeignKey('users.id'))

Index('index_user_email', User.email, unique=True, mysql_length=255)
