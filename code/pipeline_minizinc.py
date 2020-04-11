import run_minizinc_batch as batch
import dzn_generator as generator
import dzn_export as export
from os.path import join, exists

def n_teams_per_division(n_teams, nb_teams_by_division):
    nb_division = int(n_teams//nb_teams_by_division)
    last_division = n_teams % nb_teams_by_division
    division = []
    for i in range(nb_division):
        division.append(nb_teams_by_division)
    if(last_division != 0):
        division.append(last_division)

    return division

def nb_coaches(n_teams, pourcentage_nb_coach):
    n_coach = int(n_teams*pourcentage_nb_coach)
    if(n_teams == 0):
        return 1
    else: return n_coach

def createScenario(n_periods, n_venues, n_teams, pourcentage_nb_coach, nb_teams_by_division, model):
    return {
                "name" : "toy",
                "n_periods" : n_periods,
                "n_venues" : n_venues,
                "n_teams": n_teams,
                "n_coaches": nb_coaches(n_teams, pourcentage_nb_coach),
                "n_teams_per_division" : n_teams_per_division(n_teams, nb_teams_by_division),
                "break_duration" : 2,
                "model" : join('models', model + '.mzn')
            }

if __name__ == "__main__":
    #models = ["auto", "model_alldiff_regular", "model_alldiff_sat", "model_sums_regular", "model_sums_sat"]
    models = ["model_alldiff_regular", "model_alldiff_sat", "model_sums_regular", "model_sums_sat"]
    scenarios = []
    # for model in models:
    #     for p in range(4, 41, 2):
    #         for v in range(4, 11, 2):
    #             for t in range(5, 56, 5):
    #                 scenarios.append(createScenario(p, v, t, model))

    #createScenario(n_periods, n_venues, n_teams, pourcentage_nb_coach, nb_teams_by_division, model)
    #scenarios.append(createScenario(40, 20, 60, 1, 5, models[1]))
    #scenarios.append(createScenario(4, 4, 8, 1, 2, models[1]))

    for model in models:
        for p in range(4, 41, 2):
            for t in range(5, 21, 5):
                scenarios.append(createScenario(p, 4, t, 1, 5, model))

    scenario = generator.Scenario(seed=456) 

    for s in scenarios:

        n = s["name"]
        p = s["n_periods"]
        v = s["n_venues"]
        t = s["n_teams"]
        c = s["n_coaches"]
        d = s["n_teams_per_division"]
        b = s["break_duration"]
        
        resultName = str(n) + '-' + str(p) + '-' + str(v) + '-' + str(t) + '-' + str(c) + '-' + str(d) + '-' + str(b)
        dzn_file = join('test', resultName + '.dzn')

        #print(resultName)
        #if(True):
        if(exists(dzn_file)):
            print('Already processed : ' + dzn_file)
        else:
            random_scenario = scenario.generate_scenario(n, p, v, t, c, d) 
            export.export(dzn_file, random_scenario)

            s1 = f"Q = {b+2} and replace the DFA for:\n"
            s1 += scenario.generate_dfa(b)
            export.create_file("dfa.mzn", s1)

            outputSatisfiable = "outputSatisfiable.csv"
            outputUnSatisfiable = "outputUnSatisfiable.csv"
            outputUnSatisfiableTimeout = "outputUnSatisfiableTimeout.csv"
            outputUnSatisfiableError = "outputUnSatisfiableError.csv"

            resultat = s["model"] + ';' + str(n) + ';' + str(p) + ';' + str(v) + ';' + str(t) + ';' + str(c) + ';"' + str(d) + '";' + str(b)
            print("Trying : " + resultat)

            try:
                unsatisfiable, stringtime, stringnode, stringnogood = batch.excuteMinizinc(s["model"], dzn_file, join('test', resultName + '.txt'), 10*60*1000)

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
