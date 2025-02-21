import random

import random

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

def player_attack(monster_health, player_attack_power):
    """Simulates the player's attack on the monster."""
    damage = player_attack_power
    print(f"You strike the monster for {damage} damage!")
    return max(monster_health - damage, 0)

def monster_attack(player_health):
    """Simulates the monster's attack on the player."""
    if random.random() < 0.5:
        damage = 20  # Critical hit damage
        print("The monster lands a critical hit for 20 damage!")
    else:
        damage = 10  # Regular hit damage
        print("The monster hits you for 10 damage!")
    return max(player_health - damage, 0)

def display_player_status(player_stats):
    """Function to display the player's stats."""
    print("\nPlayer Stats:")
    for stat, value in player_stats.items():
        print(f"{stat}: {value}")

def discover_artifact(player_stats, artifacts, artifact_name):
    """Function to handle artifact discovery and applying its effects."""
    artifact = artifacts.get(artifact_name)

    if artifact:
        # Apply artifact effects
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"{artifact_name} increases your health by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"{artifact_name} enhances your attack by {artifact['power']}!")
        elif artifact['effect'] == "solves puzzles":
            print(f"{artifact_name} allows you to solve puzzles!")

        # Remove the artifact after it's discovered
        if artifact_name in artifacts:
            del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Function to handle clue discovery."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Function to simulate entering the dungeon and encountering different rooms."""
    for room in dungeon_rooms[:]:  # Iterate over a copy to safely remove items
        room_description, item, challenge_type, challenge_outcome = room

        print(f"\nYou enter the {room_description}.")

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
            if "staff_of_wisdom" in artifacts:  # Check in artifacts, not inventory
                print("You have the Staff of Wisdom! You can bypass a puzzle challenge in another room.")
                while True: # Input validation loop
                    bypass_choice = input("Do you want to bypass a puzzle challenge? (yes/no): ")
                    if bypass_choice.lower() in ('yes', 'no'):
                        break
                    print("Invalid input. Please enter 'yes' or 'no'.")

                if bypass_choice.lower() == "yes":
                    # Allow the player to choose a room to bypass the puzzle challenge
                    print("You can bypass one of the following puzzle rooms:")
                    puzzle_rooms = [room[0] for room in dungeon_rooms if room[2] == "puzzle"] # List of puzzle rooms
                    if puzzle_rooms: #check if there any puzzle room to skip
                        for i, room in enumerate(puzzle_rooms):  # Print room options with index
                            print(f"{i + 1}. {room}")
                        while True:  # Input validation loop
                            try:
                                bypass_room_choice = int(input("Enter the number of the room you wish to bypass: "))
                                if 1 <= bypass_room_choice <= len(puzzle_rooms):
                                    break
                                else:
                                    print("Invalid choice. Please enter a number from the list.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")

                        chosen_room = puzzle_rooms[bypass_room_choice - 1]  # Get the chosen room name
                        print(f"You bypass the {chosen_room} puzzle!")

                        # Find and update the corresponding room in dungeon_rooms
                        for i, room in enumerate(dungeon_rooms):
                            if room[0] == chosen_room:
                                if room[3]: # Check if challenge_outcome exists
                                    player_stats['health'] += room[3][2]  # Get health change from room data
                                del dungeon_rooms[i]  # Remove the room from the list
                                break
                    else:
                        print("You chose not to bypass a puzzle.")
                else:
                    print("Without the Staff of Wisdom, you cannot bypass any puzzle challenges.")

        elif challenge_type == "puzzle":
            # Handle puzzle challenges
            print("You face a puzzle challenge!")
            if challenge_outcome:
                success_message, failure_message, health_change = challenge_outcome
                if random.random() < 0.5:
                    print(success_message)
                    if item:
                        inventory = acquire_item(inventory, item)
                else:
                    print(failure_message)
                    player_stats['health'] += health_change
                    print(f"You lost {abs(health_change)} health.")

        elif challenge_type == "trap":
            # Handle trap challenges
            print("You face a trap!")
            if challenge_outcome:
                success_message, failure_message, health_change = challenge_outcome
                if random.random() < 0.5:
                    print(success_message)
                else:
                    print(failure_message)
                    player_stats['health'] += health_change
                    print(f"You lost {abs(health_change)} health.")

        elif challenge_type == "none":
            # No challenge in this room
            print("There is no challenge in this room.")
            if item:
                inventory = acquire_item(inventory, item)

        display_player_status(player_stats)  # Display status after each room
        if player_stats['health'] <= 0:
            print("Your adventure ends here...")
            return player_stats, inventory, clues

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
        monster_health = player_attack(monster_health, player_stats['attack'])  # Use player
    print(f"You dealt {player_stats['attack']} damage. Monster's health is now {monster_health}.")


    if monster_health <= 0:
           print("You defeated the monster!")
           return has_treasure

       # Monster attack
    player_stats['health'] -= 10
    print(f"The monster attacks! You lost 10 health. Your health is now {player_stats['health']}.")

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