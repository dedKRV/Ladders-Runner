import arcade
from core import MUSIC_VOLUME, SFX_VOLUME


class Music:
    """Добавление музыки и звуковых эффектов"""

    def __init__(self):
        """Инициализация менеджера музыки"""
        self.menu_music_sound = None
        self.battle_music_sound = None
        self.menu_music_player = None
        self.battle_music_player = None

        self.current_music = None

        # Звуковые эффекты
        self.shoot_sound = None
        self.player_dead_sound = None

        # Загрузка музыки
        self.menu_music_sound = arcade.load_sound("assets/sounds/1/Music/Game_menu_theme_loopable.wav")
        self.battle_music_sound = arcade.load_sound("assets/sounds/1/Music/Battle_theme_loopable.wav")


        # Загрузка звуковых эффектов
        self.shoot_sound = arcade.load_sound("assets/sounds/2/Sounds/Blaster laser.wav")
        self.player_dead_sound = arcade.load_sound("assets/sounds/2/Sounds/Dead1.wav")

    def play_menu_music(self):
        """Запустить музыку меню"""
        if self.current_music == "menu" and self.menu_music_player:
            return
        self.stop_all()
        if self.menu_music_sound:
            self.menu_music_player = arcade.play_sound(
                self.menu_music_sound,
                volume=MUSIC_VOLUME,
                loop=True
            )
            self.current_music = "menu"

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
        if self.menu_music_player:
            arcade.stop_sound(self.menu_music_player)
            self.menu_music_player = None

        if self.battle_music_player:
            arcade.stop_sound(self.battle_music_player)
            self.battle_music_player = None

        self.current_music = None

    def set_volume(self, volume):
        vol = max(0.0, min(1.0, volume))
        if self.menu_music_player:
            self.menu_music_player.volume = vol
        if self.battle_music_player:
            self.battle_music_player.volume = vol

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

    def play_shoot(self):
        """Звук выстрела игрока"""
        if self.shoot_sound:
                arcade.play_sound(self.shoot_sound, volume=SFX_VOLUME)

    def play_player_dead(self):
        """Звук смерти игрока"""
        if self.player_dead_sound:
            try:
                arcade.play_sound(self.player_dead_sound, volume=SFX_VOLUME + 0.3)
            except Exception as e:
                print(f"Ошибка звука смерти: {e}")