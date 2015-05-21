#coding: utf8
# gamelevel.py
from program import script

class GameLevel(object):
    
    def __init__(self, stage):
        self.stage = stage
        self.L = script.game.stage._colosseum_size(stage)
        self.stage_name = "STAGE %i"%stage if stage < script.game.stage_num else "LAST STAGE"
        self.enemy_num = script.game.stage._enemy_num(stage)
        self.types = script.game.stage._types_num(stage)
