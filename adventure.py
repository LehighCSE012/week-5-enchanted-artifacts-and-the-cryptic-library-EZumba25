import random

# Function to acquire an item and add to inventory
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
    artifact = artifacts.get(artifact_name, None)  # Using get() for safe access
    if artifact:
        print(f"You discovered the {artifact_name}: {artifact.get('description', 'No description available.')}")
        
        # Apply the effect based on the artifact's effect type
        effect_type = artifact.get('effect', 'none')
        power = artifact.get('power', 0)  # Get the power of the artifact

        if effect_type == "increases health":
            player_stats['health'] += power
            print(f"Your health increased by {power}!")
        elif effect_type == "enhances attack":
            player_stats['attack'] += power
            print(f"Your attack increased by {power}!")
        elif effect_type == "solves puzzles" and artifact_name == "staff_of_wisdom":
            print("You now have the knowledge to bypass puzzles in the dungeon!")
            player_stats.update({'staff_used': False})  # Using update() to mark staff as used
        
        # Remove the artifact after it's used
        del artifacts[artifact_name]
    
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

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
    library_visited = False  # Track if the library room is visited
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
            library_visited = True  # Mark that the library has been visited
        
        # Check if the player has the staff_of_wisdom and can bypass a puzzle
        if "staff_of_wisdom" in inventory and challenge_type == "puzzle" and library_visited and len(clues) > 0:
            if not player_stats.get('staff_used', False):
                print("You use the Staff of Wisdom to bypass the puzzle!")
                success_message, failure_message, health_change = challenge_outcome
                print(success_message)
                player_stats['health'] = max(player_stats['health'] + health_change, 0)
                player_stats['staff_used'] = True  # Mark the staff as used
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

def find_clue():
    """Simulates finding clues in the library."""
    clues_available = [
        "The key to the vault lies in the Eastern room.",
        "Only the bravest may face the beast in the dark hall.",
        "The puzzle of the moon can only be solved with light.",
        "The hidden treasure is guarded by fire and water."
    ]
    return random.sample(clues_available, 2)  # Select two unique clues randomly

def check_for_treasure(inventory):
    """Checks if the player has obtained the treasure."""
    if "treasure" in inventory:
        print("You found the hidden treasure! You win!")
    else:
        print("No treasure found.")

# Main game loop
def main():
    # Initialize player stats and clues
    player_stats = {
        "health": 100,
        "attack": 10,
        "inventory": [],
        "staff_used": False,
    }
    clues = set()
    library_visited = False
    artifacts = {
        "staff_of_wisdom": {"description": "Allows bypassing a puzzle in the future."},
        "amulet_of_strength": {"description": "Increases attack by 5."},
        # Add more artifacts as needed
    }

    # List of rooms in the dungeon, each room can have a specific challenge or event
    dungeon_rooms = ["entrance", "puzzle_room", "combat_room", "treasure_room", "boss_room"]

    # Iterate through the dungeon rooms
    for room in dungeon_rooms:
        print(f"\nEntering the {room}...")
        # Call enter_dungeon for each room
        player_stats, clues = enter_dungeon(player_stats, clues, library_visited)

        # Handle artifact discovery only after the dungeon exploration ends
        player_stats, artifacts = discover_artifact(player_stats, artifacts)

        # Display player status after each room
        display_player_status(player_stats)

    # Final status after all rooms are explored
    print("\nDungeon exploration complete!")
    display_player_status(player_stats)


# Function for entering the dungeon rooms and handling challenges
def enter_dungeon(player_stats, clues, library_visited):
    """
    Handles the dungeon exploration logic.
    Args:
    - player_stats: A dictionary with player's health, attack, etc.
    - clues: A set of clues the player has found
    - library_visited: A boolean indicating whether the player has visited the library.

    Returns:
    - Updated player_stats and clues.
    """
    # Here you can add logic to handle different room types (e.g., combat, puzzles, etc.)
    challenge_type = "puzzle"  # Example: For now, assume every room has a puzzle.
    
    if "staff_of_wisdom" in player_stats.get("inventory", []):
        if library_visited and len(clues) > 0:
            # Bypass the puzzle using the staff_of_wisdom and clues
            print("You used the Staff of Wisdom to bypass the puzzle!")
            player_stats["health"] -= 5  # Example health decrease for bypassing a challenge
        else:
            print("You need clues from the library to bypass the puzzle.")
    
    # After finishing the room, return the updated player stats and clues
    return player_stats, clues


# Function for discovering artifacts
def discover_artifact(player_stats, artifacts):
    """
    Randomly determines if an artifact is discovered and applies its effects.
    Args:
    - player_stats: A dictionary of the player's stats.
    - artifacts: A dictionary of available artifacts and their effects.

    Returns:
    - Updated player_stats and artifacts.
    """
    if random.random() < 0.3:  # 30% chance to find an artifact
        artifact_name = random.choice(list(artifacts.keys()))  # Randomly choose an artifact
        artifact = artifacts[artifact_name]

        print(f"Congratulations! You found the {artifact_name}. {artifact['description']}")

        # Apply the artifact's effects
        if artifact_name == "staff_of_wisdom":
            if player_stats.get('staff_used', False) == False:
                print("You now have the Staff of Wisdom!")
                player_stats["inventory"].append("staff_of_wisdom")
                player_stats["staff_used"] = False  # Mark as not used yet
            else:
                print("You've already used the Staff of Wisdom, it cannot be used again.")
        
        # Return updated player stats
        return player_stats, artifacts
    else:
        print("No artifact was found this time.")
        return player_stats, artifacts


# Function to display player status
def display_player_status(player_stats):
    print(f"Health: {player_stats['health']}")
    print(f"Attack: {player_stats['attack']}")
    print(f"Inventory: {player_stats['inventory']}")
    print(f"Staff Used: {player_stats['staff_used']}")


# Run the game
if __name__ == "__main__":
    main()

