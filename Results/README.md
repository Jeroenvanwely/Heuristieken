# Results

In de results zijn de resultaten te vinden van de verschillende algoritmes die zijn toegepast.

## Hillclimber

Hier zijn de scores te vinden van het Hillclimber algoritme. De eerste file staat voor het eerste proteïne die te vinden is in het csv bestandje van de proteïnes onder de map Data. De tweede file correspondeert met het tweede proteïne enzovoorts. 
De hillclimber is op elk proteïne 10.000 keer toegepast. Hier zijn vervolgens 30 resultaten van elk proteïne opgeslagen in het proteïne-specifieke mapje hiervoor.

## Simulated Annealing

Onder deze map zijn verschillende cooling schema's te vinden. Onder elk specifiek cooling schema zijn er twee verschillende bestandjes te vinden. 

### Course bestand

Deze weergeeft data waaruit het verloop van het algoritme te bepalen is. Hier staat telkens de huidige score, gevolgd door een lijst met de coördinaten van de Aminodes. De eerste invoer is de startscore en startpositie die meegegeven is vanuit de hillclimber. Vanaf regel 3 geldt er: Iteratie = (regellijn % 2 =\= 0) - 2. Hiermee kan de temperatuur en de probability bepaald worden.

### Result bestand

Hier zijn de scores te vinden die de simulated annealing met cooling schema X gemaakt heeft. Opnieuw geldt dat de eerste file staat voor het eerste proteïne die te vinden is in het csv bestandje van de proteïnes onder de map Data. De tweede file correspondeert met het tweede proteïne enzovoorts. 
Elke cooling scheme van de simulated annealing is weer 10.000 iteraties lang gedaan.  Hier zijn vervolgens 30 resultaten van elk proteïne opgeslagen in het proteïne-specifieke mapje hiervoor.