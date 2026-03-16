from app.models import UsersOrm, PostsOrm, CommentsOrm
from app.db import session_factory

from sqlalchemy import select

from datetime import datetime, timedelta


async def seed_database_sqlalchemy():
    """Заполнение базы данных через SQLAlchemy ORM"""
    print("🌱 Начинаем заполнение базы данных...")

    async with session_factory() as session:
        try:
            # Проверяем, есть ли уже данные
            result = await session.execute(select(UsersOrm))
            if result.scalars().first():
                print("📊 Данные уже есть, пропускаем")
                return

            now = datetime.now()

            # ===== 1. СОЗДАЁМ ПОЛЬЗОВАТЕЛЕЙ =====
            users_data = [
                UsersOrm(
                    first_name="Иван",
                    last_name="Иванов",
                    age=25,
                    bio="Люблю программировать и путешествовать",
                    username="ivan_ivanov",
                    email="ivan@mail.ru",
                    phone="+79991234567",
                    is_active=True,
                    created_at=now - timedelta(days=30),
                    updated_at=now - timedelta(days=5),
                ),
                UsersOrm(
                    first_name="Мария",
                    last_name="Петрова",
                    age=28,
                    bio="Фотограф, блогер, мама",
                    username="maria_p",
                    email="maria@mail.ru",
                    phone="+79997654321",
                    is_active=True,
                    created_at=now - timedelta(days=28),
                    updated_at=now - timedelta(days=3),
                ),
                UsersOrm(
                    first_name="Петр",
                    last_name="Сидоров",
                    age=32,
                    bio="Автомеханик, люблю активный отдых",
                    username="petr_s",
                    email="petr@mail.ru",
                    phone="+79991112233",
                    is_active=True,
                    created_at=now - timedelta(days=25),
                    updated_at=now - timedelta(days=10),
                ),
                UsersOrm(
                    first_name="Анна",
                    last_name="Кузнецова",
                    age=22,
                    bio="Студентка, учусь на дизайнера",
                    username="anna_kuz",
                    email="anna@mail.ru",
                    phone="+79994445566",
                    is_active=True,
                    created_at=now - timedelta(days=20),
                    updated_at=now - timedelta(days=2),
                ),
                UsersOrm(
                    first_name="Алексей",
                    last_name="Смирнов",
                    age=35,
                    bio="Team Lead, наставник",
                    username="alex_s",
                    email="alex@mail.ru",
                    phone="+79997778899",
                    is_active=True,
                    created_at=now - timedelta(days=15),
                    updated_at=now - timedelta(days=1),
                ),
                UsersOrm(
                    first_name="Елена",
                    last_name="Попова",
                    age=29,
                    bio="Маркетолог, SMM-специалист",
                    username="elena_pop",
                    email="elena@mail.ru",
                    phone="+79993334455",
                    is_active=True,
                    created_at=now - timedelta(days=12),
                    updated_at=now - timedelta(days=4),
                ),
                UsersOrm(
                    first_name="Дмитрий",
                    last_name="Лебедев",
                    age=41,
                    bio="Фрилансер, веб-разработчик",
                    username="dima_leb",
                    email="dima@mail.ru",
                    phone="+79996667788",
                    is_active=False,
                    created_at=now - timedelta(days=40),
                    updated_at=now - timedelta(days=20),
                ),
                UsersOrm(
                    first_name="Ольга",
                    last_name="Козлова",
                    age=27,
                    bio="Бухгалтер, люблю читать",
                    username="olga_koz",
                    email="olga@mail.ru",
                    phone="+79995556677",
                    is_active=True,
                    created_at=now - timedelta(days=18),
                    updated_at=now - timedelta(days=6),
                ),
                UsersOrm(
                    first_name="Сергей",
                    last_name="Новиков",
                    age=33,
                    bio="Системный администратор",
                    username="sergey_nov",
                    email="sergey@mail.ru",
                    phone="+79998889900",
                    is_active=True,
                    created_at=now - timedelta(days=22),
                    updated_at=now - timedelta(days=7),
                ),
                UsersOrm(
                    first_name="Наталья",
                    last_name="Морозова",
                    age=26,
                    bio="Преподаватель английского",
                    username="natalya_mor",
                    email="natalya@mail.ru",
                    phone="+79990001122",
                    is_active=True,
                    created_at=now - timedelta(days=10),
                    updated_at=now - timedelta(days=2),
                ),
            ]

            session.add_all(users_data)
            await session.flush()
            print(f"   ✅ Создано {len(users_data)} пользователей")

            # Словарь для быстрого доступа к пользователям по индексу
            users = users_data

            # ===== 2. СОЗДАЁМ ПОСТЫ =====
            posts_data = [
                PostsOrm(
                    title="Как начать программировать",
                    content="Многие думают, что программирование — это сложно. На самом деле... Достаточно начать с простого и практиковаться каждый день. В этой статье я расскажу о своем опыте.",
                    views_count=1250,
                    likes_count=45,
                    user_id=users[0].id,
                    created_at=now - timedelta(days=25),
                    updated_at=now - timedelta(days=20),
                ),
                PostsOrm(
                    title="Путешествие на Байкал",
                    content="Прошлым летом я посетила озеро Байкал. Это невероятное место... Чистейшая вода, красивые пейзажи и добрые люди.",
                    views_count=890,
                    likes_count=32,
                    user_id=users[1].id,
                    created_at=now - timedelta(days=20),
                    updated_at=now - timedelta(days=15),
                ),
                PostsOrm(
                    title="Как выбрать автомобиль",
                    content="Покупка автомобиля — ответственный шаг. Нужно учитывать множество факторов... Бюджет, состояние, год выпуска и многое другое.",
                    views_count=2100,
                    likes_count=78,
                    user_id=users[2].id,
                    created_at=now - timedelta(days=18),
                    updated_at=now - timedelta(days=12),
                ),
                PostsOrm(
                    title="Тренды веб-дизайна 2024",
                    content="В этом году в дизайне популярны минимализм, неоновые акценты... и асимметричные макеты. Рассказываю подробнее.",
                    views_count=1500,
                    likes_count=56,
                    user_id=users[3].id,
                    created_at=now - timedelta(days=15),
                    updated_at=now - timedelta(days=10),
                ),
                PostsOrm(
                    title="Как управлять командой разработчиков",
                    content="Быть тимлидом — это не только про технологии, но и про людей... Делиться опытом, помогать расти и не выгорать самому.",
                    views_count=3200,
                    likes_count=120,
                    user_id=users[4].id,
                    created_at=now - timedelta(days=12),
                    updated_at=now - timedelta(days=5),
                ),
                PostsOrm(
                    title="SMM продвижение для начинающих",
                    content="Социальные сети — мощный инструмент для бизнеса... Главное — понимать свою аудиторию и создавать полезный контент.",
                    views_count=780,
                    likes_count=23,
                    user_id=users[5].id,
                    created_at=now - timedelta(days=10),
                    updated_at=now - timedelta(days=8),
                ),
                PostsOrm(
                    title="Python для автоматизации",
                    content="Python отлично подходит для автоматизации рутинных задач... Парсинг, работа с Excel, отправка писем.",
                    views_count=1800,
                    likes_count=67,
                    user_id=users[6].id,
                    created_at=now - timedelta(days=30),
                    updated_at=now - timedelta(days=25),
                ),
                PostsOrm(
                    title="Как вести личный бюджет",
                    content="Финансовая грамотность важна для каждого... Рассказываю о приложениях и методах учета расходов.",
                    views_count=950,
                    likes_count=34,
                    user_id=users[7].id,
                    created_at=now - timedelta(days=14),
                    updated_at=now - timedelta(days=9),
                ),
                PostsOrm(
                    title="Настройка сервера под Linux",
                    content="Пошаговое руководство по настройке сервера для начинающих... Выбор ОС, установка, безопасность.",
                    views_count=2700,
                    likes_count=89,
                    user_id=users[8].id,
                    created_at=now - timedelta(days=20),
                    updated_at=now - timedelta(days=15),
                ),
                PostsOrm(
                    title="Как выучить английский самостоятельно",
                    content="Реальные советы от преподавателя: приложения, сериалы, общение... Главное — регулярность и интерес.",
                    views_count=1600,
                    likes_count=52,
                    user_id=users[9].id,
                    created_at=now - timedelta(days=8),
                    updated_at=now - timedelta(days=3),
                ),
                PostsOrm(
                    title="Второй пост Ивана",
                    content="Продолжаю делиться опытом в программировании. Сегодня поговорим об алгоритмах...",
                    views_count=450,
                    likes_count=15,
                    user_id=users[0].id,
                    created_at=now - timedelta(days=10),
                    updated_at=now - timedelta(days=7),
                ),
                PostsOrm(
                    title="Еще один пост Петра",
                    content="Советы по ремонту автомобиля своими руками. Экономим бюджет...",
                    views_count=680,
                    likes_count=22,
                    user_id=users[2].id,
                    created_at=now - timedelta(days=7),
                    updated_at=now - timedelta(days=5),
                ),
            ]

            session.add_all(posts_data)
            await session.flush()
            print(f"   ✅ Создано {len(posts_data)} постов")

            # ===== 3. СОЗДАЁМ КОММЕНТАРИИ =====
            comments_data = [
                CommentsOrm(
                    content="Отличная статья! Очень помогла новичкам.",
                    likes_count=12,
                    user_id=users[1].id,
                    post_id=posts_data[0].id,
                    created_at=now - timedelta(days=24),
                    updated_at=now - timedelta(days=24),
                ),
                CommentsOrm(
                    content="Спасибо, буду пробовать!",
                    likes_count=5,
                    user_id=users[2].id,
                    post_id=posts_data[0].id,
                    created_at=now - timedelta(days=23),
                    updated_at=now - timedelta(days=23),
                ),
                CommentsOrm(
                    content="Красивые фото! Тоже хочу на Байкал.",
                    likes_count=8,
                    user_id=users[0].id,
                    post_id=posts_data[1].id,
                    created_at=now - timedelta(days=19),
                    updated_at=now - timedelta(days=19),
                ),
                CommentsOrm(
                    content="Были там в прошлом году, согласна с автором.",
                    likes_count=4,
                    user_id=users[3].id,
                    post_id=posts_data[1].id,
                    created_at=now - timedelta(days=18),
                    updated_at=now - timedelta(days=18),
                ),
                CommentsOrm(
                    content="Полезная информация для тех, кто выбирает авто.",
                    likes_count=7,
                    user_id=users[0].id,
                    post_id=posts_data[2].id,
                    created_at=now - timedelta(days=17),
                    updated_at=now - timedelta(days=17),
                ),
                CommentsOrm(
                    content="А что думаете про электромобили?",
                    likes_count=3,
                    user_id=users[9].id,
                    post_id=posts_data[2].id,
                    created_at=now - timedelta(days=16),
                    updated_at=now - timedelta(days=16),
                ),
                CommentsOrm(
                    content="Дизайн реально меняется. Спасибо за обзор!",
                    likes_count=6,
                    user_id=users[4].id,
                    post_id=posts_data[3].id,
                    created_at=now - timedelta(days=14),
                    updated_at=now - timedelta(days=14),
                ),
                CommentsOrm(
                    content="Жду продолжения про UI/UX.",
                    likes_count=2,
                    user_id=users[6].id,
                    post_id=posts_data[3].id,
                    created_at=now - timedelta(days=13),
                    updated_at=now - timedelta(days=13),
                ),
                CommentsOrm(
                    content="Крутой материал для тимлидов. Сохранил в закладки.",
                    likes_count=15,
                    user_id=users[1].id,
                    post_id=posts_data[4].id,
                    created_at=now - timedelta(days=11),
                    updated_at=now - timedelta(days=11),
                ),
                CommentsOrm(
                    content="А как мотивировать команду, если нет бюджета на премии?",
                    likes_count=9,
                    user_id=users[3].id,
                    post_id=posts_data[4].id,
                    created_at=now - timedelta(days=10),
                    updated_at=now - timedelta(days=10),
                ),
                CommentsOrm(
                    content="Наконец-то понятное объяснение про SMM.",
                    likes_count=5,
                    user_id=users[8].id,
                    post_id=posts_data[5].id,
                    created_at=now - timedelta(days=9),
                    updated_at=now - timedelta(days=9),
                ),
                CommentsOrm(
                    content="А какой бюджет нужен для старта?",
                    likes_count=2,
                    user_id=users[0].id,
                    post_id=posts_data[5].id,
                    created_at=now - timedelta(days=8),
                    updated_at=now - timedelta(days=8),
                ),
                CommentsOrm(
                    content="Python рулит! Спасибо за статью.",
                    likes_count=11,
                    user_id=users[2].id,
                    post_id=posts_data[6].id,
                    created_at=now - timedelta(days=28),
                    updated_at=now - timedelta(days=28),
                ),
                CommentsOrm(
                    content="Подскажите библиотеку для парсинга сайтов.",
                    likes_count=4,
                    user_id=users[4].id,
                    post_id=posts_data[6].id,
                    created_at=now - timedelta(days=27),
                    updated_at=now - timedelta(days=27),
                ),
                CommentsOrm(
                    content="Очень актуальная тема про бюджет.",
                    likes_count=7,
                    user_id=users[5].id,
                    post_id=posts_data[7].id,
                    created_at=now - timedelta(days=13),
                    updated_at=now - timedelta(days=13),
                ),
                CommentsOrm(
                    content="Пользуюсь тем же приложением, удобно.",
                    likes_count=3,
                    user_id=users[1].id,
                    post_id=posts_data[7].id,
                    created_at=now - timedelta(days=12),
                    updated_at=now - timedelta(days=12),
                ),
                CommentsOrm(
                    content="Для новичка самое то!",
                    likes_count=6,
                    user_id=users[7].id,
                    post_id=posts_data[8].id,
                    created_at=now - timedelta(days=19),
                    updated_at=now - timedelta(days=19),
                ),
                CommentsOrm(
                    content="А какую ОС лучше выбрать для начала?",
                    likes_count=2,
                    user_id=users[9].id,
                    post_id=posts_data[8].id,
                    created_at=now - timedelta(days=18),
                    updated_at=now - timedelta(days=18),
                ),
                CommentsOrm(
                    content="Спасибо за советы! Очень мотивирует.",
                    likes_count=5,
                    user_id=users[0].id,
                    post_id=posts_data[9].id,
                    created_at=now - timedelta(days=7),
                    updated_at=now - timedelta(days=7),
                ),
                CommentsOrm(
                    content="А сколько времени нужно заниматься в день?",
                    likes_count=3,
                    user_id=users[2].id,
                    post_id=posts_data[9].id,
                    created_at=now - timedelta(days=6),
                    updated_at=now - timedelta(days=6),
                ),
            ]

            session.add_all(comments_data)
            await session.flush()
            print(f"   ✅ Создано {len(comments_data)} комментариев")

            # ===== 4. СОХРАНЯЕМ ВСЕ ИЗМЕНЕНИЯ =====
            await session.commit()

            # ===== 5. СТАТИСТИКА =====
            print("\n📊 СТАТИСТИКА БАЗЫ ДАННЫХ:")
            print(f"   👤 Пользователей: {len(users_data)}")
            print(f"   📝 Постов: {len(posts_data)}")
            print(f"   💬 Комментариев: {len(comments_data)}")

            print("\n✅ База данных успешно заполнена!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при заполнении базы: {e}")
            raise
