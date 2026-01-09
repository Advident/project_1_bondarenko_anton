"""Действия игрока: ввод, движение, инвентарь, взаимодействие с предметами."""

from labyrinth_game.constants import ROOMS


def get_input(prompt: str = "> ") -> str:
    """Безопасный ввод команды. При Ctrl+C/EOF возвращает 'quit'."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Открывает инвентарь"""
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state: dict, direction: str) -> None:
    """Движение игрока. После успешного перехода вызывается random_event()."""
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    exits = room["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    # апгрейд: вход в treasure_room только с rusty_key
    if next_room == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

    game_state["steps_taken"] += 1

    # вывод новой комнаты + случайное событие
    from labyrinth_game.utils import describe_current_room, random_event
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    room = ROOMS[game_state["current_room"]]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room["items"]:
        room["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Факел вспыхивает. Вокруг стало светлее.")
        return

    if item_name == "sword":
        print("Вы чувствуете уверенность, держа меч в руках.")
        return

    if item_name == "bronze_box":
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Вы открыли шкатулку и нашли rusty_key!")
        return

    print("Вы не знаете, как использовать этот предмет.")