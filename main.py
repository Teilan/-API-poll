import requests
from requests.exceptions import RequestException
from config import URL
from typing import Dict, Any, Tuple, Optional

# Tuple[Optional[Dict[str, Any]], Optional[str]]
def request(url: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Выполняет HTTP-запрос к API и возвращает данные или сообщение об ошибке. 
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data, None
    except RequestException as e:
        return None, e

def get_new_achievements(data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Определяет новые достижения пользователей между двумя наборами данных.
    """
    new_achievements = {}

    for user_id, user_data2 in data2.items():
        achievements2 = set(user_data2['achievements'].keys())
        achievements1 = set(data1.get(user_id, {}).get('achievements', {}).keys())
        new_achievements_list = achievements2 - achievements1
        if new_achievements_list:
            new_achievements[user_id] = {
                "metadata": user_data2["metadata"],
                "achievements": {achievement: True for achievement in new_achievements_list}
            }

    return new_achievements

def main(url: str) -> dict:
    """
    Основная функция для выполнения двух последовательных запросов и получения новых достижений.
    """
    data1, error = request(url)
    if error:
        return "Ошибка: во время запроса первого {error}."
    
    data2, error = request(url)
    if error:
        return "Ошибка: во время запроса второго {error}."
    
    return get_new_achievements(data1, data2)

if __name__ == "__main__":
    result = main(URL)
    print(result)
