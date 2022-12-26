import csv
import CandidateElimination

with open('./data/TDCE.csv', mode='r') as csv_file:
    csv_list = list(csv.reader(csv_file))
    all_possible_values = [["Sunny", "Rainy"],
                           ["Warm", "Cold"], ["Normal", "High"], ["Strong", "Weak"], ["Warm", "Cool"], ["Same", "Change"]]
    V = CandidateElimination.CandidateElimination(
        csv_list)
    print(V)
