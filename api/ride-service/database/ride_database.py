from datetime import datetime
import os
from typing import Optional, List

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Declarative base
Base = declarative_base()

# ORM models matching api/ride-service/models/ride_model.py
class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(String(36), primary_key=True, index=True)          # UUID
    user_id = Column(String(36), nullable=False, index=True)
    pickup_location = Column(String(255), nullable=False)
    dropoff_location = Column(String(255), nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    status = Column(String(32), default="requested", nullable=False)


class Ride(Base):
    __tablename__ = "rides"

    id = Column(String(36), primary_key=True, index=True)          # UUID
    ride_request_id = Column(String(36), ForeignKey("ride_requests.id"), nullable=False, index=True)
    driver_id = Column(String(36), nullable=True, index=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    fare = Column(Float, nullable=True)
    status = Column(String(32), default="requested", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


# Database URL (use env var in production)
DATABASE_URL = os.getenv(
    "RIDE_DATABASE_URL",
    "mysql+pymysql://root:Nikhil%40021@localhost:3306/rideapp?charset=utf8mb4",
)

# Engine and session factory
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create ride tables (safe to call at startup)."""
    Base.metadata.create_all(bind=engine)


# CRUD helpers for ride requests and rides

def create_ride_request(db: Session, req_data: dict) -> RideRequest:
    """
    req_data must contain: id (optional), user_id, pickup_location, dropoff_location, requested_at (optional), status (optional)
    """
    rr = RideRequest(
        id=req_data.get("id"),
        user_id=req_data["user_id"],
        pickup_location=req_data["pickup_location"],
        dropoff_location=req_data["dropoff_location"],
        requested_at=req_data.get("requested_at", datetime.utcnow()),
        status=req_data.get("status", "requested"),
    )
    try:
        db.add(rr)
        db.commit()
        db.refresh(rr)
        return rr
    except IntegrityError:
        db.rollback()
        raise


def get_ride_request_by_id(db: Session, request_id: str) -> Optional[RideRequest]:
    return db.query(RideRequest).filter(RideRequest.id == request_id).first()


def get_pending_ride_requests(db: Session) -> List[RideRequest]:
    return db.query(RideRequest).filter(RideRequest.status == "requested").all()


def update_ride_request_status(db: Session, request_id: str, status: str) -> Optional[RideRequest]:
    rr = get_ride_request_by_id(db, request_id)
    if not rr:
        return None
    rr.status = status
    rr.updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(rr)
        return rr
    except IntegrityError:
        db.rollback()
        raise


def create_ride(db: Session, ride_data: dict) -> Ride:
    """
    ride_data must contain: id (optional), ride_request_id, driver_id (optional), status (optional), start_time/end_time/fare optional
    """
    ride = Ride(
        id=ride_data.get("id"),
        ride_request_id=ride_data["ride_request_id"],
        driver_id=ride_data.get("driver_id"),
        start_time=ride_data.get("start_time"),
        end_time=ride_data.get("end_time"),
        fare=ride_data.get("fare"),
        status=ride_data.get("status", "requested"),
    )
    try:
        db.add(ride)
        db.commit()
        db.refresh(ride)
        return ride
    except IntegrityError:
        db.rollback()
        raise


def get_ride_by_id(db: Session, ride_id: str) -> Optional[Ride]:
    return db.query(Ride).filter(Ride.id == ride_id).first()


def assign_driver_to_ride(db: Session, ride_id: str, driver_id: str) -> Optional[Ride]:
    ride = get_ride_by_id(db, ride_id)
    if not ride:
        return None
    ride.driver_id = driver_id
    ride.status = "driver_assigned"
    ride.start_time = datetime.utcnow()
    ride.updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(ride)
        return ride
    except IntegrityError:
        db.rollback()
        raise


def update_ride_status(db: Session, ride_id: str, status: str) -> Optional[Ride]:
    ride = get_ride_by_id(db, ride_id)
    if not ride:
        return None
    ride.status = status
    # set end_time automatically if completed or canceled
    if status in ("completed", "canceled"):
        ride.end_time = ride.end_time or datetime.utcnow()
    ride.updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(ride)
        return ride
    except IntegrityError:
        db.rollback()
        raise