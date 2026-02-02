from base_level import BaseLevel
from enemy_config import LEVEL_5_ENEMIES, LEVEL_5_SPAWN, LEVEL_5_CARDS

class GameWindow5(BaseLevel):
    """Уровень 5"""

    def get_level_number(self):
        """Номер уровня"""
        return 5

    def get_tilemap_path(self):
        """Путь к тайлмапу уровня 5"""
        return "data/level_5.tmx"

    def get_spawn_position(self):
        """Позиция спавна игрока"""
        return LEVEL_5_SPAWN

    def get_enemy_config(self):
        """Конфигурация врагов"""
        return LEVEL_5_ENEMIES

    def get_cards_config(self):
        """Конфигурация карт"""
        return LEVEL_5_CARDS