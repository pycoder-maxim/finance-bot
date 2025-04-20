from sqlalchemy.orm import sessionmaker
from database.DataBaseModel import *

engine = create_engine("sqlite:///users.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind= engine)
session = Session()




cat = session.query(Comments).filter_by(name="Зарплата").first()
cat.name = "Зарплата"
session.commit()

