import arcade
from core import *


class MainMenu:
    """Главное меню игры"""

    def __init__(self, database):
        self.database = database

        # Загружаем тайлмап для фона меню
        self.menu_map = arcade.load_tilemap("data/menu.tmx", scaling=TILE_SCALING)
        self.background_list = self.menu_map.sprite_lists.get('Слой тайлов 1', arcade.SpriteList())

        # Загружаем кастомный шрифт
        self.font_name = "assets/ui_textures/10 Font/CyberpunkCraftpixPixel.otf"

        # Позиции элементов
        self.title_y = 520
        self.resume_button_y = 385
        self.restart_button_y = 290

        # Размеры кнопок (для hitbox)
        self.button_width = 250
        self.button_height = 90

    def draw(self):
        """Отрисовка главного меню"""
        # Фон
        if self.background_list:
            self.background_list.draw()

        # Заголовок СВЕРХУ
        arcade.draw_text(
            "LADDERS RUNNER",
            SCREEN_WIDTH / 2,
            self.title_y,
            arcade.color.WHITE,
            font_size=32,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name,
            bold=True
        )

        # Проверяем наличие сохранений
        from config_gun import get_level_choice
        current_level = get_level_choice()
        has_save = self.database.has_save_for_level(current_level)

        # Надпись RESUME (только если есть сохранение)
        if has_save:
            arcade.draw_text(
                "RESUME",
                SCREEN_WIDTH / 2,
                self.resume_button_y,
                arcade.color.WHITE,
                font_size=24,
                anchor_x="center",
                anchor_y="center",
                font_name=self.font_name
            )

        # Надпись RESTART
        arcade.draw_text(
            "RESTART",
            SCREEN_WIDTH / 2,
            self.restart_button_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )

    def check_click(self, x, y):
        """Проверка клика по кнопкам"""
        from config_gun import get_level_choice
        current_level = get_level_choice()
        has_save = self.database.has_save_for_level(current_level)

        # Проверка Resume
        if has_save and self._point_in_button(x, y, self.resume_button_y):
            return "resume"

        # Проверка Restart
        if self._point_in_button(x, y, self.restart_button_y):
            return "restart"

        return None

    def _point_in_button(self, x, y, button_y):
        """Проверка попадания точки в кнопку"""
        center_x = SCREEN_WIDTH / 2
        return (center_x - self.button_width / 2 <= x <= center_x + self.button_width / 2 and
                button_y - self.button_height / 2 <= y <= button_y + self.button_height / 2)


class PauseMenu:
    """Меню паузы"""

    def __init__(self):
        self.pause_map = arcade.load_tilemap("data/pause.tmx", scaling=TILE_SCALING)
        self.background_list = self.pause_map.sprite_lists.get('Слой тайлов 1', arcade.SpriteList())

        # Смещение для выравнивания по центру
        self.offset_x = 150
        self.offset_y = 0
        # Кнопка Exit (слева)
        self.exit_hitbox = {
            'min_x': 200 + self.offset_x,
            'max_x': 350 + self.offset_x,
            'min_y': 300 + self.offset_y,
            'max_y': 480 + self.offset_y
        }

        # Кнопка Resume (по центру)
        self.resume_hitbox = {
            'min_x': 410 + self.offset_x,
            'max_x': 550 + self.offset_x,
            'min_y': 300 + self.offset_y,
            'max_y': 480 + self.offset_y
        }

        # Кнопка Restart (справа)
        self.restart_hitbox = {
            'min_x': 610 + self.offset_x,
            'max_x': 760 + self.offset_x,
            'min_y': 300 + self.offset_y,
            'max_y': 480 + self.offset_y
        }

    def draw(self):
        """Отрисовка меню паузы"""
        # Смещаем все спрайты для центрирования
        for sprite in self.background_list:
            sprite.center_x += self.offset_x
            sprite.center_y += self.offset_y
        # Фон
        if self.background_list:
            self.background_list.draw()

        for sprite in self.background_list:
            sprite.center_x -= self.offset_x
            sprite.center_y -= self.offset_y

    def check_click(self, x, y):
        """Проверка клика по кнопкам, возвращает действие"""
        if self._point_in_hitbox(x, y, self.resume_hitbox):
            return "resume"

        elif self._point_in_hitbox(x, y, self.exit_hitbox):
            return "exit"

        elif self._point_in_hitbox(x, y, self.restart_hitbox):
            return "restart"

        return None

    def _point_in_hitbox(self, x, y, hitbox):
        """Проверка попадания точки в hitbox"""
        return (hitbox['min_x'] <= x <= hitbox['max_x'] and
                hitbox['min_y'] <= y <= hitbox['max_y'])


class UI:
    def __init__(self):
        pass