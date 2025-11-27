#Inte säker på vilken input som kommer hit
#Tänker att det är listor på juryklickar varje år och listor på teleklickar varje år?

jury_23 = [[1, 15, 14],[1, 2]]
tele_23 = [[25, 16, 11]]
jury_22 = [[1, 4],[7, 9]]
tele_22 = [[16, 11, 25]]
jury_21 = [[5, 6]] 
tele_21 = [[]]
jury_20 = [[1, 5]] 
tele_20 = [[]]
jury_19 = [[4, 5]] 
tele_19 = [[]]
jury_18 = [[1, 12], [4, 1, 5]] 
tele_18 = [[25, 26]]
jury_17 = [[5, 22]] 
tele_17 = [[11, 25, 16]]
jury_16 = [[22, 25], [5, 18]] 
tele_16 = [[25, 26]]

jury_list = [jury_16, jury_17, jury_18, jury_19, jury_20, jury_21, jury_22, jury_23]
tele_list = [tele_16, tele_17, tele_18, tele_19, tele_20, tele_21, tele_22, tele_23]

class Land:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

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

def top_by_attribute(top_list, land, attribute, attribute2):
    if (top_list == [] or getattr(land, attribute) > getattr(top_list[0], attribute)):
        top_list.clear()
        top_list.append(land)
    elif (getattr(land, attribute) == getattr(top_list[0], attribute2)):
        top_list.append(land)

jury_clique_list = []
tele_clique_list = []

def count_clique_participation(v, i, type_of_clique):
    # Tar emot en lista, ett index för vilket land som räknas, om det är jury eller teleklick som räknas
    # Ändrar direkt i listan, förmodligen dåligt
    for years in v:
        for cliques in years:
            if (i+1) in cliques:
                if type_of_clique == "jury":
                    landlista[i].in_jury_clique += 1
                    landlista[i].current_jury_streak += 1
                elif type_of_clique == "tele":
                    landlista[i].in_tele_clique += 1
                    landlista[i].current_tele_streak += 1
            else:
                if type_of_clique == "jury":
                    if landlista[i].current_jury_streak > landlista[i].longest_jury_streak:
                        landlista[i].longest_jury_streak = landlista[i].current_jury_streak
                    landlista[i].current_jury_streak = 0
                elif type_of_clique == "tele":
                    if landlista[i].current_tele_streak > landlista[i].longest_tele_streak:
                        landlista[i].longest_tele_streak = landlista[i].current_tele_streak
                    landlista[i].current_tele_streak = 0

for i in range(len(landlista)):
    count_clique_participation(jury_list, i, "jury")
    count_clique_participation(tele_list, i, "tele")

for jury_years in jury_list:
    for jury_cliques in jury_years:
         jury_clique_list.append(sorted(jury_cliques))   
for tele_years in tele_list:
    for tele_cliques in tele_years:
        tele_clique_list.append(sorted(tele_cliques))

tele_done_cliques = []
jury_done_cliques = []

for cliques in (jury_clique_list):
    if (cliques not in jury_done_cliques):
        print(f"{cliques} var en klick för juryröster {jury_clique_list.count(cliques)} gånger")
        jury_done_cliques.append(cliques)
for cliques in (tele_clique_list):
    if (cliques not in tele_done_cliques):
        print(f"{cliques} var en klick för teleröster {tele_clique_list.count(cliques)} gånger")
        tele_done_cliques.append(cliques)

top_jury_clique = []
top_tele_clique = []
top_jury_streak = []
top_tele_streak = []

for land in landlista:
    top_by_attribute(top_jury_clique, land, "in_jury_clique", "in_jury_clique")
    top_by_attribute(top_tele_clique, land, "in_tele_clique", "in_tele_clique")
    top_by_attribute(top_jury_streak, land, "longest_jury_streak", "in_jury_clique")
    top_by_attribute(top_tele_streak, land, "longest_tele_streak", "in_tele_clique")

print(f"Jury champ: Land {top_jury_clique} i {top_jury_clique[0].in_jury_clique} jury klickar totalt")
print(f"Tele champ: Land {top_tele_clique} i {top_tele_clique[0].in_tele_clique} televote klickar totalt")
print(f"Längsta streak att vara med i någon juryklick: \nLand {top_jury_streak}, {top_jury_streak[0].longest_jury_streak} år i rad")
print(f"Längsta streak att vara med i någon televoteklick: \nLand {top_tele_streak}, {top_tele_streak[0].longest_tele_streak} år i rad")
