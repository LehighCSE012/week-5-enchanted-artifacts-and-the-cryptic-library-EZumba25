import pytest
from adventure import enter_dungeon  # Assuming enter_dungeon is in adventure.py

def test_dungeon_rooms_is_list_of_tuples():
    dungeon_rooms = [
        ("Room 1", "item1", "none", None),
        ("Room 2", None, "puzzle", ("success", "fail", -5))
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    try:
        enter_dungeon(player_stats, inventory, dungeon_rooms, clues)
    except Exception as e:
        pytest.fail(f"enter_dungeon raised an exception with valid dungeon_rooms structure: {e}")

def test_dungeon_room_tuple_structure():
    dungeon_rooms_bad = [
        ("Room 1", "item1", "none"), # Missing challenge_outcome
        ("Room 2", None, "puzzle", "wrong_outcome_type") # outcome not tuple
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    with pytest.raises(TypeError) as excinfo: # Or potentially other errors depending on student's implementation
        enter_dungeon(player_stats, inventory, dungeon_rooms_bad, clues, artifacts)
    assert "tuple" in str(excinfo.value).lower() or "unpack" in str(excinfo.value).lower() # General error check, adjust as needed

def test_dungeon_rooms_challenge_types():
    dungeon_rooms_types = [
        ("Room none", None, "none", None),
        ("Room puzzle", None, "puzzle", ("success", "fail", -5)),
        ("Room trap", None, "trap", ("success", "fail", -5)),
        ("Room library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}
    try:
        enter_dungeon(player_stats, inventory, dungeon_rooms_types, clues)
    except Exception as e:
        pytest.fail(f"enter_dungeon failed to handle all challenge types: {e}")
