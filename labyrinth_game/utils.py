import math

from labyrinth_game.constants import (
    EVENT_PROBABILITY_MODULO,
    EVENT_TYPES_COUNT,
    ROOMS,
    TRAP_DAMAGE_MODULO,
    TRAP_DEATH_THRESHOLD,
)
from labyrinth_game.player_actions import get_input


def describe_current_room(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"== {room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:", ", ".join(room["items"]))

    print("Выходы:", ", ".join(room["exits"].keys()))

    if room["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help(commands: dict) -> None:
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        left = (cmd + " " * 16)[:16]
        print(f"  {left} - {desc}")


def solve_puzzle(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    puzzle = room["puzzle"]

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)

    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct = str(answer).strip().lower()

    alternatives = {correct}
    if correct == "10":
        alternatives.add("десять")

    if user_answer in alternatives:
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        reward_by_room = {
            "hall": "coin",
            "library": "hint_scroll",
            "trap_room": "bandage",
        }
        reward = reward_by_room.get(room_name, "coin")

        if reward not in game_state["player_inventory"]:
            game_state["player_inventory"].append(reward)
            print("Вы получили награду:", reward)
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    room = ROOMS[game_state["current_room"]]

    if "treasure_chest" not in room["items"]:
        print("Здесь нет сундука.")
        return

    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    answer = get_input("Сундук заперт. Ввести код? (да/нет) ").strip().lower()
    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    code = get_input("Введите код: ").strip().lower()

    puzzle = room["puzzle"]
    if puzzle is None:
        print("Кодовая защита не активна.")
        return

    _, correct_code = puzzle
    if code == str(correct_code).strip().lower():
        print("Код верный! Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Код неверный.")

def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    value = frac * modulo
    return int(math.floor(value))


def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        idx = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(idx)
        print("Вы потеряли предмет:", lost_item)
        return

    roll = pseudo_random(game_state["steps_taken"], TRAP_DAMAGE_MODULO)  # 0..9
    if roll < TRAP_DEATH_THRESHOLD:
        print("Вы не успели среагировать. Это конец пути...")
        game_state["game_over"] = True
    else:
        print("Вы чудом уцелели и продолжили путь.")


def random_event(game_state: dict) -> None:
    # событие с низкой вероятностью: 1 раз из 10
    happens = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY_MODULO) == 0
    if not happens:
        return

    event_type = pseudo_random(game_state["steps_taken"] + 1, EVENT_TYPES_COUNT)

    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("Находка! Вы замечаете на полу монетку.")
        if "coin" not in room["items"]:
            room["items"].append("coin")

    elif event_type == 1:
        print("Испуг! Вы слышите шорох где-то рядом...")
        if "sword" in inventory:
            print("Вы достаете меч и отпугиваете существо.")

    else:
        # ловушка только в trap_room, если нет torch
        if current_room == "trap_room" and "torch" not in inventory:
            print("Опасность! Без света легко угодить в ловушку...")
            trigger_trap(game_state)
