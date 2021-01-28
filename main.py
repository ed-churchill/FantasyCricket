import read_play_cricket
import write_google_sheets

# Test links
test_links = ['https://uniofwarwick.play-cricket.com/website/results/4050085',
              'https://uniofwarwick.play-cricket.com/website/results/4050303',
              'https://uniofwarwick.play-cricket.com/website/results/4050521',
              'https://uniofwarwick.play-cricket.com/website/results/4082463',
              'https://uniofwarwick.play-cricket.com/website/results/4052772',
              'https://uniofwarwick.play-cricket.com/website/results/4082743',
              'https://uniofwarwick.play-cricket.com/website/results/4052769',
              'https://uniofwarwick.play-cricket.com/website/results/4052768',
              'https://uniofwarwick.play-cricket.com/website/results/4026201']

for link in test_links:
    print('The current iteration uses this link: ' + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 1)




