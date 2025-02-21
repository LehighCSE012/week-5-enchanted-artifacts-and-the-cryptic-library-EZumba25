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
    """Display the current health and attack of the player."""
    print(f"Health: {player_stats['health']} | Attack: {player_stats['attack']}")

def combat_encounter(player_stats, monster_health, has_treasure):
    """Simulate combat encounter."""
    print("A monster appears!")
    # Example combat logic using monster_health
    while monster_health > 0 and player_stats['health'] > 0:
        # Simulate player attack
        damage_dealt = player_stats['attack']
        monster_health -= damage_dealt
        print(f"You attack the monster and deal {damage_dealt} damage. Monster health: {monster_health}")

        # If the monster is still alive, it attacks back
        if monster_health > 0:
            damage_taken = 10  # Assume the monster does a fixed amount of damage
            player_stats['health'] -= damage_taken
            print(f"The monster attacks you and deals {damage_taken} damage. Your health: {player_stats['health']}")

    # Check the outcome of the battle
    if player_stats['health'] > 0:
        print("You defeated the monster!")
        if has_treasure:
            print("You found treasure!")
        return 'treasure'
    else:
        print("You were defeated!")
        return None

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover an artifact and update player stats."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found the {artifact_name}: {artifact['description']}")
        
        # Apply the artifact effect
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        elif artifact['effect'] == "solves puzzles":
            print("You can bypass certain puzzles now.")
        
        # Remove the artifact from the dictionary
        del artifacts[artifact_name]
        
        print(f"The artifact's effect: {artifact['effect']}")
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Add a new clue to the set."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """Handles the player's experience when entering a dungeon room."""

    for room in dungeon_rooms:
        # Ensure room tuple has exactly 4 elements
        if len(room) != 4:
            raise TypeError(f"Incorrect number of values in room tuple: {room}")

        # Unpack room tuple
        room_description, item, challenge_type, challenge_outcome = room

        # Ensure challenge_outcome is a tuple if required
        if challenge_type.lower() not in ["none", "library"] and not isinstance(challenge_outcome, tuple):
            raise TypeError("Challenge outcome must be a tuple for challenge types other than 'none' or 'library'.")

        # Normal room processing...
        print(f"\nEntering: {room_description}")
        if item:
            print(f"You found an item: {item}")
            inventory.append(item)

        if challenge_type.lower() not in ["none", "library"]:
            success_message, failure_message, health_penalty = challenge_outcome
            print(f"You face a {challenge_type} challenge!")

            # Example challenge logic (random success/failure)
            outcome = random.choice([True, False])
            if outcome:
                print(success_message)
            else:
                print(failure_message)
                player_stats['health'] -= health_penalty

    return player_stats, inventory, clues

def main():
    """Main game loop."""
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
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    has_treasure = random.choice([True, False])

    display_player_status(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            print("You have treasure!")
        
        # Check for artifacts after combat
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        # Enter a dungeon and possibly enter the Cryptic Library
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)

    # Game end display
    print("\n--- Game End ---")
    display_player_status(player_stats)
    print("Final Inventory:", inventory)
    print("Clues:")
    if clues:
        for clue in clues:
            print(f"- {clue}")
    else:
        print("No clues.")

if __name__ == "__main__":
    main()
