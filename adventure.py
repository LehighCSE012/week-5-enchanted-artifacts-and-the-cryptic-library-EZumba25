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

def display_player_status(player_stats):
    """Displays player health and attack."""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def display_inventory(inventory):
    """Displays player inventory."""
    if inventory:
        for item in inventory:
            print(f"- {item}")
    else:
        print("Inventory is empty.")

def handle_path_choice(player_stats):
    """Handles player path choice."""
    print("\nYou come to a fork in the path.")
    print("1. Take the left path.")
    print("2. Take the right path.")

    while True:
        choice = input("Which path will you take? (1 or 2): ")
        if choice in ('1', '2'):
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        print("You bravely venture down the left path.")
        player_stats['health'] -= 5
        print("You lost 5 health.")
    elif choice == '2':
        print("You cautiously choose the right path.")
        player_stats['health'] += 10
        print("You gained 10 health.")

    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """Simulates combat."""
    print("\nA wild monster appears!")

    while player_stats['health'] > 0 and monster_health > 0:
        player_attack = player_stats['attack']
        monster_attack_damage = random.randint(5, 15)

        monster_health -= player_attack
        print(f"You attack the monster for {player_attack} damage.")

        if monster_health <= 0:
            print("You defeated the monster!")
            if has_treasure:
                treasure = random.choice(["gold", "potion", "sword"])
                print(f"You found a {treasure}!")
                return treasure
            return None

        player_stats['health'] -= monster_attack_damage
        print(f"The monster attacks you for {monster_attack_damage} damage.")

        if player_stats['health'] <= 0:
            print("You have been defeated!")
            return None

    return None

def check_for_treasure(treasure):
    """Checks for treasure."""
    if treasure:
        print(f"Congratulations! You found a {treasure}!")
    else:
        print("No treasure was found.")

def find_clue(clues, new_clue):
    """Adds a clue to the set."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles artifact discovery."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(artifact["description"])

        if artifact["effect"] == "increases health":
            player_stats['health'] += artifact["power"]
            print(f"Your health increased by {artifact['power']}.")
        elif artifact["effect"] == "enhances attack":
            player_stats['attack'] += artifact["power"]
            print(f"Your attack increased by {artifact['power']}.")
        elif artifact["effect"] == "solves puzzles":
            print("This artifact helps you solve puzzles.")

        del artifacts[artifact_name]  # Remove from dictionary after discovery
    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Enters the dungeon and handles room logic."""

    for room_description, item, challenge_type, challenge_outcome in dungeon_rooms[:]: # Iterate over a copy
        print(f"\nYou enter a {room_description}.")

        if challenge_type == "library":
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door.",
                "The whispers of the wind hold the answer."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)

            if "staff_of_wisdom" in artifacts:
                print("The staff of wisdom helps you understand the clues.")
                player_stats['health'] += 10
                print("You bypass the puzzle in the Dusty Library and gain 10 health.")

                # Remove the Dusty Library
                for i, room in enumerate(dungeon_rooms):
                    if room[0] == "Dusty library":
                        del dungeon_rooms[i]
                        break

                print("The Dusty Library is no longer accessible.")

        elif challenge_type == "puzzle":
            if challenge_outcome:
                success_message, failure_message, health_change = challenge_outcome
                if random.random() < 0.5:
                    print(success_message)
                    if item:
                        inventory.append(item)
                        print(f"You found a {item}!")
                else:
                    print(failure_message)
                    player_stats['health'] += health_change
                    print(f"You lost {abs(health_change)} health.")
        elif challenge_type == "trap":
            if challenge_outcome:
                success_message, failure_message, health_change = challenge_outcome
                if random.random() < 0.5:
                    print(success_message)
                else:
                    print(failure_message)
                    player_stats['health'] += health_change
                    print(f"You lost {abs(health_change)} health.")
        elif challenge_type == "none":
            if item:
                inventory.append(item)
                print(f"You found a {item}!")

        display_player_status(player_stats)
        if player_stats['health'] <= 0:
            print("Your adventure ends here...")
            return player_stats, inventory, clues

    return player_stats, inventory, clues


def main():
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
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }
    has_treasure = random.choice([True, False])

    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")

if __name__ == "__main__":
    main()