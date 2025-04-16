from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comments = relationship("Comment", back_populates="expense")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('expenses.id'), nullable=False)
    title = Column(String, nullable=False)
    expenses= relationship("Expense", back_populates="comments")

    def __repr__(self):
        return f"<User(id={self.id}, post='{self.title}')>"




if __name__ == '__main__':
    engine = create_engine("sqlite:///users.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("DATABASE CREATED SUCCESSFULLY\n")

