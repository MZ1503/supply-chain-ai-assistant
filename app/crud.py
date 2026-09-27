from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from app.models import Product, Query, User

# crud.py
# Status: in progress — functions written, integration with api.py pending
# Replaces Pandas CSV operations with SQLAlchemy queries

# PRODUCT QUERIES

def get_all_products(db: Session):
    """Return every product in the database."""
    return db.query(Product).all()


def get_product_by_article_code(db: Session, article_code: str):
    """Look up a single product by its unique article code."""
    return db.query(Product).filter(Product.article_code == article_code).first()


def get_products_by_brand(db: Session, brand: str):
    """Return all products for a given brand (case-insensitive)."""
    return db.query(Product).filter(Product.brand.ilike(f"%{brand}%")).all()


def get_products_by_category(db: Session, category: str):
    """Return all products in a given category."""
    return db.query(Product).filter(Product.category.ilike(f"%{category}%")).all()


def get_low_stock_products(db: Session, threshold: int = 50):
    """Return products where actual quantity is below the threshold."""
    return (
        db.query(Product)
        .filter(Product.actual_qty < threshold)
        .order_by(asc(Product.actual_qty))
        .all()
    )


def get_expiring_soon(db: Session, days: int = 30):
    """
    Return products expiring within the next N days.
    Explicitly excludes NULL values — in SQL, NULL compared
    to any value returns NULL not False, so we filter it out first.
    """
    return (
        db.query(Product)
        .filter(
            Product.days_to_expiry.isnot(None),   # fix: exclude NULLs first
            Product.days_to_expiry <= days,
            Product.days_to_expiry >= 0
        )
        .order_by(asc(Product.days_to_expiry))
        .all()
    )


def get_forecast_vs_actual(db: Session):
    """
    Return products with both forecast and actual qty
    so the agent can compare over/under stock situations.
    """
    return (
        db.query(Product)
        .filter(Product.forecast_qty.isnot(None))
        .all()
    )


def get_total_inventory_value(db: Session):
    """
    Calculate total inventory value (actual_qty * unit_price_aed)
    across all products.
    """
    result = db.query(
        func.sum(Product.actual_qty * Product.unit_price_aed)
    ).scalar()
    return round(result, 2) if result else 0.0


def get_inventory_value_by_brand(db: Session):
    """Return total inventory value grouped by brand."""
    return (
        db.query(
            Product.brand,
            func.sum(Product.actual_qty * Product.unit_price_aed).label("total_value")
        )
        .group_by(Product.brand)
        .order_by(desc("total_value"))
        .all()
    )


def get_products_by_storage_temp(db: Session, storage_temp: str):
    """Return products that require a specific storage temperature."""
    return (
        db.query(Product)
        .filter(Product.storage_temp.ilike(f"%{storage_temp}%"))
        .all()
    )


# QUERY LOG

def log_query(db: Session, question: str, answer: str, tokens_used: int = 0, user_id: int = None):
    """
    Save every question + answer to the queries table.
    Wrapped in try/except with rollback — if the insert fails,
    we roll back the session so it doesn't stay in a broken state.
    """
    try:
        query_log = Query(
            question=question,
            answer=answer,
            tokens_used=tokens_used,
            user_id=user_id
        )
        db.add(query_log)
        db.commit()
        db.refresh(query_log)
        return query_log
    except Exception as e:
        db.rollback()  # fix: without this, failed transaction breaks the session
        raise e


def get_recent_queries(db: Session, limit: int = 10):
    """Return the most recent N queries made to the assistant."""
    return (
        db.query(Query)
        .order_by(desc(Query.created_at))
        .limit(limit)
        .all()
    )


def get_queries_by_user(db: Session, user_id: int):
    """Return all queries made by a specific user."""
    return (
        db.query(Query)
        .filter(Query.user_id == user_id)
        .order_by(desc(Query.created_at))
        .all()
    )


# USER QUERIES

def get_user_by_email(db: Session, email: str):
    """Look up a user by email — used during login."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Look up a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, hashed_password: str):
    """
    Create a new user.
    - Checks for duplicate email first to avoid raw IntegrityError
    - Wraps insert in try/except with rollback
    - Never accepts plain text password — hash before calling this
    """
    # fix: check duplicate before insert — gives clean error instead of raw IntegrityError
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError(f"User with email {email} already exists")

    try:
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()  # fix: rolls back broken session on failure
        raise e


def get_all_users(db: Session):
    """Return all registered users — admin use only."""
    return db.query(User).all()