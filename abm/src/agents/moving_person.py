from BPTK_Py import Agent, Event
import numpy as np

class MovingPerson(Agent):
    STATES = ["HEALTHY", "INFECTED_LIGHT", "INFECTED_HARD", "DEAD", "RECOVERED"]
    MOVING_LIST = [[0, 0], [0, -1], [0, 1], [-1, 0], [1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]

    def initialize(self):
        self.state = np.random.choice(self.STATES, p=[0.8, 0.16, 0.04, 0, 0])
        self.register_event_handler(self.STATES, "infection_hard", self.handle_infection_hard_event)
        self.register_event_handler(self.STATES, "infection_light",
                                    self.handle_infection_light_event)

        found = False

        while not found:
            foundOne = False
            position =(np.random.randint(20),np.random.randint(20))
            for agent in self.model.agents:
                if agent == self:
                    continue
                if agent.position == position:
                    foundOne = True
                    break
            if not foundOne:
                found = True
        self.position = position

    def handle_infection_hard_event(self, event):
        if self.state == "HEALTHY":
            self.state = "INFECTED_HARD"

    def handle_infection_light_event(self, event):
        if self.state == "HEALTHY":
            self.state = "INFECTED_LIGHT"

    def act(self, time, round_no, step_no):
        if self.state == "HEALTHY":
            self.move()
        elif self.state == "DEAD":
            pass
        elif self.
        if self.state == "INFECTED_LIGHT":
            # or self.state == "INFECTED_HARD":
            infected_contacts = 0
            for i in range(0, self.model.contact_rate):
                if np.random.choice(["HEALTHY", "INFECTED"], p=[1 - self.model.infectivity, self.model.infectivity]) \
                        == "INFECTED":
                    infected_contacts += 1
            self.infected = infected_contacts
            infected_light = round(0.8 * infected_contacts)
            infected_hard = round(0.2 * infected_contacts)
            event_factory_hard = lambda agent_id: Event("infection_hard", self.id, agent_id, data=None)
            event_factory_light = lambda agent_id: Event("infection_light", self.id, agent_id, data=None)
            self.model.random_events("person", infected_hard, event_factory_hard)
            self.model.random_events("person", infected_light, event_factory_light)

    def move(self):
        position_found = 0
        found = False
        while not found:
            indices = [i for i in range(0, len(self.MOVING_LIST))]
            moving = self.MOVING_LIST[np.random.choice(indices)]
            position_found = (self.position[0]+moving[0], self.position[1]+moving[1])
            if position_found[0] >= 0 and position_found[0]<=20 and \
                position_found[1] >= 0 and position_found[1] <=20:
                found = True
                break

        self.position = position_found

    def find_neighbors(self):
         position = 0
         neighbors_list = []
         for moving_element in self.MOVING_LIST:
             position = (self.position[0]+moving_element[0], self.position[1]+moving_element[1])
             for agent in self.model.agents:
                 if agent == self:
                     continue
                 if agent.position == position:
                     neighbors_list.append(agent.position)
         return neighbors_list

    def check_infected(self, neighbors):
         for agent in self.model.agents:
             if agent == self:
                 continue
             if agent.position in neighbors:
                 if agent.state == "INFECTED":
                     self.state = "INFECTED"
                     self.model.infected += 1
                     print("Waaah I got infected")
                     self.infected =  1
                     break

    def infect_neighbors(self,neighbors):
        for agent in self.model.agents:
            if agent == self:
                continue
            if agent.position in neighbors:
                agent.state = "INFECTED"



