import run_minizinc_batch as batch
import dzn_generator as generator
import dzn_export as export
from os.path import join

if __name__ == "__main__":
        # scenarios = [
    #     {
    #         "name" : "toy",
    #         "n_periods" : 50,
    #         "n_venues" : 6,
    #         "n_teams": 30,
    #         "n_coaches": 25,
    #         "n_teams_per_division" : [5, 5, 5, 5, 5, 5],
    #         "break_duration" : 10
    #     }]
    scenarios = [
        {
            "name" : "toy",
            "n_periods" : 4,
            "n_venues" : 3,
            "n_teams": 6,
            "n_coaches": 5,
            "n_teams_per_division" : [3, 3],
            "break_duration" : 10
        }]
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

        #print(resultName)
        random_scenario = scenario.generate_scenario(n, p, v, t, c, d) 
        export.export(resultName + ".dzn", random_scenario)

        batch.excuteMinizinc(join('models', 'model2.mzn'), join(resultName + '.dzn'), resultName + '.txt')

        s1 = f"Q = {b+2} and replace the DFA for:\n"
        s1 += scenario.generate_dfa(b)
        export.create_file("dfa.mzn", s1)