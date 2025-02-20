import random

# Inventory System
def acquire_item(inventory, item):
    """Appends the item to the inventory list and notifies the player."""
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Displays the player's current inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for idx, item in enumerate(inventory, 1):
            print(f"{idx}. {item}")

def player_attack(player_stats, monster_health):
    """Simulates the player's attack on the monster."""
    print("You strike the monster for 15 damage!")
    monster_health = max(monster_health - 15, 0)
    return monster_health

def monster_attack(player_stats):
    """Simulates the monster's attack on the player."""
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        player_stats['health'] = max(player_stats['health'] - 20, 0)
    else:
        print("The monster hits you for 10 damage!")
        player_stats['health'] = max(player_stats['health'] - 10, 0)
    return player_stats

def handle_puzzle(player_stats, challenge_outcome):
    """Handles puzzle challenges in the dungeon."""
    print("You encounter a puzzle!")
    choice = input("Do you want to 'solve' or 'skip' the puzzle? ").strip().lower()
    if choice == "solve":
        success = random.choice([True, False])
        success_message, failure_message, health_change = challenge_outcome
        if success:
            print(success_message)
        else:
            print(failure_message)
        player_stats['health'] = max(player_stats['health'] + health_change, 0)
    else:
        print("You chose to skip the puzzle.")
    return player_stats

def handle_trap(player_stats, challenge_outcome):
    """Handles trap challenge logic."""
    print("You see a potential trap!")
    choice = input("Do you want to 'disarm' or 'bypass' the trap? ").strip().lower()
    if choice == "disarm":
        success = random.choice([True, False])
        success_message, failure_message, health_change = challenge_outcome
        if success:
            print(success_message)
        else:
            print(failure_message)
            player_stats['health'] = max(player_stats['health'] + health_change, 0)
    else:
        print("You chose to bypass the trap.")
    return player_stats

def handle_path_choice(player_stats):
    """Randomly determines the player's path and adjusts health accordingly."""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats['health'] = min(player_stats['health'] + 10, 100)
    else:
        print("You fall into a pit and lose 15 health points.")
        player_stats['health'] = max(player_stats['health'] - 15, 0)
        if player_stats['health'] == 0:
            print("You are barely alive!")
    return player_stats

# Function to display player stats (health and attack)
def display_player_status(player_stats):
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

# Function to discover an artifact
def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles the discovery of an artifact and applies its effects on the player."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You discovered the {artifact_name}: {artifact['description']}")
        
        # Apply the effect based on the artifact's effect type
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increased by {artifact['power']}!")
        elif artifact['effect'] == "solves puzzles" and artifact_name == "staff_of_wisdom":
            print("You now have the knowledge to bypass puzzles in the dungeon!")
        
        # Remove the artifact after it's used
        del artifacts[artifact_name]
    
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts


# Function to find a new clue
def find_clue():
    """Simulates finding a clue in the library."""
    clues_available = [
        "The key to the vault lies in the Eastern room.",
        "Only the bravest may face the beast in the dark hall.",
        "The puzzle of the moon can only be solved with light.",
        "The hidden treasure is guarded by fire and water."
    ]
    # Randomly choose a clue
    return random.choice(clues_available)

# Combat encounter function
def combat_encounter(player_stats, monster_health, has_treasure):
    """Handles the combat encounter between the player and the monster."""
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = player_attack(player_stats, monster_health)
        display_player_status(player_stats)
        if monster_health > 0:
            player_stats = monster_attack(player_stats)

    if player_stats['health'] == 0:
        print("Game Over!")
        return False, player_stats
    print("You defeated the monster!")
    return has_treasure, player_stats


# Function to handle entering the dungeon and exploring rooms
def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles entering a dungeon room, applying challenges and item acquisitions."""
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room
        print(f"\n{room_description}")

        if item:
            print(f"You found a {item} in the room.")
            inventory = acquire_item(inventory, item)

        # Check if the room is a library and the player discovers a clue
        if challenge_type == "library":
            print("You step into the Cryptic Library!")
            clue = find_clue()
            clues.add(clue)  # Add the clue to the clues set
            print(f"You discovered a clue: {clue}")
        
        # Check if the player has the staff_of_wisdom and can bypass a puzzle
        if "staff_of_wisdom" in inventory and challenge_type == "puzzle":
            bypass = input("Do you want to bypass this puzzle using your knowledge? (yes/no) ").strip().lower()
            if bypass == "yes":
                print("You use the Staff of Wisdom to bypass the puzzle!")
                continue  # Skip the puzzle and proceed with the next room

        # Handle different challenges based on the room's challenge type
        if challenge_type == "puzzle":
            player_stats = handle_puzzle(player_stats, challenge_outcome)
        elif challenge_type == "trap":
            player_stats = handle_trap(player_stats, challenge_outcome)
        elif challenge_type == "library":
            # The library challenge doesn't affect health, so no health change here
            pass

        # Prevent entering a room if health is 0
        if player_stats['health'] <= 0:
            print("You are too weak to continue.")
            break
        
        display_inventory(inventory)

    return player_stats, inventory, clues


def check_for_treasure(inventory):
    """Checks if the player has obtained the treasure."""
    if "treasure" in inventory:
        print("You found the hidden treasure! You win!")
    else:
        print("No treasure found.")

# Main game loop
def main():
    """Main function to run the adventure game."""
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()

    # Define artifacts
    artifacts = {
        "staff_of_wisdom": {"description": "A staff that grants the knowledge to bypass puzzles.", "effect": "solves puzzles", "power": 0},
        "healing_ring": {"description": "A magical ring that heals you.", "effect": "increases health", "power": 20},
        "warrior_belt": {"description": "A belt that enhances your combat skills.", "effect": "enhances attack", "power": 5}
    }

    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    has_treasure = random.choice([True, False])
    
    # Display player's initial stats
    display_player_status(player_stats)

    if player_stats['health'] > 0:
        player_stats = handle_path_choice(player_stats)
        
        treasure_obtained_in_combat, player_stats = combat_encounter(player_stats, monster_health, has_treasure)
        
        if treasure_obtained_in_combat:
            inventory = acquire_item(inventory, "treasure")
        
        player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
        check_for_treasure(inventory)

if __name__ == "__main__":
    main()
