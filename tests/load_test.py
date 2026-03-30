import asyncio
import aiohttp
import random
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def create_user(session, user_id):
    """Создать одного пользователя"""
    data = {
        "username": f"async_user_{user_id}_{random.randint(1, 9999)}",
        "email": f"async_{user_id}_{random.randint(1, 9999)}@test.com",
        "first_name": f"User{user_id}",
        "last_name": "Async",
        "age": random.randint(18, 60),
        "phone": f"+7999{random.randint(1000000, 9999999)}"
    }
    
    try:
        async with session.post(f"{BASE_URL}/users/", json=data) as response:
            return response.status
    except Exception as e:
        return f"Error: {e}"

async def get_users(session):
    """Получить список пользователей"""
    try:
        async with session.get(f"{BASE_URL}/users/") as response:
            return response.status
    except Exception as e:
        return f"Error: {e}"

async def get_404(session, user_id):
    """Получить несуществующего пользователя (404)"""
    try:
        async with session.get(f"{BASE_URL}/users/{9999 + user_id}") as response:
            return response.status
    except Exception as e:
        return f"Error: {e}"

async def run_load_test(duration: int = 30, concurrency: int = 10):
    """
    Запуск асинхронной нагрузки
    duration: сколько секунд работает тест
    concurrency: сколько параллельных запросов
    """
    print(f"🚀 Запуск асинхронного нагрузочного теста")
    print(f"   Длительность: {duration} сек")
    print(f"   Параллельных запросов: {concurrency}")
    print(f"   Начало: {datetime.now().strftime('%H:%M:%S')}\n")
    
    start_time = time.time()
    request_count = 0
    error_count = 0
    
    # Создаём сессию
    async with aiohttp.ClientSession() as session:
        # Функция, которая будет выполняться в цикле
        async def worker():
            nonlocal request_count, error_count
            while time.time() - start_time < duration:
                # Выбираем случайный тип запроса
                choice = random.choices(
                    ['create', 'get', '404'],
                    weights=[0.3, 0.6, 0.1]  # 30% создание, 60% получение, 10% ошибки
                )[0]
                
                if choice == 'create':
                    status = await create_user(session, random.randint(1, 1000))
                elif choice == 'get':
                    status = await get_users(session)
                else:
                    status = await get_404(session, random.randint(1, 100))
                
                request_count += 1
                if isinstance(status, int) and status >= 400:
                    error_count += 1
                
                # Небольшая задержка между запросами (имитация)
                await asyncio.sleep(random.uniform(0.01, 0.05))
        
        # Запускаем workers параллельно
        tasks = [asyncio.create_task(worker()) for _ in range(concurrency)]
        
        # Ждём завершения
        await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    rps = request_count / elapsed
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Всего запросов: {request_count}")
    print(f"   Ошибок: {error_count}")
    print(f"   Время: {elapsed:.2f} сек")
    print(f"   RPS: {rps:.1f} запросов/сек")
    print(f"   Завершено: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(run_load_test(duration=30, concurrency=10))