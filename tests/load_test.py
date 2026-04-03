import asyncio
import aiohttp
import random
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Список всех эндпоинтов для тестирования
ENDPOINTS = [
    {"method": "GET", "path": "/users/"},
    {"method": "POST", "path": "/users/", "data": True},  # с данными
    {"method": "GET", "path": "/users/{id}"},  # динамический ID
    {"method": "PUT", "path": "/users/{id}", "data": True},
    {"method": "DELETE", "path": "/users/{id}"},
    {"method": "GET", "path": "/posts/"},
    {"method": "POST", "path": "/posts/", "data": True},
    {"method": "GET", "path": "/posts/{id}"},
    {"method": "PUT", "path": "/posts/{id}", "data": True},
    {"method": "DELETE", "path": "/posts/{id}"},
    {"method": "GET", "path": "/comments/"},
    {"method": "POST", "path": "/comments/", "data": True},
    {"method": "GET", "path": "/comments/{id}"},
    {"method": "PUT", "path": "/comments/{id}", "data": True},
    {"method": "DELETE", "path": "/comments/{id}"},
    {"method": "GET", "path": "/users/with-rel"},  # специальный эндпоинт
    {"method": "GET", "path": "/posts/user/{user_id}"},  # посты пользователя
    {"method": "GET", "path": "/comments/post/{post_id}"},  # комментарии к посту
]

# Данные для POST/PUT запросов
USER_DATA = {
    "first_name": "Test",
    "last_name": "User",
    "age": 25,
    "bio": "Тестовый пользователь",
    "username": "test_user_{}",
    "email": "test{}@test.com",
    "phone": "+799900000{}"
}

POST_DATA = {
    "title": "Тестовый пост {}",
    "content": "Это содержание тестового поста. Здесь много текста для нагрузки.",
    "user_id": None  # будет установлен динамически
}

COMMENT_DATA = {
    "content": "Тестовый комментарий {}",
    "user_id": None,
    "post_id": None
}


class LoadTester:
    def __init__(self):
        self.created_users = []
        self.created_posts = []
        self.created_comments = []
        self.request_count = 0
        self.error_count = 0
        self.stats = {}
    
    async def create_test_user(self, session, idx):
        """Создать тестового пользователя"""
        data = USER_DATA.copy()
        data["username"] = data["username"].format(idx)
        data["email"] = data["email"].format(idx)
        data["phone"] = data["phone"].format(idx)
        
        try:
            async with session.post(f"{BASE_URL}/users/", json=data) as resp:
                if resp.status == 201:
                    user = await resp.json()
                    self.created_users.append(user.get("id", idx))
                    return resp.status
                return resp.status
        except Exception:
            return 0
    
    async def create_test_post(self, session, idx, user_id):
        """Создать тестовый пост"""
        data = POST_DATA.copy()
        data["title"] = data["title"].format(idx)
        data["user_id"] = user_id
        
        try:
            async with session.post(f"{BASE_URL}/posts/", json=data) as resp:
                if resp.status == 201:
                    post = await resp.json()
                    self.created_posts.append(post.get("id", idx))
                    return resp.status
                return resp.status
        except Exception:
            return 0
    
    async def create_test_comment(self, session, idx, user_id, post_id):
        """Создать тестовый комментарий"""
        data = COMMENT_DATA.copy()
        data["content"] = data["content"].format(idx)
        data["user_id"] = user_id
        data["post_id"] = post_id
        
        try:
            async with session.post(f"{BASE_URL}/comments/", json=data) as resp:
                if resp.status == 201:
                    comment = await resp.json()
                    self.created_comments.append(comment.get("id", idx))
                    return resp.status
                return resp.status
        except Exception:
            return 0
    
    async def make_request(self, session, endpoint, idx):
        """Выполнить один запрос к эндпоинту"""
        method = endpoint["method"]
        path = endpoint["path"]
        
        # Подставляем ID, если нужно
        if "{id}" in path:
            if self.created_users:
                obj_id = random.choice(self.created_users)
                path = path.replace("{id}", str(obj_id))
            else:
                path = path.replace("{id}", "1")
        
        if "{user_id}" in path:
            if self.created_users:
                obj_id = random.choice(self.created_users)
                path = path.replace("{user_id}", str(obj_id))
            else:
                path = path.replace("{user_id}", "1")
        
        if "{post_id}" in path:
            if self.created_posts:
                obj_id = random.choice(self.created_posts)
                path = path.replace("{post_id}", str(obj_id))
            else:
                path = path.replace("{post_id}", "1")
        
        url = f"{BASE_URL}{path}"
        
        try:
            if method == "GET":
                async with session.get(url) as resp:
                    return resp.status
            elif method == "POST":
                # Создаём тестовые данные
                if "/users/" in path:
                    data = {"first_name": f"Load{idx}", "last_name": "Test", "age": 20,
                            "username": f"load{idx}_{random.randint(1,9999)}",
                            "email": f"load{idx}_{random.randint(1,9999)}@test.com",
                            "phone": f"+7999{random.randint(1000000,9999999)}"}
                elif "/posts/" in path:
                    user_id = self.created_users[0] if self.created_users else 1
                    data = {"title": f"Load Post {idx}", "content": "Test content", "user_id": user_id}
                else:
                    user_id = self.created_users[0] if self.created_users else 1
                    post_id = self.created_posts[0] if self.created_posts else 1
                    data = {"content": f"Load comment {idx}", "user_id": user_id, "post_id": post_id}
                
                async with session.post(url, json=data) as resp:
                    return resp.status
            elif method == "PUT":
                data = {"bio": f"Updated {idx}"}
                async with session.put(url, json=data) as resp:
                    return resp.status
            elif method == "DELETE":
                async with session.delete(url) as resp:
                    return resp.status
            else:
                return 0
        except Exception:
            return 0
    
    async def run(self, duration: int = 60, concurrency: int = 20):
        """Запуск нагрузочного теста"""
        print(f"🚀 ЗАПУСК НАГРУЗОЧНОГО ТЕСТА")
        print(f"   Длительность: {duration} сек")
        print(f"   Параллельных запросов: {concurrency}")
        print(f"   Начало: {datetime.now().strftime('%H:%M:%S')}\n")
        
        start_time = time.time()
        self.request_count = 0
        
        async with aiohttp.ClientSession() as session:
            # 1. Создаём тестовых пользователей
            print("📝 Создаём тестовых пользователей...")
            for i in range(5):
                status = await self.create_test_user(session, i)
                print(f"   User {i}: {status}")
            print(f"   Создано пользователей: {len(self.created_users)}\n")
            
            # 2. Создаём тестовые посты
            if self.created_users:
                print("📝 Создаём тестовые посты...")
                for i in range(10):
                    user_id = random.choice(self.created_users)
                    status = await self.create_test_post(session, i, user_id)
                    print(f"   Post {i}: {status}")
                print(f"   Создано постов: {len(self.created_posts)}\n")
            
            # 3. Создаём тестовые комментарии
            if self.created_posts and self.created_users:
                print("📝 Создаём тестовые комментарии...")
                for i in range(20):
                    user_id = random.choice(self.created_users)
                    post_id = random.choice(self.created_posts)
                    status = await self.create_test_comment(session, i, user_id, post_id)
                    print(f"   Comment {i}: {status}")
                print(f"   Создано комментариев: {len(self.created_comments)}\n")
            
            # 4. Основная нагрузка
            print("🔥 НАГРУЗКА (все эндпоинты)")
            print("   GET /users/, POST /users/, GET /users/{id}, PUT /users/{id}, DELETE /users/{id}")
            print("   GET /posts/, POST /posts/, GET /posts/{id}, PUT /posts/{id}, DELETE /posts/{id}")
            print("   GET /comments/, POST /comments/, GET /comments/{id}, PUT /comments/{id}, DELETE /comments/{id}")
            print("   GET /users/with-rel, GET /posts/user/{user_id}, GET /comments/post/{post_id}\n")
            
            async def worker():
                nonlocal start_time
                idx = 0
                while time.time() - start_time < duration:
                    # Выбираем случайный эндпоинт
                    endpoint = random.choice(ENDPOINTS)
                    status = await self.make_request(session, endpoint, idx)
                    
                    self.request_count += 1
                    if status >= 400 or status == 0:
                        self.error_count += 1
                    
                    # Сохраняем статистику по эндпоинту
                    key = f"{endpoint['method']} {endpoint['path']}"
                    if key not in self.stats:
                        self.stats[key] = {"total": 0, "errors": 0}
                    self.stats[key]["total"] += 1
                    if status >= 400 or status == 0:
                        self.stats[key]["errors"] += 1
                    
                    idx += 1
                    # Небольшая задержка между запросами
                    await asyncio.sleep(random.uniform(0.02, 0.1))
            
            # Запускаем воркеры
            tasks = [asyncio.create_task(worker()) for _ in range(concurrency)]
            await asyncio.gather(*tasks)
        
        elapsed = time.time() - start_time
        rps = self.request_count / elapsed
        
        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"   Всего запросов: {self.request_count}")
        print(f"   Ошибок: {self.error_count} ({self.error_count/self.request_count*100:.1f}%)")
        print(f"   Время: {elapsed:.2f} сек")
        print(f"   RPS: {rps:.1f} запросов/сек")
        print(f"   Завершено: {datetime.now().strftime('%H:%M:%S')}\n")
        
        # Статистика по эндпоинтам
        print("📈 СТАТИСТИКА ПО ЭНДПОИНТАМ:")
        for key, data in sorted(self.stats.items(), key=lambda x: x[1]["total"], reverse=True):
            error_rate = data["errors"] / data["total"] * 100 if data["total"] > 0 else 0
            print(f"   {key}: {data['total']} запросов, ошибки: {error_rate:.1f}%")


async def main():
    tester = LoadTester()
    await tester.run(duration=60, concurrency=20)


if __name__ == "__main__":
    asyncio.run(main())