from base_level import BaseLevel
from enemy_config import LEVEL_3_ENEMIES, LEVEL_3_SPAWN, LEVEL_3_CARDS


class GameWindow3(BaseLevel):
    """Уровень 3"""

    def get_level_number(self):
        """Номер уровня"""
        return 3

    def get_tilemap_path(self):
        """Путь к тайлмапу уровня 3"""
        return "data/level_3.tmx"

    def get_spawn_position(self):
        """Позиция спавна игрока"""
        return LEVEL_3_SPAWN

    def get_enemy_config(self):
        """Конфигурация врагов"""
        return LEVEL_3_ENEMIES

    def get_cards_config(self):
        """Конфигурация карт"""
        return LEVEL_3_CARDS