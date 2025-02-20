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

def handle_puzzle(puzzle_data, choice=None):

    # Display the puzzle if choice=None (e.g., before the staff usage prompt)
    if choice is None:
        print(puzzle_data["question"])
        for i, option in enumerate(puzzle_data["options"], 1):
            print(f"{i}. {option}")
        return None, None  # Signal that no answer was processed

    # Input validation loop
    while True:
        user_input = input("Choose an option (enter number): ")

        try:
            choice = int(user_input) - 1  # Convert to 0-based index
            if 0 <= choice < len(puzzle_data["options"]):
                break  # Valid choice
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Determine success
    selected_option = puzzle_data["options"][choice]
    success = selected_option == puzzle_data["answer"]

    # Provide clearer success/failure messages
    if success:
        print(f" Correct! You solved the puzzle.")
    else:
        print(f" Incorrect. The correct answer was: {puzzle_data['answer']}")

    return success, None  # Returning a tuple to match expected structure



def enter_dungeon(player_stats, inventory, clues, dungeon_rooms, current_room_index):
    # Extract the current room's data from the tuple
    room_description, item, challenge_type, challenge_outcome = dungeon_rooms[current_room_index]
    
    print(f"You have entered: {room_description}")

    if challenge_type == "puzzle":
        puzzle, success_message, failure_message, health_penalty = challenge_outcome  

        # Display puzzle initially
        handle_puzzle(puzzle, choice=None)  

        while True:
            try:
                user_input = input("Enter the number of your choice: ").strip()
                
                # Allow staff usage
                if "staff_of_wisdom" in inventory:
                    use_staff = input("Use the Staff of Wisdom to bypass the puzzle? (yes/no): ").strip().lower()
                    if use_staff == "yes":
                        inventory.remove("staff_of_wisdom")  # Staff is now removed
                        print("You used the Staff of Wisdom to bypass the puzzle!")
                        print(success_message)  
                        return player_stats, inventory, clues  # Return updated values

                # Validate numeric input
                user_choice = int(user_input)

                # Process puzzle answer
                result = handle_puzzle(puzzle, user_choice)

                if result is True:
                    print(success_message)
                    return player_stats, inventory, clues  # Player succeeded
                elif result is False:
                    print(failure_message)
                    player_stats["health"] -= health_penalty  # Apply penalty
                    return player_stats, inventory, clues  # Player failed
                
            except ValueError:
                print("Invalid input. Please enter a number.")


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

            for new_clue in clues_found: # loop through the clues
                clues = find_clue(clues, new_clue) # use the provided function to add to the set
            library_visited = True
            clues_found = find_clue() #Get list of clues
        
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
    # Ensure challenge_outcome contains puzzle_data in the correct format
            puzzle_data, success_message, failure_message, health_penalty = challenge_outcome  
    
    # Call handle_puzzle correctly (ensure 'choice' is None initially)
    player_stats, success = handle_puzzle(puzzle_data, choice=None) 

    # Handle puzzle results based on success or failure
    if success:
        print(success_message)
    else:
        print(failure_message)
        player_stats["health"] = max(0, player_stats["health"] - health_penalty)


        # Prevent entering a room if health is 0
        if player_stats['health'] <= 0:
            print("You are too weak to continue.")
            break
        
        display_inventory(inventory)

    return player_stats, inventory, clues

def generate_clues():
    """Returns a list of possible clues to be discovered in the library."""
    return [
        "The dungeon was built atop an ancient ruin.",
        "A secret passage lies behind the great tapestry.",
        "The artifact of power is hidden in the dragon’s lair.",
        "Only those with true courage may wield the sacred blade.",
        "The cursed amulet drains the life of its wielder.",
        "A long-lost hero once sealed away an ancient evil here."
    ]

def find_clue(clues, new_clue):
    """Adds a new clue to the set of clues if it's not already present."""
    if new_clue not in clues: # use set operation 'in' for check
        clues.add(new_clue)      # use set operation 'add' to add the clue.
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues # return the updated clues set.


def check_for_treasure(inventory):
    """Checks if the player has obtained the treasure."""
    if "treasure" in inventory:
        print("You found the hidden treasure! You win!")
    else:
        print("No treasure found.")

# Main game loop
def main():
    """Main function to run the adventure game."""
    player_stats = {'health': 100, 'attack': 5, 'staff_used': False}
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
        
        # Combat encounter
        treasure_obtained_in_combat, player_stats = combat_encounter(player_stats, monster_health, has_treasure)
        display_player_status(player_stats)  # Display updated stats after combat
        
        if treasure_obtained_in_combat:
            inventory = acquire_item(inventory, "treasure")
        
        # Artifact discovery logic
        if random.random() < 0.3:  # 30% chance to discover an artifact
            artifact_name = random.choice(list(artifacts.keys()))
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)  # Display updated stats after artifact discovery

        # Enter dungeon
        player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
        
        # Check if the player has obtained the treasure
        check_for_treasure(inventory)

# Run the game
if __name__ == "__main__":
    main()
