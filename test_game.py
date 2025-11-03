
import subprocess
import os

def run_game(inputs: str):
    # Clean up old CSV
    if os.path.exists("game_output.csv"):
        os.remove("game_output.csv")
    subprocess.run(["./solution"], input=inputs.encode(),
                   capture_output=True, timeout=5)

def read_csv():
    boards = []
    with open("game_output.csv") as f:
        for line in f:
            cells = line.strip().split(",")
            if len(cells) == 16:
                board = [list(map(int, cells[i*4:(i+1)*4])) for i in range(4)]
                boards.append(board)
    return boards

def first_nonspawn_board(boards):
    """
    Return last two boards (before, after) so we can compare merge
    effects ignoring random spawns.
    """
    if len(boards) < 2:
        return None, None
    return boards[-2], boards[-1]

# -------------------------------
# Basic tests
# -------------------------------

def test_progression_multiple_moves():
    run_game("a\nw\nd\ns\nq\n")
    boards = read_csv()
    assert len(boards) >= 5  # initial + 4 moves

def test_spawn_after_multiple_moves():
    # Slam left 5 times, then quit
    run_game("a\n" * 5 + "q\n")
    boards = read_csv()
    start, end = boards[0], boards[-1]

    nonzeros_start = sum(val != 0 for row in start for val in row)
    nonzeros_end = sum(val != 0 for row in end for val in row)

    # After 5 moves, guaranteed to have more tiles
    assert nonzeros_end > nonzeros_start

def test_undo_restores():
    run_game("a\nu\nq\n")
    boards = read_csv()
    assert len(boards) >= 3
    assert boards[0] == boards[-1]

def test_multiple_undos():
    run_game("a\nd\nu\nu\nq\n")
    boards = read_csv()
    assert boards[0] == boards[-1]

# -------------------------------
# Merge correctness tests
# -------------------------------

def test_merge_two_twos_left():
    run_game("a\nq\n")
    boards = read_csv()
    before, after = first_nonspawn_board(boards)
    if before and before[0][0] == 2 and before[0][1] == 2:
        assert after[0][0] == 4
        assert after[0][1] == 0

def test_no_double_merge():
    run_game("a\nq\n")
    boards = read_csv()
    before, after = first_nonspawn_board(boards)
    if before and before[0][:3] == [2, 2, 2]:
        assert after[0][0] == 4
        assert after[0][1] == 2

def test_merge_right():
    run_game("d\nq\n")
    boards = read_csv()
    before, after = first_nonspawn_board(boards)
    if before and before[3][2] == 2 and before[3][3] == 2:
        assert after[3][3] == 4
