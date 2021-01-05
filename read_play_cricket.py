"""Module containing functions that will allow a scorecard to be read from PlayCricket and use this information to
update a spreadsheet accordingly"""

import pandas as pd
import bs4 as bs
import requests


def scorecard_to_df(scorecard_url):
    """Function that reads a scorecard from PlayCricket.com and converts it to a Pandas dataframe

    :param str scorecard_url: The URL of the scorecard on PlayCricket.com
    """

    response = requests.get("https://uniofwarwick.play-cricket.com/website/results/4055612")
    soup = bs.BeautifulSoup(response.text)
    table = soup.find('table')
    print(table)



