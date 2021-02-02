import write_google_sheets, read_play_cricket

week_one = ['https://uniofwarwick.play-cricket.com/website/results/4050085',
'https://uniofwarwick.play-cricket.com/website/results/4050303', 
'https://uniofwarwick.play-cricket.com/website/results/4050521',
'https://uniofwarwick.play-cricket.com/website/results/4082463']

week_two = ['https://uniofwarwick.play-cricket.com/website/results/4052772',
'https://uniofwarwick.play-cricket.com/website/results/4082743', 
'https://uniofwarwick.play-cricket.com/website/results/4052769',
'https://uniofwarwick.play-cricket.com/website/results/4052768']

week_three = ['https://uniofwarwick.play-cricket.com/website/results/4026201',
'https://uniofwarwick.play-cricket.com/website/results/4026195',
'https://uniofwarwick.play-cricket.com/website/results/4055612']

week_four = ['https://uniofwarwick.play-cricket.com/website/results/4057064',
'https://uniofwarwick.play-cricket.com/website/results/4057064']

# Update week 1
for link in week_one:
    print("\nThe current iteration uses this link: " + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 1)
    print("\n Successfully updated stats for the game using this link: " + link)

# Update week 2
for link in week_two:
    print("\nThe current iteration uses this link: " + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 2)
    print("\n Successfully updated stats for the game using this link: " + link)

# Update week 3
for link in week_three:
    print("\nThe current iteration uses this link: " + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 3)
    print("\n Successfully updated stats for the game using this link: " + link)

# Update week 4
for link in week_four:
    print("\nThe current iteration uses this link: " + link)
    bat_df, bowl_df, field_df = read_play_cricket.clean_scorecards(link)
    write_google_sheets.update_stats(bat_df, bowl_df, field_df, 4)
    print("\n Successfully updated stats for the game using this link: " + link)