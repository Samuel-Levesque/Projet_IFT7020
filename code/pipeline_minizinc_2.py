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

    models = {
        "model_alldiff_regular": 80,
        "model_alldiff_sat": 80,
        "model_sums_regular": 55,
        "model_sums_sat": 55
    }
  
    scenario = generator.Scenario(seed=456) 

    for model in models:

         for n_teams in range(5, models[model], 5):
                
            p = 2 * n_teams
            v = 4
            t = n_teams
            c = int(n_teams * pourcentage_nb_coach)
            d = [5] * (n_teams // 5)                
            
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
