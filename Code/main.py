import hillclimber as hill
import sim_an_lin as lin
import sim_an_ex as ex
import sim_an_log as log
import random_sampling as rand

proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]

for i in range(len(proteinlist)):
    print(i+1, ":", proteinlist[i])

proteinnumber = int(input("Hello, which protein would you like to use? "))-1

print("Your choice is", proteinlist[proteinnumber])
heuristicslist = ["Random Sampling", "Hillclimber", "Simulated Annealing Linear", "Simulated Annealing Exponential", "Simulated Annealing Logarithmic"]

for i in range(len(heuristicslist)):
    print(i+1, ":", heuristicslist[i])

heuristicsnumber = int(input("Which type of algorithm would you like to use? "))-1

print("Your choice is", heuristicslist[heuristicsnumber])
print("One moment please...")

if heuristicsnumber == 0:
    print("The stabilityscore is ", rand.random_structure_without_collision(proteinlist[proteinnumber]))
elif heuristicsnumber == 1:
    print("The stabilityscore is ", hill.hillclimber(proteinlist[proteinnumber]))
elif heuristicsnumber == 2:
    print("The stabilityscore is ", ex.sim_anneal(proteinlist[proteinnumber], int(1)))
elif heuristicsnumber == 3:
    cool = str(ex)
    print("The stabilityscore is ", ex.sim_anneal(proteinlist[proteinnumber], int(2)))
elif heuristicsnumber == 4:
    cool = str(log)
    print("The stabilityscore is ", ex.sim_anneal(proteinlist[proteinnumber], int(3)))




