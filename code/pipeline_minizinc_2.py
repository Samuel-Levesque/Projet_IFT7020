import run_minizinc_batch_2 as batch
import dzn_generator as generator
import dzn_export as export
from os.path import join, exists

def add2file(path, content):
    with open(path, mode='a') as f:
        f.writelines(f"{content}\n")

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
            
            test_path = f"test_{id}/{model}-t{t}-p{p}-d{len(d)}-v{v}-c{c}"
            dzn_file = f"{test_path}.dzn"
            result_file = f"{test_path}.txt"

            random_scenario = scenario.generate_scenario("test", p, v, t, c, d) 
            export.export(dzn_file, random_scenario)
          
            outputUnSatisfiable = f"test_{id}/un_satisfiable.out"
            outputUnSatisfiableError = f"test_{id}/error.out"

            resultat = f"{model};{t};{p};{len(d)};{v};{c}"
            print("Model: " + resultat)

            try:
                unsatisfiable, duration, node, nogood = batch.excuteMinizinc(f"../models/{model}.mzn", dzn_file, result_file, 10*60*1000)
               
                if not unsatisfiable:
                    add2file(f"test_{id}/satisfiable.out", f"{resultat};{duration};{node};{nogood}")
                else :
                     add2file(f"test_{id}/timeout.out", f"{resultat}")
                    
            except Exception as inst:
                add2file(f"test_{id}/timeout.out", f"{resultat};{str(inst.args)}\n")
