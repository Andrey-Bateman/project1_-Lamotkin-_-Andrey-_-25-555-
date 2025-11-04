#!/usr/bin/env python3
from player_actions import move_player, show_inventory, take_item, use_item
from utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    show_help,
    solve_puzzle,
)

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command):
    parts = command.lower().strip().split()
    if not parts:
        return
    
    action = parts[0]
    arg = parts[1] if len(parts) > 1 else None
    
    
    if action in ['north', 'south', 'east', 'west']:
        move_player(game_state, action)
        return
    
    match action:
        case "go":
            if arg and arg in ['north', 'south', 'east', 'west']:
                move_player(game_state, arg)
            else:
                print("Укажите направление: north, south, east, west.")
        case "look":
            describe_current_room(game_state)
        case "take":
            if arg:
                if arg == "treasure_chest" and game_state['current_room'] == 'treasure_room':
                    print("Вы не можете поднять сундук, он слишком тяжелый.")
                else:
                    take_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "inventory":
            show_inventory(game_state)
        case "solve":
            current = game_state['current_room']
            if current == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("Спасибо за игру!")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")
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
