import subprocess
import dzn_generator
import re
import os
from dzn_export import create_file


def add2file(path, content):
    with open(path, mode='a') as f:
        f.writelines(f"{content}\n")


def run_minizinc(model, scenario, output, timeout):

    parms = [
        'C:/Program Files/MiniZinc/minizinc.exe',
        '--solver', 
        'chuffed', 
        '-a', 
        '--verbose-solving', 
        '--solver-statistics', 
        '-f', 
        '--solver-time-limit', 
        str(timeout), 
        model, 
        scenario
    ]
    
    out, err = subprocess.Popen(parms, stdout=subprocess.PIPE, universal_newlines=True).communicate() 

    create_file(output, out)
  
    return out


def is_satisfiable(content):
    return not re.match('=====UNSATISFIABLE=====', content)


def is_timeout(content):
    return re.match('% Time limit exceeded!', content)


def parser(content):

    duration = re.search("%%%mzn-stat: time=(.*)\n", content).group(1)    
    nodes = re.search("%%%mzn-stat: nodes=(.*)\n", content).group(1)  
    nogoods = re.search("%%%mzn-stat: nogoods=(.*)\n", content).group(1)  

    return duration, nodes, nogoods


def run_all_models(id):
    pourcentage_nb_coach = 1 
    
    models = {
        "model_alldiff_regular": 95,
        "model_alldiff_sat": 95,
        "model_sums_regular": 60,
        "model_sums_sat": 60
    }
  
    scenario = dzn_generator.Scenario(seed=456) 
    scenarios = []
    
    for n_teams in range(5, max(models.values()), 5): 
                 
        p = 2 * n_teams
        v = 4
        t = n_teams
        c = int(n_teams * pourcentage_nb_coach)
        d = [5] * (n_teams // 5)                

        s = {
            "dzn": f"test_{id}/scenario_t{t}-p{p}-d{len(d)}-v{v}-c{c}.dzn",
            "name": f"t{t}-p{p}-d{len(d)}-v{v}-c{c}",
            "results": f"{t};{p};{len(d)};{v};{c}", 
            "n_teams": n_teams           
        }    

        random_scenario = scenario.generate_scenario("test", p, v, t, c, d) 
        dzn_generator.export(s["dzn"], random_scenario)             
        scenarios.append(s)
                
    for model in models:

         for s in scenarios:

            # We dont run all models because of time restrictions
            if s["n_teams"] > models[model]:
                continue

            txt_file = f"test_{id}/{model}-{s['name']}.txt"
            resultat = f"{model};{s['results']}"

            print("Model: " + resultat)

            try:
                out = run_minizinc(f"../models/{model}.mzn", s["dzn"], txt_file, 10*60*1000)

                if is_satisfiable:
                    duration, nodes, nogoods = parser(out)
                    add2file(f"test_{id}/satisfiable.out", f"{resultat};{duration};{nodes};{nogoods}")
                else :
                     add2file(f"test_{id}/un_satisfiable.out", f"{resultat}")
                    
            except Exception as e:
                add2file(f"test_{id}/timeout.out", f"{resultat};{str(e.args)}\n")


def run_models(id, models, scenario):

    models = [f for f in os.scandir(models)] 
    
    for model in models:
    
        try:
            out = run_minizinc(model.path, scenario, f"test_{id}/{model.name}_t", 10*60*1000)

            if is_satisfiable:
                duration, nodes, nogoods = parser(out)
                add2file(f"test_{id}/satisfiable.out", f"{model.name};{duration};{nodes};{nogoods}")
            else :
                    add2file(f"test_{id}/un_satisfiable.out", f"{model.name}")
                
        except Exception as e:
            add2file(f"test_{id}/timeout.out", f"{model.name};{str(e.args)}\n")


if __name__ == "__main__":
    
    run_all_models("bruno_3")
    #run_models("breaks", "../models/breaks", "../code/test_bruno/scenario_t50-p100-d10-v4-c50.dzn")
