from DataBaseModel import Reports
from sqlalchemy.orm import Session

class ReportsHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    def create_transactions(self, name: str, report_data: str, created_at: str, user_id: int) -> Reports:
        reports = Reports(name=name, report_data=report_data, created_at=created_at)
        reports.user_id = user_id
        self.__session__.add(reports)
        self.__session__.commit()
        return reports

    def get_reports_by_user_id(self,user_id: int) -> list[Reports]:
        return self.__session__.query(Reports).filter(Reports.user_id == user_id).all()

    def update_reports(self, reports_id: int, **kwargs) -> bool:
        reports = self.__session__.query(Reports).get(reports_id)
        if not reports:
            return False
        for key, value in kwargs.items():
            if hasattr(reports, key):
                setattr(reports, key, value)
        self.__session__.commit()
        return True

    def delete_reports(self, reports_id: int) -> bool:
        report = self.__session__.query(Reports).get(reports_id)
        if not report:
            return False
        self.__session__.delete(report)
        self.__session__.commit()
        return True