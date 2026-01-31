import arcade
from core import MUSIC_VOLUME

class Music:
    """Добавление музыки"""

    def __init__(self):
        """Инициализация менеджера музыки"""
        self.menu_music_sound = None
        self.battle_music_sound = None
        self.menu_music_player = None
        self.battle_music_player = None

        self.current_music = None
        try:
            self.menu_music_sound = arcade.load_sound("assets/sounds/1/Music/Game_menu_theme_loopable.wav")
            self.battle_music_sound = arcade.load_sound("assets/sounds/1/Music/Battle_theme_loopable.wav")
            print("Музыка успешно загружена!")
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")

    def play_menu_music(self):
        """Запустить музыку меню"""
        if self.current_music == "menu" and self.menu_music_player:
            return
        self.stop_all()
        if self.menu_music_sound:
            try:
                self.menu_music_player = arcade.play_sound(
                    self.menu_music_sound,
                    volume=MUSIC_VOLUME,
                    loop=True
                )
                self.current_music = "menu"
                print("Запущена музыка меню")
            except Exception as e:
                print(f"Ошибка воспроизведения музыки меню: {e}")

    def play_battle_music(self):
        """Запустить музыку игры"""
        if self.current_music == "battle" and self.battle_music_player:
            return
        self.stop_all()
        if self.battle_music_sound:
            self.battle_music_player = arcade.play_sound(
                self.battle_music_sound,
                volume=MUSIC_VOLUME,
                loop=True
            )
            self.current_music = "battle"

    def stop_all(self):
        """Остановить всю музыку"""
        try:
            if self.menu_music_player:
                arcade.stop_sound(self.menu_music_player)
                self.menu_music_player = None

            if self.battle_music_player:
                arcade.stop_sound(self.battle_music_player)
                self.battle_music_player = None

            self.current_music = None
        except Exception as e:
            print(f"Ошибка остановки музыки: {e}")

    def set_volume(self, volume):
        MUSIC_VOLUME = max(0.0, min(1.0, volume))
        if self.menu_music_player:
            self.menu_music_player.volume = MUSIC_VOLUME
        if self.battle_music_player:
            self.battle_music_player.volume = MUSIC_VOLUME

    def pause(self):
        """Приостановить музыку"""
        if self.menu_music_player:
            self.menu_music_player.pause()

        if self.battle_music_player:
            self.battle_music_player.pause()

    def resume(self):
        """Возобновить музыку"""
        if self.current_music == "menu" and self.menu_music_player:
            self.menu_music_player.play()
        elif self.current_music == "battle" and self.battle_music_player:
            self.battle_music_player.play()