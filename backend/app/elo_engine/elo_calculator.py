def calculate_elo(winner_elo, loser_elo, result):
    """
    Temporary ELO calculator...
    """
    if result == 'win':
        return winner_elo + 10, loser_elo - 10
    elif result == 'loss':
        return loser_elo + 10, winner_elo - 10
    elif result == 'draw':
        return winner_elo, loser_elo  # No change for draw
    else:
        return winner_elo, loser_elo  # No change for no contest
