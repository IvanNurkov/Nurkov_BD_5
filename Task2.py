import sqlalchemy 
from sqlalchemy.orm import sessionmaker
from Task1 import Publisher, Book, Shop, Stock, Sale, create_tables

DSN = 'postgresql://postgres:post@localhost:5432/task_5'
engine  = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

pub1 = Publisher(name='Директ-Медиа')
pub2 = Publisher(name='АСТ')
session.add_all([pub1, pub2])
session.commit()

book1 = Book(title='Ночевала тучка золотая', publisher=pub1)
book2 = Book(title='На западном фронте без перемен', publisher=pub2)
session.add_all([book1, book2])
session.commit()  

sh1 = Shop(name='Буквоед')
sh2 = Shop(name='Зингер')
sh3 = Shop(name='Графит')
session.add_all([sh1, sh2, sh3])
session.commit()

st1 = Stock(book=book1, shop=sh1, count=25)
st2 = Stock(book=book1, shop=sh2, count=40)
st3 = Stock(book=book2, shop=sh1, count=100)
st4 = Stock(book=book2, shop=sh3, count=1914)
session.add_all([st1, st2, st3, st4])
session.commit()

sl1 = Sale(price=850, date_sale='2022-11-10', stock=st1, count=4)
sl2 = Sale(price=250, date_sale='2022-08-18', stock=st2, count=1)
sl3 = Sale(price=400, date_sale='2022-10-21', stock=st3, count=3)
session.add([sl1, sl2, sl3])
session.commit()


pub_name = input('Название издательства: ')
pub_id = input('Идентификатор издательства: ')

def get_shop_by_publisher(publisher_name=None, publisher_id=None):
    if publisher_id is not None and publisher_name is None:
        for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.id == int(publisher_id)):
            print(c)
    elif publisher_name is not None and publisher_id is None:
        for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == publisher_name):
            print(c)
    elif publisher_name is not None and publisher_id is not None:
        for c in session.query(Shop.name).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == publisher_name, Publisher.id == int(publisher_id)):
            print(c)

if __name__ == '__main__':
    if pub_name == True and pub_id == False:
        get_shop_by_publisher(publisher_name=pub_name)
    elif pub_name == False and pub_id == True:
        get_shop_by_publisher(publisher_id=pub_id)
    elif pub_name == True and pub_id == True:
        get_shop_by_publisher(publisher_id=pub_id, publisher_name=pub_name)
    else: 
        print(f'Ошибка ввода')

session.close()