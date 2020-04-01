from BPTK_Py import Agent, Event
import numpy as np


class Person(Agent):
    STATES = ["HEALTHY", "INFECTED"]
    MOVING_LIST = [[0, 0], [0, -1], [0, 1], [-1, 0], [1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]

    def initialize(self):
        self.state = np.random.choice(self.STATES, p=[0.9, 0.1])
        self.register_event_handler(["HEALTHY","INFECTED"], "infection", self.handle_infection_event)

        # found = False
        #
        # while not found:
        #     foundOne = False
        #     position =(np.random.randint(20),np.random.randint(20))
        #     for agent in self.model.agents:
        #         if agent == self:
        #             continue
        #         if agent.position == position:
        #             foundOne = True
        #             break
        #     if not foundOne:
        #         found = True
        # self.position = position


    def handle_infection_event(self,event):
        self.state = "INFECTED"
        self.infected = 1

    def act(self,time,round_no, step_no):
        if self.state == "HEALTHY":
            pass
            #print(self.position)
            #self.move()
            #print(self.position)
            #neighbors = self.find_neighbors()
            #self.check_infected(neighbors)
        elif self.state == "INFECTED":
            event_factory = lambda agent_id: Event("infection", self.id, agent_id, data=None)
            self.model.random_events("person", 20, event_factory)



    # def move(self):
    #     position_found = 0
    #     found = False
    #     while not found:
    #         indices = [i for i in range(0, len(self.MOVING_LIST))]
    #         moving = self.MOVING_LIST[np.random.choice(indices)]
    #         position_found = (self.position[0]+moving[0], self.position[1]+moving[1])
    #         if position_found[0] >= 0 and position_found[0]<=20 and \
    #             position_found[1] >= 0 and position_found[1] <=20:
    #             found = True
    #             break
    #
    #     self.position = position_found
    #
    # def find_neighbors(self):
    #      position = 0
    #      neighbors_list = []
    #      for moving_element in self.MOVING_LIST:
    #          position = (self.position[0]+moving_element[0], self.position[1]+moving_element[1])
    #          for agent in self.model.agents:
    #              if agent == self:
    #                  continue
    #              if agent.position == position:
    #                  neighbors_list.append(agent.position)
    #      return neighbors_list
    #
    # def check_infected(self, neighbors):
    #      for agent in self.model.agents:
    #          if agent == self:
    #              continue
    #          if agent.position in neighbors:
    #              if agent.state == "INFECTED":
    #                  self.state = "INFECTED"
    #                  self.model.infected += 1
    #                  print("Waaah I got infected")
    #                  self.infected =  1
    #                  break
    #
    # def infect_neighbors(self,neighbors):
    #     for agent in self.model.agents:
    #         if agent == self:
    #             continue
    #         if agent.position in neighbors:
    #             agent.state = "INFECTED"



