# labyrinth_game/utils.py
from constants import ROOMS  
from player_actions import get_input
def describe_current_room(game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    print(f"\n== {current_room.upper()} ==")
    
    print(room_data['description'])
    
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))
    else:
        print("Здесь нет заметных предметов.")
    
    print("Выходы:", ", ".join(room_data['exits'].keys()))
    
    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
def solve_puzzle(game_state):
    current_room = game_state['current_room']
    from constants import ROOMS
    room_data = ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, answer = room_data['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()
    
    if user_answer == answer.lower():
        print("Загадка решена.")
        room_data['puzzle'] = None
        print("Вы получили подсказку!")
    else:
        print("Неверно. Попробуйте снова.")
def attempt_open_treasure(game_state):
    current_room = game_state['current_room']
    if current_room != 'treasure_room':
        return  
    
    from constants import ROOMS
    room_data = ROOMS[current_room]
    inventory = game_state['player_inventory']
    
    
    if 'treasure_chest' in room_data['items'] and "take treasure_chest" in command:  
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    
    if 'treasure_key' in inventory:  
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    try_code = get_input("Сундук заперт. Хотите ввести код? (да/нет): ").strip().lower()
    if try_code == 'да':
        code = get_input("Введите код: ").strip()
        puzzle_answer = ROOMS['treasure_room']['puzzle'][1] if ROOMS['treasure_room']['puzzle'] else '10'
        if code == puzzle_answer:
            print("Код верный! Сундук открылят.")
            room_data['items'].remove('treasure_chest')
            print("В сундуке сокровища!")
            game_state['game_over'] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
