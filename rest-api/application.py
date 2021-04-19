from flask import Flask, redirect, url_for, request, make_response, jsonify
import BPTK_Py
import pandas as pd
from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
import json

application = Flask(__name__)

model = Model(starttime=1.0,stoptime=1500.0,dt=1.0,name='COVID Simulation Model')

susceptible = model.stock("susceptible")  # those that have not been infected yet
infectious = model.stock("infectious") # those that are currently carrying an infection
recovered = model.stock("recovered") # those that have recovered from an infection
deceased = model.stock("deceased") # those that have died from the infection

infection_rate = model.flow("infection_rate") # the rate at which people are becoming infected
recovery_rate = model.flow("recovery_rate") # the rate at which people are recovering from an infection
death_rate = model.flow("death_rate") # the rate at which people are dying from an infection

infectivity = model.constant("infectivity") # the infectivity of the corona virus
lethality = model.constant("lethality") # the lethality of the corona virus
duration = model.constant("duration") # the average time it takes to recover from the virus

intensive_available = model.constant("intensive_available") # the number of intensive care units available
intensive_percentage = model.constant("intensive_percentage") # the fraction of people needing intensive care


total_population = model.converter("total_population") # the total population, i.e the sum of susceptible, infected and recovered
contact_rate = model.converter("contact_rate") # the rate at which people are being contacted, in all scenarios

intensive_needed = model.converter("intensive_needed") # the number of intensive care units needed at any time

contact_number = model.converter("contact_number") #  measures which fraction of a susceptible population is infected by a contagious person
reproduction_rate = model.converter("reproduction_rate") # measures the rate at which an epidemic reproduces


susceptible.initial_value = 80000000.0
infectious.initial_value = 120.0
recovered.initial_value = 0.0
deceased.initial_value = 0.0

infectivity.equation = 0.02
duration.equation = 20.0
lethality.equation = 0.001

intensive_percentage.equation = 0.002
intensive_available.equation = 30000.0
intensive_needed.equation =infectious*intensive_percentage

susceptible.equation = -infection_rate
infectious.equation = infection_rate - recovery_rate - death_rate
recovered.equation = recovery_rate
deceased.equation = death_rate

total_population.equation = susceptible+infectious+recovered

infection_rate.equation = (contact_rate*infectivity*infectious)*(susceptible/total_population)

recovery_rate.equation = infectious/duration

death_rate.equation = infectious*lethality

contact_number.equation=contact_rate*infectivity*duration
reproduction_rate.equation=contact_number*(susceptible/total_population)

contact_rate.equation=sd.lookup(sd.time(),"contact_rate_table")


contact_rate_table = [[0,20.0],[1500,20.0]]

model.points["contact_rate_table"]=contact_rate_table

bptk = BPTK_Py.bptk()
bptk.register_model(model)
bptk.register_scenario_manager({"smSir":{"model":model}})
bptk.register_scenarios(
    scenarios ={
        "dashboard":{},
        "base":{},
        "strong_social_distancing":{
            "points":{
                "contact_rate_table":[
                    [0,20.0],
                    [25,10.0],
                    [41,5.0],
                    [500,10.0],
                    [1200,20.0],
                    [1500,20.0]
                ]
            }
        },
        "weak_social_distancing":{
            "points":{
                "contact_rate_table":[
                    [0,20.0],
                    [10,2],
                    [100,20],
                    [1500,20.0]
                ]
            }
        }
    },
    scenario_manager="smSir")


bptk.reset_simulation_model(scenario_manager="smSir", scenario="dashboard")

# rest API

@application.route('/', methods=['GET'])
def home():
    return "<h1>BPTK-Py Simulation Service</h1>"

@application.route('/run', methods=['POST','PUT'])
def run():
    application.logger.info("Request is JSON: {}".format(request.is_json))
    application.logger.info("Request is JSON: {}".format(request.data))
    
    if not request.is_json:
        resp = make_response('{"error": "please pass the request with content-type application/json"}',500)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp
        
    content = request.get_json()
    
    try:
        settings = content["settings"]

        for scenario_manager_name, scenario_manager_data in settings.items():
            for scenario_name, scenario_settings in scenario_manager_data.items():
                scenario = bptk.get_scenario(scenario_manager_name,scenario_name)
                constants = scenario_settings["constants"]
                for constant_name, constant_settings in constants.items():
                    scenario.constants[constant_name]=constant_settings
                points = scenario_settings["points"]
                for points_name, points_settings in points.items():
                    scenario.points[points_name]=points_settings
                bptk.reset_simulation_model(scenario_manager=scenario_manager_name,scenario=scenario_name)
                    
    except KeyError:
        application.logger.info("Settings not specified")
        pass
    
    try:
        scenario_managers=content["scenario_managers"]
    except KeyError:
        resp = make_response('{"error": "expecting scenario_managers to be set"}',500)
        resp.headers['Content-Type']='application/json'
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp
    
    try:
        scenarios=content["scenarios"]
    except KeyError:
        resp = make_response('{"error": "expecting scenario_managers to be set"}',500)
        resp.headers['Content-Type']='application/json'
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp
        
    try:
        equations=content["equations"]
    except KeyError:
        resp = make_response('{"error": "expecting equations to be set"}',500)
        resp.headers['Content-Type']='application/json'
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp
      
        
    result = bptk.plot_scenarios(
          scenario_managers=scenario_managers,
          scenarios=scenarios,
          equations=equations,
          return_df=True
        )
       
    if result is not None:
        resp = make_response(result.to_json(), 200)
    else:
        resp = make_response('{"error": "no data was returned from simulation"}', 500)

    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

@application.route('/scenarios', methods=['GET'])
def scenarios():
    scenarions = []
    for scenario in bptk.get_scenarios():
        scenarions.append(scenario)
    scenarions = jsonify(scenarions)
    
    if scenarions is not None:
        resp = make_response(scenarions, 200)
    else:
        resp = make_response('{"error": "no data was returned from simulation"}', 500)
        
    return resp
@application.route('/equations', methods=['GET'])

def equations():
    equations_names = {}

    stock_names = []
    for key, value in model.stocks.items():
        stock_names.append(key)

    flows_names = []
    for key, value in model.flows.items():
        flows_names.append(key)

    constants_names = []
    for key, values in model.constants.items():
        constants_names.append(key)

    points_names = []
    for key, values in model.points.items():
        points_names.append(key)
    
    equations_names["stocks"] = [name for name in stock_names]
    equations_names["flows"] = [name for name in flows_names]
    equations_names["constants"] = [name for name in constants_names]
    equations_names["points"] = [name for name in points_names]
    
    if equations_names is not None:
        resp = make_response(equations_names, 200)
    else:
        resp = make_response('{"error": "no data was returned from simulation"}', 500)
        
    return resp


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')    
