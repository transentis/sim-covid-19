from flask import Flask, redirect, url_for, request
import BPTK_Py
import pandas as pd
from BPTK_Py import Model
from BPTK_Py import sd_functions as sd

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
normal_contact_rate=model.constant("normal_contact_rate") # the average contact rate between people in "normal" times
duration = model.constant("duration") # the average time it takes to recover from the virus

intensive_available = model.constant("intensive_available") # the number of intensive care units available
intensive_percentage = model.constant("intensive_percentage") # the fraction of people needing intensive care

dashboard_on=model.constant("dashboard_on") # should be equal to 1.0 for dashboard scenario and 0.0 otherwise
distancing_on=model.constant("distancing_on") # defines whether social distancing is on within an interactive scenario
distancing_contact_rate=model.constant("distancing_contact_rate") # interactive scenario: the contact rate when practicing social distancing
distancing_begin=model.constant("distancing_begin") # interactive scenario: when to begin social distancing
distancing_duration=model.constant("distancing_duration")# interactive scenario: when social distancing ends and we return to normal behavior

total_population = model.converter("total_population") # the total population, i.e the sum of susceptible, infected and recovered
contact_rate = model.converter("contact_rate") # the rate at which people are being contacted, in all scenarios

intensive_needed = model.converter("intensive_needed") # the number of intensive care units needed at any time

contact_number = model.converter("contact_number") #  measures which fraction of a susceptible population is infected by a contagious person
reproduction_rate = model.converter("reproduction_rate") # measures the rate at which an epidemic reproduces

variable_contact_rate=model.converter("variable_contact_rate") # the variable contact rate used in the detailed scenarios
dashboard_with_distancing_contact_rate=model.converter("dashboard_with_distancing_contact_rate") # the contact rate used in interactive scenarios with distancing on
dashboard_contact_rate=model.converter("dashboard_contact_rate") # the contact rate used in interactive scenarios with distancing off

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

contact_rate.equation=20

contact_rate.equation=dashboard_on*dashboard_contact_rate+(-dashboard_on+1.0)*variable_contact_rate
dashboard_on.equation=1.0
distancing_on.equation=0.0
dashboard_contact_rate.equation=distancing_on*dashboard_with_distancing_contact_rate+(-distancing_on+1.0)*normal_contact_rate
dashboard_with_distancing_contact_rate.equation=sd.If(sd.Or(sd.time()<distancing_begin,sd.time()>distancing_begin+distancing_duration),normal_contact_rate,distancing_contact_rate)
normal_contact_rate.equation=20.0
distancing_contact_rate.equation=2.0
distancing_begin.equation=20.0
distancing_duration.equation=200.0

variable_contact_rate.equation=sd.lookup(sd.time(),"variable_contact_rate")

variable_contact_rate_points = [[0,20.0],[1500,20.0]]

model.points["variable_contact_rate"]=variable_contact_rate_points

bptk = BPTK_Py.bptk()
bptk.register_model(model)
bptk.register_scenario_manager({"smSir":{"model":model}})
bptk.register_scenarios(
    scenarios ={
        "dashboard":{}
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
        return '{"error": "please pass the request with content-type application/json"}'
        
    content = request.get_json()
    
    try:
        settings = content["settings"]

        for scenario_manager_name, scenario_manager_data in settings.items():
            for scenario_name, scenario_settings in scenario_manager_data.items():
                scenario = bptk.get_scenario(scenario_manager_name,scenario_name)
                constants = scenario_settings["constants"]
                for constant_name, constant_settings in constants.items():
                    scenario.constants[constant_name]=constant_settings                   
                    
    except KeyError:
        application.logger.info("Settings not specified")
        pass
    
    try:
        scenario_managers=content["scenario_managers"]
    except KeyError:
        return '{"error": "expecting scenario_managers to be set"}'
    
    try:
        scenarios=content["scenarios"]
    except KeyError:
        return '{"error": "expecting scenario_managers to be set"}'
        
    try:
        equations=content["equations"]
    except KeyError:
        return '{"error": "expecting equations to be set"}'
      
        
    result = bptk.plot_scenarios(
          scenario_managers=scenario_managers,
          scenarios=scenarios,
          equations=equations,
          return_df=True
        )
       
    if result is not None:
        return result.to_json()
    else:
        return '{"error": "no data was return from simulation"}'

if __name__ == "__main__":
    application.debug = False
    application.run(host='0.0.0.0')    
