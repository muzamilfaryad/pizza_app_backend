import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.order import Order, OrderStatus
from schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderStatusUpdate,
)


class OrderService:
    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        order_data: OrderCreate,
    ) -> Order:
        """
        Create a new order.
        """

        items_json = json.dumps([
            item.model_dump()
            for item in order_data.items
        ])

        order = Order(
            user_id=user_id,
            items=items_json,
            total_price=order_data.total_price,
            delivery_address=order_data.delivery_address,
            status=OrderStatus.PENDING,
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        """
        Retrieve order by ID.
        """

        order = (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return order

    @staticmethod
    def get_user_orders(db: Session, user_id: int) -> list[Order]:
        """
        Get all orders for a specific user.
        """

        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_all_orders(db: Session) -> list[Order]:
        """
        Get all orders.
        """

        return db.query(Order).all()

    @staticmethod
    def update_order(
        db: Session,
        order_id: int,
        user_id: int,
        order_data: OrderUpdate,
    ) -> Order:
        """
        Update a user's order.
        """

        order = OrderService.get_order_by_id(db, order_id)

        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own orders",
            )

        if order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending orders can be updated",
            )

        if order_data.items is not None:
            order.items = json.dumps([
                item.model_dump()
                for item in order_data.items
            ])

        if order_data.total_price is not None:
            order.total_price = order_data.total_price

        if order_data.delivery_address is not None:
            order.delivery_address = order_data.delivery_address

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        status_data: OrderStatusUpdate,
    ) -> Order:
        """
        Update order status.
        """

        order = OrderService.get_order_by_id(db, order_id)

        order.status = status_data.status

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def delete_order(
        db: Session,
        order_id: int,
        user_id: int,
    ) -> dict:
        """
        Delete an order.
        """

        order = OrderService.get_order_by_id(db, order_id)

        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own orders",
            )

        db.delete(order)
        db.commit()

        return {
            "message": "Order deleted successfully",
        }