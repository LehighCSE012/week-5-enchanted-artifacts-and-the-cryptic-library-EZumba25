import random

def acquire_item(inventory, item):
    """Appends the item to the inventory list and notifies the player."""
    inventory.append(item)
    print(f"You acquired a {item}!.")
    return inventory

def display_inventory(inventory):
    """Displays the player's current inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for idx, item in enumerate(inventory, 1):
            print(f"{idx}. {item}")

def player_attack(monster_health):
    """Simulates the player's attack on the monster."""
    print("You strike the monster for 15 damage!")
    return max(monster_health - 15, 0)

def monster_attack(player_health):
    """Simulates the monster's attack on the player."""
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        player_health = max(player_health - 20, 0)
    else:
        print("The monster hits you for 10 damage!")
        player_health = max(player_health - 10, 0)
    return player_health

# Adventure Game Functions
def display_player_status(player_health):
    """Displays the player's current health."""
    print(f"Your current health: {player_health}")

def handle_path_choice(player_health):
    """Randomly determines the player's path and adjusts health accordingly."""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health = min(player_health + 10, 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_health = max(player_health - 15, 0)
        if player_health == 0:
            print("You are barely alive!")
    return player_health
def discover_artifact(player_stats, artifacts, artifact_name):
    """Function to discover an artifact and apply its effects using a dictionary."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You discovered: {artifact_name} - {artifact['description']}")

        # Map artifact effects to corresponding actions
        effects_map = {
            'increases health': lambda: player_stats.update({'health': player_stats['health'] + artifact['power']}),
            'enhances attack': lambda: player_stats.update({'attack': player_stats['attack'] + artifact['power']}),
            'solves puzzles': lambda: print(f"{artifact_name} allows you to bypass puzzles!")
        }
        # Apply the artifact effect
        effect_action = effects_map.get(artifact['effect'])
        if effect_action:
            effect_action()
            if artifact['effect'] != 'solves puzzles':  # Only remove artifact if it doesn't solve puzzles
                print(f"{artifact_name} effect applied!")
            else:
                print(f"{artifact_name} will help you bypass puzzles in the future!")
        
        # Remove the artifact from the dictionary after being used
        del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")  
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Function to find and store a new clue."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Function to process dungeon rooms and challenges."""
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room

        print(f"\nEntering room: {room_description}")

        if challenge_type == "library":
            # Handle Cryptic Library challenge
            clues_list = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            
            selected_clues = random.sample(clues_list, 2)
            
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if 'staff_of_wisdom' in inventory:
                print("With the staff of wisdom, you understand the clues and bypass a puzzle!")
                player_stats['health'] += 10  # Update health as per puzzle outcome
            else:
                print("You must solve the puzzles yourself.")
        
        elif challenge_type == "puzzle":
            # Handle puzzle challenge, using the challenge_outcome
            print("A puzzle challenge! Let's see if you solve it...")
            if random.random() < 0.5:  # Random chance of solving the puzzle
                print(challenge_outcome[0])  # "Solved puzzle!"
                player_stats['health'] += challenge_outcome[2]  # Outcome health effect
            else:
                print(challenge_outcome[1])  # "Puzzle unsolved."
                player_stats['health'] += challenge_outcome[2]  # Outcome health effect
        
        elif challenge_type == "trap":
            # Handle trap challenge, using the challenge_outcome
            print("A trap! Be careful!")
            if random.random() < 0.7:  # Random chance of avoiding trap
                print(challenge_outcome[0])  # "Avoided trap!"
            else:
                print(challenge_outcome[1])  # "Triggered trap!"
                player_stats['health'] += challenge_outcome[2]  # Outcome health effect
        
        elif challenge_type == "none":
            # No challenge in this room, just describe it
            print("This room seems calm and without danger.")
        
        # After processing the challenge, if there is an item, the player can collect it
        if item:
            print(f"You found a {item}!")

    # Return updated player stats, inventory, and clues
    return player_stats, inventory, clues

def check_for_treasure(treasure_obtained_in_combat):
    """Function to check if a treasure is obtained."""
    if treasure_obtained_in_combat:
        print("You have obtained a treasure!")

def combat_encounter(player_stats, monster_health, has_treasure):
    """Function to simulate a combat encounter."""
    print("A monster appears!")
    while monster_health > 0 and player_stats['health'] > 0:
        # Player attack
        monster_health -= player_stats['attack']
        print(f"You dealt {player_stats['attack']} damage. Monster's health is now {monster_health}.")

        if monster_health <= 0:
            print("You defeated the monster!")
            return has_treasure

        # Monster attack
        player_stats['health'] -= 10
        print(f"The monster attacks! You lost 10 health. Your health is now {player_stats['health']}.")

    if player_stats['health'] <= 0:
        print("You were defeated in combat!")
    return None

def handle_path_choice(player_stats):
    """Function to simulate player path choice and update stats."""
    print("\nChoose a path: 1. Combat, 2. Explore")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        print("You chose to fight!")
    elif choice == "2":
        print("You chose to explore!")
    return player_stats

def main():
    """Main game loop."""
    
    # Dungeon rooms with a new room: The Cryptic Library
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    # Random chance to discover an artifact
    if random.random() < 0.3:
        artifact_name = random.choice(list(artifacts.keys()))
        player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)

    # Enter dungeon and process rooms
    if player_stats['health'] > 0:
        player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)

    print("\n--- Game End ---")
    print(f"Final Health: {player_stats['health']}")
    print("Clues collected:")
    for clue in clues:
        print(f"- {clue}")

if __name__ == "__main__":
    main()
