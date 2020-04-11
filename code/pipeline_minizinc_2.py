import run_minizinc_batch as batch
import dzn_generator as generator
import dzn_export as export
from os.path import join, exists

if __name__ == "__main__":
    
    pourcentage_nb_coach = 0.95 
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
            
            dzn_file = f"test/{n}-{model}-{p}-{v}-{t}-{c}-{d}-{b}.dzn"
            result_file = f"test/{n}-{model}-{p}-{v}-{t}-{c}-{d}-{b}.txt"

            random_scenario = scenario.generate_scenario(n, p, v, t, c, d) 
            export.export(dzn_file, random_scenario)
          
            outputSatisfiable = "satisfiable.out"
            outputUnSatisfiable = "un_satisfiable.out"
            outputUnSatisfiableTimeout = "timeout.out"
            outputUnSatisfiableError = "error.out"

            resultat = f"{model};{n};{p};{v};{t};{c};{d};{b}"
            print("Trying : " + resultat)

            try:
                unsatisfiable, stringtime, stringnode, stringnogood = batch.excuteMinizinc(f"models/{model}.mzn", dzn_file, result_file, 10*60*1000)

                if(unsatisfiable):
                    print("The scenario is unsatisfiable.")
                    resultat = resultat + '\n'
                    with open(outputUnSatisfiable, mode='a') as f:
                        f.writelines(resultat)
                elif(not unsatisfiable and(stringtime == '' or stringnode == '' or stringnogood == '')):
                    resultat = resultat + '\n'
                    with open(outputUnSatisfiableError, mode='a') as f:
                        f.writelines(resultat)
                else:
                    resultat = resultat + ';' + stringtime + ';' + stringnode + ';' + stringnogood + '\n'
                    with open(outputSatisfiable, mode='a') as f:
                        f.writelines(resultat)
            except Exception as inst:
                resultat = resultat + ';' + str(inst.args) + '\n'
                with open(outputUnSatisfiableTimeout, mode='a') as f:
                        f.writelines(resultat)
