import read_play_cricket
import write_google_sheets


week2_links = ['https://uniofwarwick.play-cricket.com/website/results/4052769',
               'https://uniofwarwick.play-cricket.com/website/results/4052768']
week3_links = ['https://uniofwarwick.play-cricket.com/website/results/4026201',
               'https://uniofwarwick.play-cricket.com/website/results/4026195']

for link in week2_links:
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 2)
for link in week3_links:
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 3)




