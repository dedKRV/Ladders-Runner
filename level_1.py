from base_level import BaseLevel
from enemy_config import LEVEL_1_ENEMIES, LEVEL_1_SPAWN, LEVEL_1_CARDS


class GameWindow(BaseLevel):
    """Уровень 1"""

    def get_level_number(self):
        """Номер уровня"""
        return 1

    def get_tilemap_path(self):
        """Путь к тайлмапу уровня 1"""
        return "data/level_1.tmx"

    def get_spawn_position(self):
        """Позиция спавна игрока"""
        return LEVEL_1_SPAWN

    def get_enemy_config(self):
        """Конфигурация врагов"""
        return LEVEL_1_ENEMIES

    def get_cards_config(self):
        """Конфигурация карт"""
        return LEVEL_1_CARDS