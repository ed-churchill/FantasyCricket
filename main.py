import read_play_cricket
import write_google_sheets

test_links = ['https://uniofwarwick.play-cricket.com/website/results/4055612',
              'https://uniofwarwick.play-cricket.com/website/results/4052769']

# Test the script that updates the stats on the test_links
for link in test_links:
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, test_links.index(link) + 1)




