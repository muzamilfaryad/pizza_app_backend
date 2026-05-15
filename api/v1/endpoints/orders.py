from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from middleware.auth import get_current_user, get_current_superuser
from models.user import User
from schemas.order import OrderCreate, OrderUpdate, OrderStatusUpdate, OrderResponse
from services.order_service import OrderService
from utlis.response import api_response

router = APIRouter(prefix="/orders", tags=["Orders"])

# Place an order
@router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Place a new order
    
    - **items**: List of items with name, quantity, and price
    - **total_price**: Total price of the order
    - **delivery_address**: Delivery address for the order
    """
    order = OrderService.create_order(db, current_user.id, order_data)
    return api_response(
        message="Order created successfully",
        data=OrderResponse.model_validate(order).model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED,
    )

# Update an order
@router.put("/order/update/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an order (only pending orders can be updated)
    
    - **order_id**: ID of the order to update
    - **items**: Updated items (optional)
    - **total_price**: Updated total price (optional)
    - **delivery_address**: Updated delivery address (optional)
    """
    order = OrderService.update_order(db, order_id, current_user.id, order_data)
    return api_response(
        message="Order updated successfully",
        data=OrderResponse.model_validate(order).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )

# Update order status (admin only)
@router.put("/order/status/{order_id}", status_code=status.HTTP_200_OK)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Update order status (Superuser only)
    
    - **order_id**: ID of the order
    - **status**: New status (pending, confirmed, preparing, ready, delivered, cancelled)
    """
    order = OrderService.update_order_status(db, order_id, status_data)
    return api_response(
        message="Order status updated successfully",
        data=OrderResponse.model_validate(order).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )

# Delete an order
@router.delete("/order/delete/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an order
    
    - **order_id**: ID of the order to delete
    """
    result = OrderService.delete_order(db, order_id, current_user.id)
    return api_response(
        message=result.get("message", "Order deleted successfully"),
        status_code=status.HTTP_200_OK,
    )

# Get user's orders
@router.get("/user/orders", status_code=status.HTTP_200_OK)
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all orders for the current user
    """
    orders = OrderService.get_user_orders(db, current_user.id)
    return api_response(
        message="User orders retrieved successfully",
        data=[OrderResponse.model_validate(order).model_dump(mode="json") for order in orders],
        status_code=status.HTTP_200_OK,
    )

# Get all orders (admin only)
@router.get("/orders", status_code=status.HTTP_200_OK)
async def get_all_orders(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get all orders (Superuser only)
    """
    orders = OrderService.get_all_orders(db)
    return api_response(
        message="Orders retrieved successfully",
        data=[OrderResponse.model_validate(order).model_dump(mode="json") for order in orders],
        status_code=status.HTTP_200_OK,
    )

# Get specific order (admin only)
@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get a specific order (Superuser only)
    
    - **order_id**: ID of the order to retrieve
    """
    order = OrderService.get_order_by_id(db, order_id)
    return api_response(
        message="Order retrieved successfully",
        data=OrderResponse.model_validate(order).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )

# Get user's specific order
@router.get("/user/order/{order_id}", status_code=status.HTTP_200_OK)
async def get_user_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific order for the current user
    
    - **order_id**: ID of the order to retrieve
    """
    order = OrderService.get_order_by_id(db, order_id)
    
    # Verify user owns this order
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own orders"
        )
    
    return api_response(
        message="Order retrieved successfully",
        data=OrderResponse.model_validate(order).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )
