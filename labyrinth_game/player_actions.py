# labyrinth_game/player_actions.py
def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")
def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
from constants import ROOMS 

def move_player(game_state, direction):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        game_state['current_room'] = room_data['exits'][direction]
        game_state['steps_taken'] += 1
        print(f"\nВы переместились в {game_state['current_room']}.")
        from utils import describe_current_room  
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")
def take_item(game_state, item_name):
    current_room = game_state['current_room']
    from constants import ROOMS
    room_data = ROOMS[current_room]
    
    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    inventory = game_state['player_inventory']
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    
    match item_name.lower():
        case "torch":
            print("У вас есть факео!")
        case "sword":
            print("Вы нашли меч.")
        case "bronze_box":
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Вы открыли шкатулку. Внутри ключ с ироглифом!")
            else:
                print("Шкатулка пуста.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")
