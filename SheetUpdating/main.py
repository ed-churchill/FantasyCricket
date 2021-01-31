import write_google_sheets, read_play_cricket

# Test links
test_links = ['https://uniofwarwick.play-cricket.com/website/results/4050085',
              'https://uniofwarwick.play-cricket.com/website/results/4050521',
              'https://uniofwarwick.play-cricket.com/website/results/4052769',
              'https://uniofwarwick.play-cricket.com/website/results/4052768']

for i, link in enumerate(test_links):
    print('The current iteration uses this link: ' + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, i + 1)
    print('\n All stats have been updated for game: ' + link + ' \n')




