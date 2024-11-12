from .database import Base
from sqlalchemy import *
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    year = Column(Integer)

    user = relationship("User")


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email= Column(String , nullable=False , unique=True)
    password = Column(String, nullable=False, unique=True)

class Vote(Base):
    __tablename__= "votes"
    user_id = Column(Integer , ForeignKey(User.id , ondelete="CASCADE") , primary_key= True )
    post_id = Column(Integer , ForeignKey(Post.id , ondelete="CASCADE") , primary_key= True )






 

 