def parse_turn(line):
    turn = line.strip(">").split(" ")

    if turn[2] == "-":
        turn.insert(2, "")
        turn.insert(6, "Pass")
    elif turn[2].startswith("-"):
        turn.insert(2, "")
        turn.insert(6, "Exchange")
    elif turn[2] == "(time)":
        turn.insert(2, "")
        turn.insert(6, "Timeout")
    elif turn[2].startswith("("):
        turn.insert(2, "")
        turn.insert(6, "Six-Zero Rule")
    elif turn[1].startswith("("):
        turn.insert(1, "")
        turn.insert(2, "")
        turn.insert(6, "End")
    else:
        turn.insert(6, "Play")
    return turn
