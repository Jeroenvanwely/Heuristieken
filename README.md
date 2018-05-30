# Proteinpowder

Eiwitten zijn de bouwstenen van het leven. Ze zorgen dat alle processen in het menselijk (en dierlijk) lichaam goed verlopen. De vouwing van een specifiek eiwit is belangrijk voor het gedrag van dit proteine. Dit is een belangrijk punt voor het synthetiseren van een eiwit. Dit eiwit moet hier op de juiste manier gevouwen zijn wil het de juiste effecten hebben. Nu bestaat een eiwit uit hydrofobe (H) en polaire aminozure (P) en cysteïne (C). De hydrofobe aminozuren willen graag naast elkaar liggen, om zo een H-bond te vormen, die stabiliteit -1 aan het eiwit geeft. Als een cysteïne aminozuur en een hydrofobe aminozuur naast elkaar liggen zorgt die ook voor een stabiliteit van -1. Twee cysteïne moleculen zorgen echter voor een stabiliteit van -5.  Hoe meer H-bonds, CH-bonds of CC-bonds een eiwit heeft, hoe stabieler het eiwit.

![alt text](http://heuristieken.nl/wiki/images/3/3a/GoodBadFoldings.jpg)
Bron: Daan van den Berg, http://heuristieken.nl/wiki/images/3/3a/GoodBadFoldings.jpg

Dit vouwen van eiwitten tot een zo stabiel mogelijke vouwing kan gezien worden als een constrained optimization problem. Door het schrijven van de juiste algoritmes kan er ontdekt worden wat de laagste score (de stabielste vorm) van een specifiek eiwit is. In dit onderzoek zijn er verschillende algoritmes gebruikt om dit probleem te proberen oplossen. Hiermee gaan we op zoek naar het 'beste' algoritme voor dit probleem. 
Onder de map Code is de code te vinden die hiervoor geschreven is. In de map Data is de data die gebruikt is voor dit probleem. To watch this problem 'unfold' gaat u naar het mapje met Results, waar de resultaten zowel in csv bestandjes als in visualisaties te zien zijn.

## Vereisten

De hieropvolgende codebase is geschreven in Python 3.6.3. Alle packages die nodig zijn om de code succesvol te draaien zijn te vinden in requirements.txt en kunnen gemakkelijk geintstalleerd worden d.m.v. de volgende instructie:

pip install -r requirements.txt

## Structuur

In het Data mapje, zal alle data die nodig is voor het gebruiken van deze files te vinden zijn. 

In het Code mapje, zal alle code the vinden zijn die geschreven is.

In het Results mapje zullen alle resultaten worden opgeslagen.

## Testen

Gebruik de volgende constructie om de code te runnen met een heuristiek naar keuze:

python main.py

## Auteurs

Melanie Baaten 11053909
...

## Dankwoord

