import sqlalchemy 
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DSN = 'postgresql://postgres:post@localhost:5432/task_5'
engine  = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column(sqlalchemy.String(length=60), nullable = False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = 'book'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    title = sqlalchemy.Column(sqlalchemy.String(length=60), nullable = False)   
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publisher.id"))

    publisher = relationship(Publisher, backref = 'publisher_book')

    def __str__(self):
        return f'{self.id}: {self.title}, {self.id_publisher}'

class Shop(Base):
    __tablename__ = 'Shop'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable = False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id"))
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shop.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)

    book = relationship(Book, backref = 'book_Stock')
    shop = relationship(Shop, backref = 'shop_Stock')

    def __str__(self):
        return f'{self.id}: {self.id_book}, {self.id_shop}, {self.count}'

class Sale(Base):
    __tablename__ = 'sale'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    date_sale = sqlalchemy.Column(sqlalchemy.Date, nullable = False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)

    stock = relationship(Stock, backref = "stock_book")

    def __str__(self):
        return f'{self.id}: {self.price}, {self.date_sale}, {self.id_stock}, {self.count}'

def create_tables(engine):
    Base.metadata.creat_all(engine)