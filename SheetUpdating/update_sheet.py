import write_google_sheets, read_play_cricket

"""This file contains the function that will be used to update the Google Sheet"""

def update_sheets(scorecard_link, week_number):
    """Function that updates the spreadsheet corresponding to the parameter week_number with the stats from the link scorecard_link
    
    :param scorecard_link The link (as a string) to the PlayCricket scorecard that we will use to update the sheet
    :param week_number The week number corresponding to the sheet we want to update (e.g 5 would update the Week5 Sheet)"""

    # Get the batting, bowling and fielding data
    print(f"\nFetching data for the game {scorecard_link} from PlayCricket.com\n")
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(scorecard_link)
    print(f"'\nFinished collecting data for the game {scorecard_link} from PlayCricket\n")

    # Update the relevant sheet using the data
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, week_number)
    print(f"\nFinished updating the Week{week_number} sheet with data from {scorecard_link}\n")

if __name__ == "__main__":
    # Scorecard link (copy and paste it into the quotation marks)
    scorecard_link = ''

    # Week number to update (Change it to the week you want to update)
    week_number = 1

    # Update the sheet  
    update_sheets(scorecard_link, week_number)
   