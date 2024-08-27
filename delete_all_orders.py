from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork


def delete_all_orders():
    # SQLite データベースの URL を直接指定
    db_url = 'sqlite:///orders.db'

    with UnitOfWork(db_url) as unit_of_work:
        orders_repository = OrdersRepository(unit_of_work.session)
        orders = orders_repository.list()
        for order in orders:
            orders_repository.delete(order.id)
        unit_of_work.commit()


if __name__ == "__main__":
    delete_all_orders()