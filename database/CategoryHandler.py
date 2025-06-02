from DataBaseModel import Categories
from sqlalchemy.orm import Session

categories_of_expenses = ["продуткы","кафе и рестораны","аренда жилья","комунальные услуги ","транспорт ","одежда и обувь ","медицина","подарки","развлечения","спорт","связь и интернет ","покупки","путеществия","образоание","домашние животные ","долги и кредиты"]
categories_of_icomes = ["зарплата","фриланс" ,"проценты" ,"инвестиции","аренда" ,"продажи" ,"возврат долгов ","продажа вещей ","поддержка семьи","стипендия","возврат налогоа"]
categories_of_savings = ["резервный фонд", "на черный день", "общие сбережения", "на увольннение", "на ремонт"]
categories_of_goals = ["отпуск", "покупка авто", "первый взнос на жилье", "образоваение", "новый гаджет", "детям", "подарок себе"]


class CategoryHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    def create_category(self, name: str, ctype: str, created_at: str, user_id: int) -> Categories:
        category = Categories(name=name, ctype=ctype, created_at=created_at)
        category.user_id = user_id
        self.__session__.add(category)
        self.__session__.commit()
        return category

    def get_categories_by_user_id(self, user_id: int) -> list[Categories]:
        return self.__session__.query(Categories).filter(Categories.user_id == user_id).all()

    def get_categories_by_tg_id_and_ctype(self, user_id:int, cat_type:str) -> list[Categories]:
        return self.__session__.query(Categories).filter(Categories.user_id == user_id, Categories.ctype == cat_type).all()

    def update_category(self, category_id: int, **kwargs) -> bool:
        category = self.__session__.query(Categories).get(category_id)
        if not category:
            return False
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        self.__session__.commit()
        return True

    def delete_category(self, category_id: int) -> bool:
        category = self.__session__.query(Categories).get(category_id)
        if not category:
            return False
        self.__session__.delete(category)
        self.__session__.commit()
        return True