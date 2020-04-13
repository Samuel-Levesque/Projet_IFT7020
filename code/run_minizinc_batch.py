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
        '-f',
        '-v', 
        '-t', 
        str(timeout), 
        model, 
        scenario
    ]
    out = subprocess.Popen(parms, stdout=subprocess.PIPE, universal_newlines=True).communicate() 
    create_file(output, out[0])
    return out[0]

def is_unsatisfiable(content):
    return "=====UNSATISFIABLE=====" in content


def parse_out(path, head, content):
      
    try:
        if is_unsatisfiable(content):
             add2file(f"{path}/un_satisfiable.out", f"{head}")

        if "%%%mzn-stat:" in content:
            duration = re.search("%%%mzn-stat: time=(.*)\n", content).group(1)    
            nodes = re.search("%%%mzn-stat: nodes=(.*)\n", content).group(1)  
            nogoods = re.search("%%%mzn-stat: nogoods=(.*)\n", content).group(1)  
            add2file(f"{path}/satisfiable.out", f"{head};{duration};{nodes};{nogoods}")
      
    except Exception as e:
        add2file(f"{path}/unknown.out", f"{head};{str(e.args)}\n")

   
def run_coaches(id, n_teams):

    scenarios = []

    for n_coaches in range(n_teams, n_teams - 20, -1):         
        scenario = dzn_generator.Scenario(seed=456) 
                    
        p = 2 * n_teams
        v = 4
        t = n_teams
        c = n_coaches
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

    
    run_scenarios(id, {"model_alldiff_regular" : 100}, scenarios)


def run_scenarios(id, models, scenarios):

    for model in models:        
        for s in scenarios:
           # We dont run all models because of time restrictions
            if s["n_teams"] > models[model]:
                continue

            txt_file = f"test_{id}/{model}-{s['name']}.txt"
            resultat = f"{model};{s['results']}"
            print("Model: " + resultat)
            out = run_minizinc(f"../models/{model}.mzn", s["dzn"], txt_file, 10*60*1000)
            parse_out(f"test_{id}", model, out)


def run_all_models(id, scenarios_gen):
    models = {
        "model_alldiff_regular": 95,
        "model_alldiff_sat": 95,
        "model_sums_regular": 60,
        "model_sums_sat": 60
    }

    scenarios = []
    
    for n_teams in range(5, max(models.values()), 5):          
        scenario = dzn_generator.Scenario(seed=456) 
                    
        p = 2 * n_teams
        v = 4
        t = n_teams
        c = n_teams
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

    run_scenarios(id, models, scenarios)
           

def run_models(id, models, scenario):
    models = [f for f in os.scandir(models)] 
    for model in models:
        out = run_minizinc(model.path, scenario, f"test_{id}/{model.name}_t", 10*60*1000)
        parse_out(f"test_{id}", model.name, out)
    

def run_model_scenario(id, model, scenario):
    base = os.path.basename(model)
    name = os.path.splitext(base)[0]
    out = run_minizinc(model, scenario, f"test_{id}/{name}.txt", 10*60*1000)
    parse_out(f"test_{id}", model, out)
  
if __name__ == "__main__":
    #run_all_models("4")
    #run_models("test", "models/auto.mzn", "test.dzn")
    #run_model_scenario(5, "../models/model_sums_sat.mzn", "test_test_4/scenario_t50-p100-d10-v4-c50.dzn")
    run_coaches(4, 50)
