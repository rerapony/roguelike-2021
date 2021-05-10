from src.server.game.Engine import Engine


class BaseComponent:
    def __init__(self):
        self.entity_id = None

    def entity(self, engine: Engine):
        return engine.game_map.entities[self.entity_id]


class AttackComponent(BaseComponent):
    def __init__(self, hp: int, defense: int, attack: int):
        super().__init__()
        self.max_health = hp
        self.health = hp
        self.defense = defense
        self.attack = attack

    def update_hp(self, engine: Engine) -> None:

        if self.health == 0 and self.entity(engine).ai:
            self.die(engine)

    def die(self, engine: Engine) -> None:
        if self.entity_id in engine.game_map.players:
            death_message = "You died!"
        else:
            death_message = f"Monster is dead!"

        self.entity.char = "%"
        self.entity.blocks_movement = False
        self.entity.ai = None

        print(death_message)
