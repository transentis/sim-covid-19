from flask import Flask, redirect, url_for, request, make_response, jsonify
import BPTK_Py
import pandas as pd
from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
import json

from BPTK_Py.server import BptkServer


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
bptk.register_model(model,"smSir")
bptk.register_scenarios(
    scenarios ={
        "dashboard":{},
        "base":{},
        "strong_social_distancing":{
            "points":{
                "contact_rate_table":[
                    [0,20.0],
                    [100,2.0],
                    [1100,2.0],
                    [1200,20.0],
                    [1500,20.0]
                ]
            }
        },
        "weak_social_distancing":{
            "points":{
                "contact_rate_table":[
                    [0,20.0],
                    [100,15.0],
                    [120,10.0],
                    [140,5.0],
                    [160,2.0],
                    [400,2.0],
                    [500,20.0],
                    [1500,20.0]
                ]
            }
        }
    },
    scenario_manager="smSir")


bptk.reset_simulation_model(scenario_manager="smSir", scenario="dashboard")

# Calling the BptkServer class
application = BptkServer(__name__, bptk) 

if __name__ == "__main__":
    application.run()