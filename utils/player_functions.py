import logging
import requests

import pandas as pd

from colorama import Fore, Style
from tqdm import tqdm


def get_player_data() -> pd.DataFrame:
    """
    Function to retrieve data from the fantasy football endpoint
    for a given player (using their ID). Returns a dataframe of
    their current and historical performance.

    Returns
    ---------

    pd.DataFrame :
        A dataframe containing data about players.
    """
    base_url = "https://fantasy.premierleague.com/api/"

    logging.info(f"✉️   Sending request off for current player/team data")

    current_players = get_current_players(base_url)

    logging.info(f"✅   Successfully pulled current player/team data")

    player_history = pd.DataFrame()

    for player_id in tqdm(range(1, 1_000)):
        tqdm.write(f"{Fore.YELLOW}✉️   Sending historical data requests for Player ID: {player_id}{Style.RESET_ALL}")
        returned_df = get_player_history(base_url, player_id)

        if returned_df is not None:
            player_history = pd.concat([player_history, returned_df], ignore_index=True)
            tqdm.write(f"{Fore.GREEN}✅   Successfully pulled current data for Player ID: {player_id}{Style.RESET_ALL}")
        else:
            tqdm.write(f"{Fore.RED}❌   Wasn't able to pull current data for Player ID: {player_id}{Style.RESET_ALL}")
    
    final_df = current_players.merge(player_history,
                                     left_on="id",
                                     right_on="element")

    return final_df


def get_current_players(base_url: str) -> pd.DataFrame:
    """
    Function to retrieve data about current players in the Premier
    League.

    Parameters
    ---------

    base_url : str
        The base url used to call out to the endpoint.

    Returns
    ---------

    pd.DataFrame :
        A dataframe of current player data, has the following
        structure:

        #TODO: Fill in structure of outputted dataframe
    """
    r = requests.get(base_url + "bootstrap-static/").json()
    players = pd.json_normalize(r["elements"])
    teams = pd.json_normalize(r["teams"])
    positions = pd.json_normalize(r["element_types"])
    df = pd.merge(
        left=players,
        right=teams,
        left_on="team",
        right_on="id"
    )

    df = df.merge(
        positions,
        left_on="element_type",
        right_on="id"
    )

    return df


def get_player_history(base_url: str, player_id: int) -> pd.DataFrame:
    """
    Function to get a player's historical data based on their ID

    Parameters
    ---------

    base_url : str
        The base url used to call out to the endpoint.

    Returns
    ---------

    pd.DataFrame :
        A pandas dataframe of the
    """
    r = requests.get(base_url + "element-summary/" + str(player_id) + "/")

    if r.status_code == 200:
        r = r.json()
        history_df = pd.json_normalize(r["history"])
        history_df["player_id"] = player_id
        return history_df
    else:
        return None

