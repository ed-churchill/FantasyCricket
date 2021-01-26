import read_play_cricket
import write_google_sheets

test_link = 'https://uniofwarwick.play-cricket.com/website/results/4055612'


bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(test_link)
write_google_sheets.update_stats(bat_df, bowl_df, field_df, 1)




