#Inte säker på vilken input som kommer hit
#Tänker att det är listor på juryklickar varje år och listor på teleklickar varje år?

jury_23 = [[1, 15, 14],[1, 2]]
tele_23 = [[]]
jury_22 = [[1, 4],[7, 9]]
tele_22 = [[]]
jury_21 = [[5, 6]] 
tele_21 = [[]]
jury_20 = [[1, 5]] 
tele_20 = [[]]
jury_19 = [[4, 5]] 
tele_19 = [[]]
jury_18 = [[1, 12], [4, 1]] 
tele_18 = [[25, 26]]
jury_17 = [[]] 
tele_17 = [[25, 16]]
jury_16 = [[22, 25]] 
tele_16 = [[25, 26]]

jury_list = [jury_16, jury_17, jury_18, jury_19, jury_20, jury_21, jury_22, jury_23]
tele_list = [tele_16, tele_17, tele_18, tele_19, tele_20, tele_21, tele_22, tele_23]

class Land:
    def __init__(self, name):
        self.name = name

    in_jury_clique = 0
    in_tele_clique = 0

    current_jury_streak = 0
    current_tele_streak = 0
    longest_jury_streak = 0
    longest_tele_streak = 0

class Clique:
    def __init__(self, clique):
        self.clique = sorted(clique)
    
    jury_years = 0
    tele_years = 0

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

jury_clique_list = []
tele_clique_list = []

for i in range(len(landlista)):
    for jury_years in jury_list:
        for jury_cliques in jury_years:
            if (i+1) in jury_cliques:
                landlista[i].in_jury_clique += 1
                landlista[i].current_jury_streak += 1
            else:
                if landlista[i].current_jury_streak > landlista[i].longest_jury_streak:
                    landlista[i].longest_jury_streak = landlista[i].current_jury_streak
                landlista[i].current_jury_streak = 0
    for tele_years in tele_list:
        for tele_cliques in tele_years:
            tele_clique_list.append(sorted(tele_cliques))
            if (i+1) in tele_cliques:
                landlista[i].in_tele_clique += 1
                landlista[i].current_tele_streak += 1
            else:
                if landlista[i].current_tele_streak > landlista[i].longest_tele_streak:
                    landlista[i].longest_tele_streak = landlista[i].current_tele_streak
                landlista[i].current_tele_streak = 0

for jury_years in jury_list:
    for jury_cliques in jury_years:
         jury_clique_list.append(sorted(jury_cliques))   
for tele_years in tele_list:
    for tele_cliques in tele_years:
        tele_clique_list.append(sorted(tele_cliques))

for cliques in jury_clique_list:
    print(f"{cliques} var en klick {jury_clique_list.count(cliques)} gånger")

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

print(f"Jury champ: Land {jury_clique_champ.name} i {jury_clique_champ.in_jury_clique} jury klickar totalt")
print(f"Tele champ: Land {tele_clique_champ.name} i {tele_clique_champ.in_tele_clique} televote klickar totalt")
print(f"Längsta streak att vara med i någon juryklick: \nLand {jury_streak_champ.name}, {jury_streak_champ.longest_jury_streak} år i rad")
print(f"Längsta streak att vara med i någon televoteklick: \nLand {tele_streak_champ.name}, {tele_streak_champ.longest_tele_streak} år i rad")
