"""Module containing functions that will allow a scorecard to be read from PlayCricket and use this information to
update a spreadsheet accordingly"""

import pandas as pd

def batting_to_df(match_url):
    """Function that reads the batting scorecard from PlayCricket.com and converts it to a Pandas dataframe

    :param str match_url: The URL of the scorecard on PlayCricket.com
    """

    # Fetch all the tables on the page
    tables = pd.read_html(match_url)

    

print(scorecard_to_df("https://uniofwarwick.play-cricket.com/website/results/4055612"))



