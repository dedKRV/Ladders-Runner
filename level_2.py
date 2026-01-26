from base_level import BaseLevel
from enemy_config import LEVEL_2_ENEMIES, LEVEL_2_SPAWN, LEVEL_2_CARDS


class GameWindow2(BaseLevel):
    """Уровень 2"""

    def get_level_number(self):
        """Номер уровня"""
        return 2

    def get_tilemap_path(self):
        """Путь к тайлмапу уровня 2"""
        return "data/level_2.tmx"

    def get_spawn_position(self):
        """Позиция спавна игрока"""
        return LEVEL_2_SPAWN

    def get_enemy_config(self):
        """Конфигурация врагов"""
        return LEVEL_2_ENEMIES

    def get_cards_config(self):
        """Конфигурация карт"""
        return LEVEL_2_CARDS