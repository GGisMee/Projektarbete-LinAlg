# Gemensamt projekt linjär algebra
**Medlemmar:** Gustav Gamstedt, Noah Marklund, Edvin Blomberg, Alfred Hansson och Jesper Steinarson
**Grupp:** Grafteori 9

För att köra koden använd 
* compare_cliques_data.py (För )
* visualise_cliques.py (För visualisering)

### Funktionsdelar i koden
Hämta data från fil och få det till matriser (Noah) 
* Input CSV fil
* Output: np.array (n x n) och lista med länder av typ str
Behandla data så vi har en matris med 1:or och 0:or - Jesper
* Input: np.array (n x n) från funktionsdel 1. 
* Output: np.array (n x n) alltså nodmatrisen,
Hitta vilka som är i klickar - Jesper
* Input: np.array (n x n) från funktionsdel 2, lista med länder av typ str. 
* Output: Lista med indexar för de länder i klickar (typ np.array)
Dela upp dem i separata klickar (Output) - Edvin
* Input: Matris från funktionsdel 2 och lista med listor av indexar från länder i klickar från funktionsdel 2. 
* Output: Lista med listor av indexar för länder i klickar 
Rangordna klickarna efter storlek. (Output) - Alfred
* Input: Lista med listor av indexar från länder i klickar från funktionssteg 4
Output: Lista med ordnade listor av indexar för länder i klickar
Visa klickar på lämpligt sätt (Output) - Gustav
* Input: lista från steg 2 
* Output: visas på skärm
Jämför olika års data samt jämför televote och jury (Output) - Alfred
* Input: 
Exempel på vad man kan göra:
Se vilka som har varit i klickar på många år
