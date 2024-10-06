from typing import Union, Tuple

def calculate_elo(fighter_1_elo: Union[float, int], fighter_2_elo: Union[float, int], result: str, method: str, k_factor=200) -> Tuple[Union[float, int], Union[float, int]]:
    """
    Temporary ELO calculator...
    """
    k_factor = get_k_factor(method, k_factor, multiplier=1.15)
    expected_score_fighter_1 = expected_score(fighter_1_elo, fighter_2_elo)
    expected_score_fighter_2 = expected_score(fighter_2_elo, fighter_1_elo)
    if result == 'win':
        S_fighter_1 = 1
        S_fighter_2 = 0
    elif result == 'loss':
        S_fighter_1 = 0
        S_fighter_2 = 1
    elif result == 'draw':
        S_fighter_1 = 0.5
        S_fighter_2 = 0.5
    else:
        return fighter_1_elo, fighter_2_elo  # No change for no contest (nc)

    fighter_1_elo_new = fighter_1_elo + k_factor * (S_fighter_1 - expected_score_fighter_1)
    fighter_2_elo_new = fighter_2_elo + k_factor * (S_fighter_2 - expected_score_fighter_2)
    return fighter_1_elo_new, fighter_2_elo_new

def expected_score(current_elo: Union[float, int], opponent_elo: Union[float, int], denom=400) -> Union[float, int]:
    return 1 / (1 + 10**((opponent_elo - current_elo)/denom))

def get_k_factor(method: str, k: Union[float, str], multiplier: Union[float, int]):
    if method == 'KO/TKO' or method == 'SUB':
        return k * multiplier  # Increase K by 15% for KO or submission
    else:
        return k