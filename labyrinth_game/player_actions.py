# labyrinth_game/player_actions.py

from constants import ROOMS

def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        
        if new_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
       
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
       
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"\nВы переместились в {new_room}.")
        from utils import describe_current_room
        describe_current_room(game_state)
        from utils import random_event
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room = game_state['current_room']
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
            print("Вы зажгли факел. Стало светлее!")
        case "sword":
            print("Вы чувствуете себя увереннее с мечом в руках.")
        case "bronze_box":
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Вы открыли шкатулку. Внутри ржавый ключ!")
            else:
                print("Шкатулка пуста.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")
