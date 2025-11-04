# labyrinth_game/utils.py
import math

from constants import COMMANDS, ROOMS


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
    
  
    accepted_answers = [answer.lower()]
    if answer.lower() == '10':
        accepted_answers.append('десять')
    
    if user_answer in accepted_answers:
        print("Правильно! Загадка решена.")
        room_data['puzzle'] = None
        if current_room == 'hall':
            game_state['player_inventory'].append('hint')
            print("Награда: подсказка добавлена в инвентарь!")
        elif current_room == 'trap_room':
            print("Награда: путь безопасен!")
        else:
            print("Вы получили силу для дальнейшего пути!")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == 'trap_room':
            trigger_trap(game_state)  
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
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:<16} - {desc}")

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    result = math.floor(fractional * modulo)
    return result
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']
    
    if inventory:
        idx = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли: {lost_item}")
    else:
        damage = pseudo_random(steps, 10)
        if damage < 3:
            print("Вы не уцелели... Игра окончена поражением!")
            game_state['game_over'] = True
        else:
            print("Вы чудом живы.")
def random_event(game_state):
    steps = game_state['steps_taken']
    if pseudo_random(steps, 10) == 0:  
        event_type = pseudo_random(steps + 1, 3)  
        current_room = game_state['current_room']
        inventory = game_state['player_inventory']
        from constants import ROOMS
        room_data = ROOMS[current_room]
        if event_type == 0:
            room_data['items'].append('coin')
            print("Вы нашли на полу монетку!")
        elif event_type == 1:
            print("Вы слышите в темноте что-то.")
            if 'sword' in inventory:
                print("С мечом в руках вы отпугиваете кого-то!")
            else:
                print("Шорох затих... (на этот раз пронесло).")
        elif event_type == 2:
            if current_room == 'trap_room' and 'torch' not in inventory:
                print("Темнота усиливает опасность.")
                trigger_trap(game_state)
            else:
                print("Лёгкий шорох — ничего серьёзного.")
def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
