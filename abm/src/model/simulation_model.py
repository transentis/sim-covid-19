from BPTK_Py import Model, Agent
from src.agents import Person

class SimulationModel(Model):
    def instantiate_model(self):
        self.grid = (20, 20)
        self.register_agent_factory(
            "person",
            lambda agent_id, model, properties: Person(agent_id, model, properties,agent_type="person")
        )