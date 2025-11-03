#!/usr/bin/env python3
from constants import ROOMS
from player_actions import get_input, show_inventory
from utils import describe_current_room

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command):
    parts = command.lower().split()
    if not parts:
        return
    
    action = parts[0]
    arg = parts[1] if len(parts) > 1 else None
    
    match action:
        case "go":
            if arg:
                from player_actions import move_player
                move_player(game_state, arg)
            else:
                print("Укажите направление: north, south, east, west.")
        case "look":
            from utils import describe_current_room
            describe_current_room(game_state)
        case "take":
            if arg == "treasure_chest" and game_state['current_room'] == 'treasure_room':
                from utils import attempt_open_treasure  
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            elif arg:
                from player_actions import take_item
                take_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "inventory":
            from player_actions import show_inventory
            show_inventory(game_state)
        case "use":
            if arg:
                from player_actions import use_item
                use_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "solve":
            from utils import solve_puzzle
            solve_puzzle(game_state)
            # Для treasure_room
            if game_state['current_room'] == 'treasure_room':
                from utils import attempt_open_treasure
                attempt_open_treasure(game_state)
        case "help":
            from utils import show_help
            show_help()
        case "quit" | "exit":
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда.")

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)
    
    if game_state['game_over']:
        print("Игра окончена!")

if __name__ == "__main__":
    main()
