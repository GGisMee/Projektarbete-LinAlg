#importera listor från olika år antar jag?
#Insåg att det här är fel, ska fixa när jag hinner
#Blir väl en lista på år med en lista på klickar från varje år?
#Alltså
#Lista på år 
# --> Lista på juryklickar det året + Lista på televoteklickar det året 
# --> Lista på länder i varje klick

jury_23 = [1, 2]
tele_23 = []
jury_22 = [1, 4]
tele_22 = []
jury_21 = [5, 6] 
tele_21 = []
jury_20 = [1, 5] 
tele_20 = []
jury_19 = [4, 5] 
tele_19 = []
jury_18 = [1, 12] 
tele_18 = []
jury_17 = [] 
tele_17 = []
jury_16 = [22, 25] 
tele_16 = [25, 26]

jury_list = [jury_16, jury_17, jury_18, jury_19, jury_20, jury_21, jury_22, jury_23]
tele_list = [tele_16, tele_17, tele_18, tele_19, tele_20, tele_21, tele_22, tele_23]

antal_land = 26

class Land:
    def __init__(self, name):
        self.name = name

    in_jury_clique = 0
    in_tele_clique = 0

    current_jury_streak = 0
    current_tele_streak = 0
    longest_jury_streak = 0
    longest_tele_streak = 0

land1 = Land("1")
land2 = Land("2")
land3 = Land("3")
land4 = Land("4")
land5 = Land("5")
land6 = Land("6")
land7 = Land("7")
land8 = Land("8")
land9 = Land("9")
land10 = Land("10")
land11 = Land("11")
land12 = Land("12")
land13 = Land("13")
land14 = Land("14")
land15 = Land("15")
land16 = Land("16")
land17 = Land("17")
land18 = Land("18")
land19 = Land("19")
land20 = Land("20")
land21 = Land("21")
land22 = Land("22")
land23 = Land("23")
land24 = Land("24")
land25 = Land("25")
land26 = Land("26")

landlista = (land1, land2, land3, land4, land5, land6, land7, land8, land9, land10, land11, land12, land13, land14, land15,
             land16, land17, land18, land19, land20, land21, land22, land23, land24, land25, land26)

for i in range(antal_land):
    for jury_years in jury_list:
        if (i+1) in jury_years:
            landlista[i].in_jury_clique += 1
            landlista[i].current_jury_streak += 1
        else:
            if landlista[i].current_jury_streak > landlista[i].longest_jury_streak:
                landlista[i].longest_jury_streak = landlista[i].current_jury_streak
            landlista[i].current_jury_streak = 0
    for tele_years in tele_list:
        if (i+1) in tele_years:
            landlista[i].in_tele_clique += 1
            landlista[i].current_tele_streak += 1
        else:
            if landlista[i].current_tele_streak > landlista[i].longest_tele_streak:
                landlista[i].longest_tele_streak = landlista[i].current_tele_streak
            landlista[i].current_tele_streak = 0

jury_clique_champ = land1
tele_clique_champ = land1
tele_streak_champ = land1
jury_streak_champ = land1

for land in landlista:
    if (land.in_jury_clique > jury_clique_champ.in_jury_clique):
        jury_clique_champ = land
    if (land.in_tele_clique > tele_clique_champ.in_tele_clique):
        tele_clique_champ = land
    if (land.longest_jury_streak > jury_streak_champ.longest_jury_streak):
        jury_streak_champ = land
    if (land.longest_tele_streak > tele_streak_champ.longest_tele_streak):
        tele_streak_champ = land

print(f"Jury champ: Land {jury_clique_champ.name} i {jury_clique_champ.in_jury_clique} jury klickar")
print(f"Tele champ: Land {tele_clique_champ.name} i {tele_clique_champ.in_tele_clique} televote klickar")
print(f"Längsta streak i en juryklick: Land {jury_streak_champ.name}, {jury_streak_champ.longest_jury_streak} år i rad")
print(f"Längsta streak i en televoteklick: Land {tele_streak_champ.name}, {tele_streak_champ.longest_tele_streak} år i rad")

#jury_clique_champ, tele_clique_champ = find_clique_records(landlista)

#print(f"{jury_clique_champ} var i juryklickar flest gånger, {tele_clique_champ} var i televoteklickar flest gånger")
