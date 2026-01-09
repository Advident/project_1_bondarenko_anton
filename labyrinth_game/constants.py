# labyrinth_game/constants.py
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. '
        'На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал '
        'с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 
                  'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: '
        '"Назовите число, которое идет после девяти". '
        'Введите ответ цифрой или словом.', '10')
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. '
          'На стене видна надпись: "Осторожно — ловушка".',
          "exits": {"west": "entrance", "north": "secret_tunnel"},
          'items': ['rusty_key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" '
          'три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. '
          'Где-то здесь может быть ключ от сокровищницы.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?" '
          '(ответ одно слово)', 'резонанс')  
    },
        'armory': {
          'description': 'Старая оружейная комната. '
          'На стене висит меч, рядом — небольшая бронзовая шкатулка.',
          "exits": {"south": "library", "east": "garden"},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе большой сундук. '
          'Дверь заперта — нужен особый ключ.',
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': ('Дверь защищена кодом. '
          'Введите код (подсказка: это число пятикратного шага, 2*5= ? )', '10')
    },
    # дополнительные комнаты
    "secret_tunnel": {
        "description": "Узкий секретный тоннель. Здесь сухо и тихо. Вдали виден свет.",
        "exits": {"south": "trap_room", "east": "hall"},
        "items": [],
        "puzzle": None,
    },
    "garden": {
        "description": "Небольшой внутренний сад. В каменной чаше лежит странный ключ.",
        "exits": {"west": "armory"},
        "items": ["treasure_key"],
        "puzzle": None,
    },
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "north/south/east/west": "короткая команда перемещения без go",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "help": "показать это сообщение",
    "quit": "выйти из игры",
}

# --- псевдослучайные события/ловушки ---
EVENT_PROBABILITY_MODULO = 10  # шанс события: 1 из 10
EVENT_TYPES_COUNT = 3          # 0..2

TRAP_DAMAGE_MODULO = 10        # 0..9
TRAP_DEATH_THRESHOLD = 3       # < 3 => game over