import run_minizinc_batch_2 as batch
import dzn_generator as generator
import dzn_export as export
from os.path import join, exists

def add2file(path, content):
    with open(path, mode='a') as f:
        f.writelines(content)

if __name__ == "__main__":
    
    id = "bruno"
    pourcentage_nb_coach = 1 
    models = ["model_alldiff_regular", "model_alldiff_sat", "model_sums_regular", "model_sums_sat"]
    scenarios = []

    for n_teams in range(5, 40, 5):

        scenario = {
                "name" : "toy",
                "n_periods" : 2*n_teams,
                "n_venues" : 4,
                "n_teams": n_teams,
                "n_coaches": int(n_teams * pourcentage_nb_coach),
                "n_teams_per_division" : [5] * (n_teams // 5),
                "break_duration" : 2
            }
   
        scenarios.append(scenario)
   
    scenario = generator.Scenario(seed=456) 

    for model in models:

        for s in scenarios:

            n = s["name"]
            p = s["n_periods"]
            v = s["n_venues"]
            t = s["n_teams"]
            c = s["n_coaches"]
            d = s["n_teams_per_division"]
            b = s["break_duration"]
            
            test_path = f"test_{id}/{model}-t{t}-p{p}-d{len(d)}-v{v}-c{c}-{b}"
            dzn_file = f"{test_path}.dzn"
            result_file = f"{test_path}.txt"

            random_scenario = scenario.generate_scenario(n, p, v, t, c, d) 
            export.export(dzn_file, random_scenario)
          
            outputSatisfiable = f"test_{id}/satisfiable.out"
            outputUnSatisfiable = f"test_{id}/un_satisfiable.out"
            outputUnSatisfiableTimeout = f"test_{id}/timeout.out"
            outputUnSatisfiableError = f"test_{id}/error.out"

            resultat = f"{model};{t};{p};{len(d)};{v};{c};{b}"
            print("Model: " + resultat)

            try:
                unsatisfiable, duration, node, nogood = batch.excuteMinizinc(f"../models/{model}.mzn", dzn_file, result_file, 10*60*1000)

                if(unsatisfiable):
                    print("The scenario is unsatisfiable.")
                    add2file(outputUnSatisfiable, resultat + '\n')
                elif(not unsatisfiable and (duration == '' or node == '' or nogood == '')):
                    add2file(outputUnSatisfiableError, resultat + '\n')
                else:
                    add2file(outputSatisfiable, f"{resultat};{duration};{node};{nogood}\n")
            except Exception as inst:
                add2file(outputUnSatisfiableTimeout, f"{resultat};{str(inst.args)}\n")
