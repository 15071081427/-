from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    billType = Column(Integer)
    totalType = Column(Integer)
    money = Column(FLOAT)

    def __repr__(self):
        return 'Bill(id:{},year:{},month:{},day:{},billType:{},totalType:{})'\
            .format(self.id,self.year,self.month,self.day,self.billType,self.totalType, self.money)

class BillSqlalchemy(object):
    session = None

    def __init__(self):
        engine = create_engine('sqlite:///./bill.db', echo=True)
        Base.metadata.create_all(engine, checkfirst=True)
        self.session = sessionmaker(bind=engine)

    def Insert(self, _year, _month, _day, _billType, _totalType, _money):
        bill = Bill(year=_year, month=_month, day=_day, billType=_billType, totalType=_totalType, money=_money)
        self.session.add(bill)
        self.session.commit()

    def Query(self, queryType):
        if queryType == 0:
            return self.QueryTotal()
        elif queryType == 1:
            return self.QueryYear()
        elif queryType == 2:
            return self.QueryMonth()

    def QueryYear(self, _year):
        return self.session.query(Bill).filter_by(year=_year)

    def QueryMonth(self, _month):
        return self.session.query(Bill).filter_by(year=_month)

    def QueryTotal(self):
        return self.session.query(Bill).all()
    
    def Update(self, _id, _money):
        update_bill = self.session.query(Bill).filter_by(id=_id)
        if update_bill:
            update_bill.money = _money
            self.session.commit()

    def Delete(self, _id):
        delete_bill = self.session.query(Bill).filter_by(id=_id)
        if delete_bill:
            self.session.delete(delete_bill)
            self.session.commit()


