from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

if __name__ == '__main__':
    engine = create_engine("sqlite:///users.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("DATABASE CREATED SUCCESSFULLY\n")
