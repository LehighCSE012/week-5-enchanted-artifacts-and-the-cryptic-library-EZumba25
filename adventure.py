import random

def discover_artifact(player_stats, artifacts, artifact_name):
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found {artifact_name}: {artifact['description']}")

        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']

        print(f"Effect: {artifact['effect']} (+{artifact['power']})")
        del artifacts[artifact_name]  # Remove artifact after discovery
    else:
        print("You found nothing of interest.")

    return player_stats, artifacts

def find_clue(clues, new_clue):
    if new_clue in clues:  # Using 'in' operator to check if the clue exists
        print("You already know this clue.")
    else:
        clues.add(new_clue)  # Using add() method to add unique clues
        print(f"You discovered a new clue: {new_clue}")
    return clues

def acquire_item(inventory, item):
    """Adds an item to the player's inventory if it's not None."""
    if item:
        inventory.append(item)
        print(f"You acquired: {item}")
    return inventory

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    for room in dungeon_rooms:
        name, item, challenge_type, challenge_outcome = room
        print(f"You entered: {name}")  # Use `name` (already used)
        if item:
            print(f"You found an item: {item}")  # Now using `item`
        if challenge_type:
            print(f"A {challenge_type} challenge awaits!")  # Now using `challenge_type`

        if name == "Cryptic Library":
            print("A vast library filled with ancient, cryptic texts.")
            clue_pool = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            found_clues = random.sample(clue_pool, 2)
            for clue in found_clues:
                clues = find_clue(clues, clue)
            
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you understand the meaning of the clues.")
                print("You can bypass a puzzle challenge of your choice.")
    
    return player_stats, inventory, clues

def display_player_status(player_stats):
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def main():
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {"description": "Glowing amulet, life force.", "power": 15, "effect": "increases health"},
        "ring_of_strength": {"description": "Powerful ring, attack boost.", "power": 10, "effect": "enhances attack"},
        "staff_of_wisdom": {"description": "Staff of wisdom, ancient.", "power": 5, "effect": "solves puzzles"}
    }
    
    display_player_status(player_stats)
    
    if random.random() < 0.3:  # 30% chance of finding an artifact
        artifact_keys = list(artifacts.keys())
        if artifact_keys:
            artifact_name = random.choice(artifact_keys)
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)
    
    player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
    
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
