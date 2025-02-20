import random

# Function to display player stats (health and attack)
def display_player_status(player_stats):
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

# Function to discover an artifact
def discover_artifact(player_stats, artifacts, artifact_name):
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found: {artifact_name} - {artifact['description']}")
        
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']} points!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increased by {artifact['power']} points!")

        del artifacts[artifact_name]  # Remove artifact after it's been discovered
    else:
        print("You found nothing of interest.")
    
    return player_stats, artifacts

# Function to find a new clue
def find_clue(clues, new_clue):
    if new_clue in clues:  # Check if clue already found
        print("You already know this clue.")
    else:
        clues.add(new_clue)  # Add new clue
        print(f"You discovered a new clue: {new_clue}")
    return clues

# Combat encounter function
def combat_encounter(player_stats, monster_health, has_treasure):
    while player_stats['health'] > 0 and monster_health > 0:
        print("You attack the monster!")
        monster_health -= player_stats['attack']
        if monster_health <= 0:
            print("You defeated the monster!")
            return has_treasure
        print("The monster attacks!")
        player_stats['health'] -= 10
        if player_stats['health'] <= 0:
            print("You have been defeated!")
            return None

# Function to handle entering the dungeon and exploring rooms
def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts=None):
    for room in dungeon_rooms:
        room_name, item, challenge_type, challenge_outcome = room
        print(f"\nYou enter the {room_name}.")  # Match expected test string exactly

        if room_name == "The Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            clue_options = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(clue_options, 2)  # Randomly pick two clues
            
            for clue in selected_clues:
                clues = find_clue(clues, clue)  # Ensure clues are updated

            if "staff_of_wisdom" in inventory:
                print("The Staff of Wisdom hums in your hand, allowing you to decipher the texts effortlessly.")
                # Example of bypassing a puzzle challenge:
                print("You bypass the puzzle challenge with your knowledge.")

    return player_stats['health'], inventory, clues

# Main game loop
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
        "amulet_of_vitality": {"description": "A glowing amulet that enhances your life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "A powerful ring that boosts your attack damage.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "A staff imbued with ancient wisdom.", "power": 5, "effect": "solves puzzles"}
    }

    has_treasure = random.choice([True, False])
    
    # Display player's initial stats
    display_player_status(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat:
            print("You obtained treasure from the monster.")
            inventory.append("treasure")

        if random.random() < 0.3 and artifacts:  # 30% chance to find an artifact
            artifact_name = random.choice(list(artifacts.keys()))
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)

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
