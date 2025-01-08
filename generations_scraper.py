import requests
import json
import time

# 🔧 Настройки
BASE_URL = "https://mike-auto.ru/api/proxy/filter/filter"
HEADERS = {
    "Referer": "https://mike-auto.ru/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# 📋 Вводим manufacturerId
manufacturer_id = 140  # Toyota
models = {}


# 🚀 Функция для получения моделей по manufacturerId
def fetch_models(manufacturer_id):
    page = 1
    while True:
        try:
            params = {
                "manufacturerId": manufacturer_id,
                "modelId": "",
                "page": page,
            }
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            # Перебираем автомобили и извлекаем модели
            for car in data["data"]:
                model_id = car["model_id"]
                model_name = car["model_name"]

                if manufacturer_id not in models:
                    models[manufacturer_id] = []

                if not any(
                    model["id"] == model_id for model in models[manufacturer_id]
                ):
                    models[manufacturer_id].append({"id": model_id, "name": model_name})

            print(f"✅ Страница {page} обработана.")

            if page >= data["pageCount"]:
                break

            page += 1
            time.sleep(0.5)  # ⏱ Пауза между запросами

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса на странице {page}: {e}")
            break


# 📂 Сохранение результата в файл models.js
def save_to_file():
    with open("models.js", "w", encoding="utf-8") as f:
        f.write(
            "const models = " + json.dumps(models, indent=4, ensure_ascii=False) + ";"
        )
    print("✅ Данные сохранены в models.js")


# 🔄 Запуск скрипта
fetch_models(manufacturer_id)
save_to_file()
