# 实现数据库操作，用于对账单信息进行增删改查
#
# create by：zhuyiming 2024.3.3
#
#该数据库是通过ORM方式创建的sqlite数据库

from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker

# 构造工厂基类
Base = declarative_base()    

# 账单信息
class Bill(Base):
    # 表名
    __tablename__ = 'bill'
    # id号
    id = Column(Integer, primary_key=True)
    # 年份
    year = Column('year', Integer)
    # 月份
    month = Column('month',Integer)
    # 日期
    day = Column('day',Integer)
    # 账单类型，收入或支出
    billType = Column('billType',Integer)
    # 总类型，具体的收支项
    totalType = Column('totalType',String)
    # 金额
    money = Column('money',FLOAT)

    def __repr__(self):
        return 'Bill(id:{},year:{},month:{},day:{},billType:{},totalType:{}, money:{})'\
            .format(self.id,self.year,self.month,self.day,self.billType,self.totalType, self.money)

# 数据库操作
class BillSqlalchemy(object):
    session = None

    def __init__(self):
        engine = create_engine('sqlite:///./bill.db', echo=True)
        Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert(self, _year, _month, _day, _billType, _totalType, _money):
        """ 插入操作

        :param _year:年份
        :param _month:月份
        :param _day:日期
        :param _billType:账单类型
        :param _totalType:总类型
        :param _money:金额

        """
        bill = Bill(year=_year, month=_month, day=_day, billType=_billType, totalType=_totalType, money=_money)
        self.session.add(bill)
        self.session.commit()

    def queryYear(self, _year):
        """ 根据年份查找

        :param _year:年份
        return:查找信息
        """
        return self.session.query(Bill).filter_by(year=_year).all()

    def queryMonth(self, _month):
        """ 根据月份查找

        :param _month:月份
        return:查找信息
        """
        return self.session.query(Bill).filter_by(month=_month).all()

    def queryTotal(self):
        """ 全部查找

        return:查找信息
        """
        return self.session.query(Bill).all()
    
    def update(self, _id, _money, _totalType):
        """ 更新数据

        :param _id:当前id信息
        :param _money:金额
        """
        update_bill = self.session.query(Bill).filter_by(id=_id).first()
        print('update bill %s'%update_bill)
        if update_bill:
            update_bill.money = _money
            update_bill.totalType = _totalType
            self.session.commit()

    def delete(self, _id):
        """ 删除数据

        :param _id:当前id信息
        """
        delete_bill = self.session.query(Bill).filter_by(id=_id)
        if delete_bill:
            self.session.delete(delete_bill)
            self.session.commit()

billDataBase = BillSqlalchemy()

