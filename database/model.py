from typing import List, Optional

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, nullable=False, unique=True)
    chat_id = mapped_column(BigInteger, nullable=False)
    creator_id = mapped_column(BigInteger)
    game_status = mapped_column(BigInteger)
    id_secret_friend = mapped_column(BigInteger)
    subscription: Mapped[str] = mapped_column()

    questionnaires: Mapped[List["Questionnaire"]] = relationship(back_populates='user')
    gift_list: Mapped[List["GiftList"]] = relationship(back_populates='user')
    generate_gifts: Mapped[List["GenerateGifts"]] = relationship(back_populates='user')

    def __repr__(self) -> str:
        ...
        return f"User(id={self.id}, user_id={self.user_id}, chat_id={self.chat_id})"


class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                            nullable=False, unique=True)
    photo: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    sex: Mapped[str] = mapped_column()
    clothing_brand: Mapped[str] = mapped_column()
    color_palette: Mapped[str] = mapped_column()
    sizes: Mapped[str] = mapped_column()
    fashion_style: Mapped[str] = mapped_column()
    hobby: Mapped[str] = mapped_column()
    allergy: Mapped[str] = mapped_column()
    salty_or_sweet: Mapped[str] = mapped_column()
    dream: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column()
    user: Mapped["User"] = relationship(back_populates='questionnaires')

    def __repr__(self) -> str:
        ...
        return f"Questionnaires(id={self.id}, user_id={self.user_id})"


class GiftList(Base):
    __tablename__ = 'gift_list'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                            nullable=False, unique=True)
    list: Mapped[Optional[str]] = mapped_column()
    user: Mapped["User"] = relationship(back_populates='gift_list')

    def __repr__(self) -> str:
        ...
        return f"Giftlist(id={self.id}, user_id={self.user_id})"


class GenerateGifts(Base):
    __tablename__ = 'generate_gifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                            nullable=False)
    gift: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    shop: Mapped[str] = mapped_column()
    id_gift: Mapped[int] = mapped_column()
    brand: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    supplierRating: Mapped[float] = mapped_column()
    feedbacks: Mapped[int] = mapped_column()

    user: Mapped["User"] = relationship(back_populates='generate_gifts')

    def __repr__(self) -> str:
        ...
        return f"GenerateGifts(id={self.id}, user_id={self.user_id})"
