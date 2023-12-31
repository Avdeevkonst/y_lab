import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Menu(Base):
    __tablename__ = "menus"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenu = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete-orphan",
    )


class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu = relationship("Menu", back_populates="submenu")
    dishes = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete-orphan",
    )


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    submenu = relationship("Submenu", back_populates="dishes")
