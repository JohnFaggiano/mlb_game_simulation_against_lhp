def get_player_outcome(first_name, last_name):
    from pybaseball import statcast_batter, playerid_lookup
    import random 

    player = playerid_lookup(last_name, first_name)
    player_id = int(player.loc[0, "key_mlbam"])
    df = statcast_batter("2025-03-27", "2025-09-28", player_id) # extracts all ABs the player recorded in 2025

    df_lhp = df[df['p_throws'] == 'L'] # isolates the player's ABs specifically against lefties

    outs_events = ['field_out', 'force_out', 'grounded_into_double_play', 'triple_play', 'double_play'] # a list of potential events the at-bat returns

    walks = (df_lhp['events'] == 'walk').sum() # the sum of the number of times [df1_lhp['events'] == 'walk'] was True, ie the sum of walks the player drew against left-handed pitchers in 2025
    singles = (df_lhp['events'] == 'single').sum()
    doubles = (df_lhp['events'] == 'double').sum()
    triples = (df_lhp['events'] == 'triple').sum()
    home_runs = (df_lhp['events'] == 'home_run').sum()
    strikeouts = (df_lhp['events'] == 'strikeout').sum()
    outs_in_play = (df_lhp['events'].isin(outs_events)).sum()
    pa = len(df_lhp) # sum of all plate appearances the player had against left-handed pitchers in 2025
    if pa == 0:
        return 'out in play' # avoids division by 0 in the next step if the player has zero plate appearances in 2025, and assumes out in play

    outcomes = ['walk', 'single', 'double', 'triple', 'home_run', 'strikeout', 'out in play'] # creates list of potential outcomes for the player's plate appearance
    probabilities = [walks/pa, singles/pa, doubles/pa, triples/pa, home_runs/pa, strikeouts/pa, outs_in_play/pa] # assigns probabilities to each outcome based upon the player's 2025 statistics, ie. if the player walked 33/100 times, a 33% walk probability is assigned.
    result = random.choices(outcomes, probabilities)[0] # produces a randomized outcome based upon the probabilities assigned to each outcome
    return result

def main():
    from pybaseball import playerid_lookup
    innings = 0
    runs = 0

    i = 0 # i identifies the batter currently up to bat
    while True: # purpose is to ensure the user inputs only official MLB players who played in 2025
        try:
            players = [p.strip() for p in input("Input today's lineup against LHP (commas separated): ").split(',')] # calls for user to print nine-item list, which is the lineup
            while innings < 9:
                outs = 0
                first_base = second_base = third_base = 0 # declares first_base, second_base, and third_base as variables to determine how many runners are on each base at a given moment
                if len(players) == 9: # ensures the code will only run if the user inputs nine items
                    print(f"Start of inning {innings + 1}")
                    while outs < 3: # ends the loop when outs = 3, signalling the end of the inning
                        ab = get_player_outcome(players[i].split()[0], players[i].split()[1]) # calls get_player_outcome to return randomized outcome for players[i]
                        if ab == 'walk':
                            print(f"{players[i]} walks. ")
                            if first_base == 0:
                                first_base = 1 # walk adds runner to first
                            elif first_base == 1 and second_base == 0 and third_base == 0:
                                second_base = 1 # if runner on first and there is a walk, runner count on second moves to 1 while runner count on first stays 1
                            elif first_base == 1 and second_base == 1:
                                if third_base == 1:
                                    runs += 1 # bases loaded --> runner scores
                                third_base = 1 # men on first and second --> a walk automatically increases the number of runners on third to 1
                            first_base = 1

                        elif ab == 'single':
                            print(f"{players[i]} hits a single.")
                            if first_base == 0:
                                first_base = 1
                            elif first_base == 1 and second_base == 0 and third_base == 0:
                                second_base = 1
                            elif first_base == 1 and second_base == 1:
                                if third_base == 1:
                                    runs += 1
                                third_base = 1
                            first_base = 1

                        elif ab == 'double':
                            print(f"{players[i]} hits a double.")
                            if (second_base == 1 and third_base == 0) or (second_base == 0 and third_base == 1):
                                runs += 1
                            elif second_base == 1 and third_base == 1:
                                runs += 2
                            elif first_base == 1:
                                first_base = 0
                                third_base = 1 # assumes runner simply moves from first to third on the double
                            second_base = 1

                        elif ab == 'triple':
                            print(f"{players[i]} hits a triple.")
                            runs += first_base + second_base + third_base # adds the sum of the runners currently on base
                            first_base = second_base = 0
                            third_base = 1

                        elif ab == 'home_run':
                            print(f"{players[i]} hits a home run.")
                            runs += 1 + first_base + second_base + third_base # runs increase by 1 + the amount of runners on base at that moment
                            first_base = second_base = third_base = 0

                        elif ab == 'strikeout':
                            print(f"{players[i]} strikes out.")
                            outs += 1

                        else:
                            print(f"{players[i]} makes contact, out in play.")
                            outs += 1
                        print(f"Runs scored: {runs}.")

                        if first_base == 0 and second_base == 0 and third_base == 0:
                            print("Bases empty.")
                        elif first_base == 1 and second_base == 0 and third_base == 0:
                            print("Man on first.")
                        elif first_base == 0 and second_base == 1 and third_base == 0:
                            print("Man on second.")
                        elif first_base == 0 and second_base == 0 and third_base == 1:
                            print("Man on third.")
                        elif first_base == 1 and second_base == 1 and third_base == 0:
                            print("Men on first and second.")
                        elif first_base == 1 and second_base == 0 and third_base == 1:
                            print("Men on first and third.")
                        elif first_base == 0 and second_base == 1 and third_base == 1:
                            print("Men on second and third.")
                        else:
                            print("Bases loaded.")

                        print(f"Outs: {outs}")

                        if outs == 3:
                            print(f"Inning {innings + 1} is over.") # ends the inning
                            innings += 1
                            if innings == 9: # breaks out of loop because the game is now over
                                return

                        i += 1 # moves on to next batter in the lineup
                        if i == 9:
                            i = 0 # resets the lineup to return the start after the 9th batter in the order has hit, ensuring player[0] is up next

                else:
                    print("Please print nine names, first and last, that include MLB players.") # if the user did not initially input nine items
                    break

        except Exception: # opens up possibility that the user mistyped a name or included a player not in the MLB in 2025, leading to the user being asked to provide 9 players again
            print("One or more players provided were not in the MLB in 2025. Please input official MLB players.")

main()
