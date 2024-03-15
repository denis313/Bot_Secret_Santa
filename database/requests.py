from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError
from database.model import User, Questionnaire, GiftList, Base, GenerateGifts


class DatabaseManager:
    def __init__(self, dsn):
        self.engine = create_async_engine(dsn, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.async_session() as session:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    # add new user from db
    async def add_user(self, user_data):
        try:
            async with self.async_session() as session:
                new_user = User(**user_data)
                session.add(new_user)
                await session.commit()
        except IntegrityError:
            print(f"Пользователь с user_id {user_data['user_id']} уже существует.")

    # add questionnaire for user from db
    async def add_questionnaire(self, questionnaire_data):
        async with self.async_session() as session:
            new_questionnaire = Questionnaire(**questionnaire_data)
            session.add(new_questionnaire)
            await session.commit()

    # add gift list for user from db
    async def add_gift_list(self, gift_list_data):
        async with self.async_session() as session:
            new_gift_list = GiftList(**gift_list_data)
            session.add(new_gift_list)
            await session.commit()

    # add generate gifts from db
    async def add_generate_gift(self, gifts_data):
        async with self.async_session() as session:
            new_gift_list = GenerateGifts(**gifts_data)
            session.add(new_gift_list)
            await session.commit()

    # get user by user_id from db
    async def get_user_by_id(self, user_id):
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar()
            return user

    # get all users from db
    async def get_all_users(self, id_chat):
        async with self.async_session() as session:
            result = await session.execute(select(User).filter(User.chat_id == id_chat))
            all_users = result.scalars()
            users = [[user.id, user.user_id, user.chat_id, user.creator_id, user.game_status, user.id_secret_friend]
                     for user in all_users]
            return users

    # get questionnaire by user_id from db
    async def get_questionnaire_by_id(self, user_id):
        async with self.async_session() as session:
            query = select(Questionnaire).filter(Questionnaire.user_id == user_id)
            result = await session.execute(query)
            questionnaires = result.scalar()
            return questionnaires if questionnaires is not None else None

    # get gift list by user_id from db
    async def get_gift_list(self, user_id):
        async with self.async_session() as session:
            g_l = select(GiftList).filter(GiftList.user_id == user_id)
            result = await session.execute(g_l)
            gift_list = result.scalar()
            return gift_list if gift_list is not None else None

    # get generate gift by user_id from db
    async def get_generate_gift(self, user_id, name_gift):
        async with self.async_session() as session:
            stmt = select(GenerateGifts).where(
                (GenerateGifts.user_id == user_id) & (GenerateGifts.gift == name_gift)
            )
            result = await session.execute(stmt)
            gift_list = result.scalars()
            return gift_list

    # update user by user_id or chat_id from db

    async def update_user(self, user_id=None, chat_id=None, user_data=None):
        async with self.async_session() as session:
            # Проверяем, что передан хотя бы один из user_id или chat_id
            if user_id is not None or chat_id is not None:
                # Создаем выражение для обновления записи
                stmt = update(User).where((User.user_id == user_id) | (User.chat_id == chat_id)).values(user_data)

                # Выполняем обновление
                await session.execute(stmt)
                await session.commit()
            else:
                # Логика обработки ошибки или просто возвращение, в зависимости от вашего случая
                print("Ошибка: Не передан user_id или chat_id")

    # update questionnaire by user_id from db
    async def update_questionnaire(self, user_id, questionnaire_data):
        async with self.async_session() as session:
            stmt = update(Questionnaire).where(Questionnaire.user_id == user_id).values(questionnaire_data)
            await session.execute(stmt)
            await session.commit()

    # update gift_list by user_id from db
    async def update_gift_list(self, user_id, list_data):
        async with self.async_session() as session:
            stmt = update(GiftList).where(GiftList.user_id == user_id).values(list_data)
            await session.execute(stmt)
            await session.commit()

    # update generate list by user_id from db
    async def update_generate_gift(self, user_id, list_data):
        async with self.async_session() as session:
            stmt = update(GenerateGifts).where(GenerateGifts.user_id == user_id).values(list_data)

            await session.execute(stmt)
            await session.commit()

    # delete user
    async def delete_user(self, user_id):
        async with self.async_session() as session:
            stmt = delete(User).where(User.user_id == user_id)

            await session.execute(stmt)
            await session.commit()

    # delete generate list
    async def delete_gifts(self, user_id):
        async with self.async_session() as session:
            stmt = delete(GenerateGifts).where(GenerateGifts.user_id == user_id)

            await session.execute(stmt)
            await session.commit()
