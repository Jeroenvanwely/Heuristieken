import hillclimber as hill

proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]

for i in range(len(proteinlist)):
    print(i+1, ":", proteinlist[i])

proteinnumber = int(input("Hello, which protein would you like to use? "))-1

print("Your choice is", proteinlist[proteinnumber])
heuristicslist = ["Random Sampling", "Hillclimber", "Simulated Annealing"]

for i in range(len(heuristicslist)):
    print(i+1, ":", heuristicslist[i])

heuristicsnumber = int(input("Which type of heuristic would you like to use? "))-1

print("Your choice is", heuristicslist[heuristicsnumber])

if heuristicsnumber == 1:
    hill.hillclimber(proteinlist[proteinnumber])




