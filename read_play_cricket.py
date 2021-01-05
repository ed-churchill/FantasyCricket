"""Module containing functions that will allow a scorecard to be read from PlayCricket and use this information to
update a spreadsheet accordingly"""

import pandas as pd

def scorecard_to_df(scorecard_url):
    """Function that reads a scorecard from PlayCricket.com and converts it to a Pandas dataframe

    :param str scorecard_url: The URL of the scorecard on PlayCricket.com
    """

    # Find the first batting scorecard
    data = pd.read_html(scorecard_url)




