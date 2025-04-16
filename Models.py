from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comments = relationship("comments", back_populates="expenses")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    expenses= relationship("expenses", back_populates="comments")

    def __repr__(self):
        return f"<User(id={self.id}, post='{self.title}')>"




if __name__ == '__main__':
    engine = create_engine("sqlite:///users.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("DATABASE CREATED SUCCESSFULLY\n")

