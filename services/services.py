# распределение игроков между собой
import random


def random_assignment(user_ids):
    # Создаем список содержащий id юзеров
    users = [u_id[1] for u_id in user_ids]

    # Создаем копию списка users
    shuffled_ids = users.copy()

    # Перемешиваем элементы списка случайным образом
    random.shuffle(shuffled_ids)

    # Формируем пары (id, assigned_id)
    while any(user_id == assigned_id for user_id, assigned_id in zip(users, shuffled_ids)):
        random.shuffle(shuffled_ids)

    assignments = list(zip(users, shuffled_ids))

    return assignments
