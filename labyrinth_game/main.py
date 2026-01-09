"""Точка входа в игру: цикл, обработка команд и управление состоянием."""

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

game_state = {
    "player_inventory": [],
    "current_room": "entrance",
    "game_over": False,
    "steps_taken": 0,
}


def process_command(state: dict, command: str, commands: dict) -> None:
    command = command.strip().lower()
    if not command:
        return

    # односложные направления без go
    if command in {"north", "south", "east", "west"}:
        move_player(state, command)
        return

    parts = command.split()
    action = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    match action:
        case "look":
            describe_current_room(state)

        case "inventory":
            show_inventory(state)

        case "go":
            if not arg:
                print("Укажите направление: go north/south/east/west")
                return
            move_player(state, arg)

        case "take":
            if not arg:
                print("Укажите предмет: take <item>")
                return
            take_item(state, arg)

        case "use":
            if not arg:
                print("Укажите предмет: use <item>")
                return
            use_item(state, arg)

        case "solve":
            if state["current_room"] == "treasure_room":
                attempt_open_treasure(state)
            else:
                solve_puzzle(state)

        case "help":
            show_help(commands)

        case "quit" | "exit":
            state["game_over"] = True

        case _:
            print("Неизвестная команда. Введите help.")


def main() -> None:
    print("Добро пожаловать в Лабиринт сокровищ!\n")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command, COMMANDS)

    print(
        "\nИгра завершена. Шагов сделано:",
        game_state["steps_taken"],
    )


if __name__ == "__main__":
    main()