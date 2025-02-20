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

def discover_artifact(player_stats, artifacts, artifact_name):
    """Function to handle artifact discovery and applying its effects."""
    
    # Use keys() to check if the artifact_name exists in the artifacts dictionary
    if artifact_name in artifacts.keys():  # keys() gives us a list of all the keys (artifact names)
        artifact = artifacts[artifact_name]
        # Apply artifact effects and remove from dictionary
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"{artifact_name} increases your health by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"{artifact_name} enhances your attack by {artifact['power']}!")
        elif artifact['effect'] == "solves puzzles":
            print(f"{artifact_name} allows you to solve puzzles!")
        
        # Remove the artifact after it's discovered using `pop()`
        artifacts.pop(artifact_name)
    else:
        print("You found nothing of interest.")
    
    return player_stats, artifacts


def find_clue(clues, new_clue):
    """Function to find and add a new clue to the set."""
    
    # Check if the clue already exists in the set
    if new_clue in clues:
        print("You already know this clue.")
    else:
        # Add the new clue to the set and print the discovery message
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    
    return clues

import random

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Function to simulate entering the dungeon and encountering different rooms."""
    # Loop through all rooms
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room

        # Print the room description
        print(f"\nYou enter the {room_description}.")
        
        # Handle challenge logic based on the room's challenge type
        if challenge_type == "library":
            # Room-specific logic for the Cryptic Library
            print("A vast library filled with ancient, cryptic texts.")
            
            # Create a list of possible clues
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door.",
                "The path to victory lies through the old castle.",
                "Darkness follows the light."
            ]
            
            # Randomly select 2 clues from the list
            selected_clues = random.sample(possible_clues, 2)
            
            # Call find_clue to add the selected clues to the clues set
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            
            # Check if the player has the staff_of_wisdom to bypass a puzzle
            if "staff_of_wisdom" in inventory:
                print("You have the Staff of Wisdom! You can bypass a puzzle challenge in another room.")
                bypass_choice = input("Do you want to bypass a puzzle challenge? (yes/no): ")
                
                if bypass_choice.lower() == "yes":
                    # Allow the player to choose a room to bypass the puzzle challenge
                    print("You can bypass one of the following puzzle rooms:")
                    puzzle_rooms = [
                        "Dusty library", "Small room, locked chest"
                    ]
                    print("1. Dusty library\n2. Small room, locked chest")
                    bypass_room_choice = input("Enter the number of the room you wish to bypass: ")
                    
                    if bypass_room_choice == "1":
                        print("You bypass the Dusty library puzzle!")
                        player_stats['health'] += challenge_outcome[2]  # Modify health based on the puzzle outcome
                    elif bypass_room_choice == "2":
                        print("You bypass the Small room, locked chest puzzle!")
                        player_stats['health'] += challenge_outcome[2]  # Modify health based on the puzzle outcome
                    else:
                        print("Invalid choice, no room bypassed.")
            else:
                print("Without the Staff of Wisdom, you cannot bypass any puzzle challenges.")

        elif challenge_type == "puzzle":
            # Handle puzzle challenges (you already have this logic)
            print("You face a puzzle challenge!")
            if challenge_outcome:
                # Handle puzzle success or failure
                pass
        
        elif challenge_type == "trap":
            # Handle trap challenges (you already have this logic)
            print("You face a trap!")
            if challenge_outcome:
                # Handle trap success or failure
                pass
        
        elif challenge_type == "none":
            # No challenge in this room
            print("There is no challenge in this room.")
        
        # Continue to the next room (if applicable)
        print("Proceeding to the next room...\n")
    
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
    
    # Define the path options in a dictionary
    path_choices = {
        "1": "combat",  # Combat path
        "2": "explore",  # Explore path
    }
    
    # Prompt player for choice
    print("\nChoose a path: 1. Combat, 2. Explore")
    choice = input("Enter 1 or 2: ")

    # Get the corresponding path action
    action = path_choices.get(choice)

    if action == "combat":
        print("You chose to fight!")
        # You can insert your combat logic here
    elif action == "explore":
        print("You chose to explore!")
        # You can insert your exploration logic here
    else:
        print("Invalid choice. Please choose 1 or 2.")

    return player_stats

def main():
    """Main game loop."""
    
    # Dungeon rooms with a new room: The Cryptic Library
    dungeon_rooms = [
    ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
    ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
    ("Grand hall, shimmering pool", "healing potion", "none", None),
    ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
    ("Cryptic Library", None, "library", None)  # Adding the Cryptic Library room
]

    player_stats = handle_path_choice(player_stats)
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
