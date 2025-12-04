# Inte säker på vilken input som kommer hit
# Tänker att det är listor på juryklickar varje år och listor på teleklickar varje år?
# Koden är ganska lång, men mer än hälften är bara en massa testlistor

# En lista på klickar för jury och televotes (inte korrekta, bara test)
# Blev lättare att jämföra olika länder med en klass
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

def top_by_attribute(top_list, land, attribute, attribute2):
    # Tar emot en lista, ett land, ett attribut hos land som det ska sorteras efter
    # Och ett andra attribut, vilket behövs då funktionen anropas när man vill
    # hålla koll på både hur många år i rad den har varit i en klick just nu och 
    # hur många år i rad den har varit i en klick som längst
    if (top_list == [] or getattr(land, attribute) > getattr(top_list[0], attribute)):
        top_list.clear()
        top_list.append(land)
    elif (getattr(land, attribute) == getattr(top_list[0], attribute2)):
        top_list.append(land)


def count_clique_participation(v, i, type_of_clique, streak_type, long_streak_type, landlista):
    # Tar emot en lista, ett index för vilket land som räknas, om det är jury eller teleklick som räknas
    # vilken streak som räknas, vilken längsta streak som ska passeras
    for years in v:
        for cliques in years:
            if (i+1) in cliques:
                setattr(landlista[i], type_of_clique, getattr(landlista[i], type_of_clique) + 1)
                setattr(landlista[i], streak_type, getattr(landlista[i], streak_type) + 1)
            else:
                setattr(landlista[i], streak_type, getattr(landlista[i], streak_type) + 1)
                if getattr(landlista[i], streak_type) > getattr(landlista[i], long_streak_type):
                    setattr(landlista[i], long_streak_type, getattr(landlista[i], streak_type))
                setattr(landlista[i], streak_type, 0)


def count_clique_occurence(clique_list, most_common):
    done_cliques = []
    most_common_number = 0
    for cliques in clique_list:
        if (cliques not in done_cliques and cliques != []):
            done_cliques.append(cliques)
            if (most_common == [] or clique_list.count(cliques) > len(most_common[0])):
                most_common.clear()
                most_common.append(cliques)
                most_common_number = clique_list.count(cliques)
            elif (clique_list.count(cliques) == len(most_common[0])):
                most_common.append(cliques)
    return most_common_number

def run(jury_list, tele_list, countries:list[str]):
    '''Funktionen skriver ut en del information om klickarna utifrån data från flera år 
    jury_list: en lista med sublistor av klickar från flera år för jury rösterna
    tele_list: en lista med sublistor av klickar från flera år för tele rösterna
    countries: en lista med alla länder.
    '''
    # Lista på klickar som har förekommit minst en gång
    jury_clique_list = []
    tele_clique_list = []


    # Lång lista på länder, kanske går med en dictionary istället
    landlista = [Land(country) for country in countries]


    for i in range(len(landlista)):
        count_clique_participation(jury_list, i, "in_jury_clique", "current_jury_streak", "longest_jury_streak", landlista)
        count_clique_participation(tele_list, i, "in_tele_clique", "current_tele_streak", "longest_tele_streak", landlista)

    for jury_years in jury_list:
        for jury_cliques in jury_years:
             jury_clique_list.append(sorted(jury_cliques))   
    for tele_years in tele_list:
        for tele_cliques in tele_years:
            tele_clique_list.append(sorted(tele_cliques))

    common_tele_clique = []
    common_tele_clique_number = 0
    common_jury_clique = []
    common_jury_clique_number = 0

    common_jury_clique_number = count_clique_occurence(jury_clique_list, common_jury_clique)
    common_tele_clique_number = count_clique_occurence(tele_clique_list, common_tele_clique)

    # Topplistor för vilka länder som var med i flest klickar
    top_jury_clique = []
    top_tele_clique = []
    # Topplistor för vilka länder som var i klickar flest år i rad, inte nödvändigtvis samma klick varje år
    top_jury_streak = []
    top_tele_streak = []

    for land in landlista:
        top_by_attribute(top_jury_clique, land, "in_jury_clique", "in_jury_clique")
        top_by_attribute(top_tele_clique, land, "in_tele_clique", "in_tele_clique")
        top_by_attribute(top_jury_streak, land, "longest_jury_streak", "in_jury_clique")
        top_by_attribute(top_tele_streak, land, "longest_tele_streak", "in_tele_clique")

    cliques_in_both = []

    if len(jury_list) and len(tele_list):
        for i in range(len(jury_list) - 1):
            for j_cliques in jury_list[i]:
                for t_cliques in tele_list[i]:
                    if sorted(j_cliques) == sorted(t_cliques):
                        cliques_in_both.append((2016+i, (sorted(j_cliques))))
    
    # Byter ut siffrorna i listorna till motsvarande land
    for cliques in common_jury_clique:
        for i in range(len(cliques)):
            cliques[i] = landlista[cliques[i]-1]
    for cliques in common_tele_clique:
        for j in range(len(cliques)):
            cliques[j] = landlista[cliques[j]-1]

    # Print-satser för alla resultat som hittats    
    print(f"Med i flest jury-klickar: {top_jury_clique} i {top_jury_clique[0].in_jury_clique} jury klickar totalt")
    print(f"Med i flest televote-klickar: {top_tele_clique} i {top_tele_clique[0].in_tele_clique} televote klickar totalt")
    print(f"\nLängsta streak att vara med i någon juryklick: \n{top_jury_streak}, {top_jury_streak[0].longest_jury_streak} år i rad inte ensam")
    print(f"\nLängsta streak att vara med i någon televoteklick: \n{top_tele_streak}, {top_tele_streak[0].longest_tele_streak} år i rad inte ensam")
    print(f"\nVanligaste jury-klicken/klickarna:\n{common_jury_clique}, förekom {common_jury_clique_number} gånger")
    print(f"Vanligaste televote-klicken/klickarna:\n{common_tele_clique}, förekom {common_tele_clique_number} gånger")
    print("\nKlickar som fanns både bland jury och televote: ")
    # cliques_in_both är en lista med tupler, varav ena är en lista
    # ser ut som [[20XX, [1, 2]], [20XX, [3, 4]]]
    for years in range(len(cliques_in_both)):
        for cliques in range(len(cliques_in_both[years][1])):
            cliques_in_both[years][1][cliques] = landlista[cliques_in_both[years][1][cliques]-1]
        print(f"{cliques_in_both[years][0]}: {cliques_in_both[years][1]}")


if __name__ == '__main__':
    # Lång lista på länder, kanske går med en dictionary istället
    # Vet inte hur en loop för det skulle se ut om de ska ha olika namn, inte bara land_1, land_2 etc	
    sim_landlista = ["Austria","Iceland","Azerbaijan","San Marino","Czech Republic",
             "Ireland","Georgia","Bosnia and Herzegovina","Malta","Spain",
             "Finland","Switzerland","Denmark","France","Moldova","Armenia",
             "Cyprus","Bulgaria","Netherlands","Latvia","Israel","Belarus", 
             "Germany","Russia","Norway","Australia","Belgium","United Kingdom",
             "Croatia","Greece","Lithuania","Serbia","Macedonia","Albania",
             "Estonia","Ukraine","Italy","Poland","Slovenia","Hungary",
             "Montenegro","Sweden"]
    jury_23 = [[1, 15, 14],[1, 2]]
    tele_23 = [[25, 16, 11]]
    jury_22 = [[1, 4],[7, 9]]
    tele_22 = [[16, 11, 25]]
    jury_21 = [[5, 6]] 
    tele_21 = [[]]
    jury_20 = [[1, 5], [22, 25], [14, 1, 15]] 
    tele_20 = [[]]
    jury_19 = [[4, 5, 1, 7], [15, 18]] 
    tele_19 = [[5, 1, 7, 4], [18, 15]]
    jury_18 = [[1, 12], [4, 1, 5]] 
    tele_18 = [[25, 26]]
    jury_17 = [[22, 5]] 
    tele_17 = [[11, 25, 16], [22, 5]]
    jury_16 = [[22, 25], [5, 18]] 
    tele_16 = [[25, 26]]

    # Listor med jury och televotes
    jury_list = [jury_16, jury_17, jury_18, jury_19, jury_20, jury_21, jury_22, jury_23]
    tele_list = [tele_16, tele_17, tele_18, tele_19, tele_20, tele_21, tele_22, tele_23]
    tele_list = []
    run(jury_list, tele_list, countries=sim_landlista)