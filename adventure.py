import random

def discover_artifact(player_stats, artifacts, artifact_name):
    """Function to discover an artifact and apply its effects."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You discovered: {artifact_name} - {artifact['description']}")
        
        # Apply the effect of the artifact
        if artifact['effect'] == 'increases health':
            player_stats['health'] += artifact['power']
            print(f"{artifact_name} increases your health by {artifact['power']}!")
        elif artifact['effect'] == 'enhances attack':
            player_stats['attack'] += artifact['power']
            print(f"{artifact_name} enhances your attack by {artifact['power']}!")
        elif artifact['effect'] == 'solves puzzles':
            print(f"{artifact_name} allows you to bypass puzzles!")

        # Remove the artifact from the dictionary
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

        # Return updated player stats, inventory, and clues
        return player_stats, inventory, clues

def display_player_status(player_stats):
    """Function to display the current player stats."""
    print(f"Player Health: {player_stats['health']}, Player Attack: {player_stats['attack']}")

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
