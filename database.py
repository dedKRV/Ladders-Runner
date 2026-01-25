import sqlite3
from datetime import datetime


class GameDatabase:
    """Управление базой данных игры"""

    def __init__(self, db_file="game_save.db"):
        self.db_file = db_file
        self.create_tables()

    def connect(self):
        """Подключение к базе данных"""
        conn = sqlite3.connect(self.db_file, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        """Создание таблиц если их нет"""
        conn = self.connect()
        cursor = conn.cursor()

        # Таблица сохранений - теперь с уровнем как частью ключа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_save (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_number INTEGER NOT NULL,
                character_skin TEXT NOT NULL,
                weapon INTEGER NOT NULL,
                player_x REAL NOT NULL,
                player_y REAL NOT NULL,
                player_health INTEGER NOT NULL,
                enemies_killed INTEGER DEFAULT 0,
                cards_collected INTEGER DEFAULT 0,
                money_collected INTEGER DEFAULT 0,
                total_cards INTEGER DEFAULT 0,
                play_time REAL DEFAULT 0.0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(level_number)
            )
        ''')

        # Таблица убитых врагов - теперь с привязкой к уровню
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS killed_enemies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_number INTEGER NOT NULL,
                enemy_index INTEGER NOT NULL,
                FOREIGN KEY (level_number) REFERENCES game_save(level_number)
            )
        ''')

        # Таблица общего прогресса игры
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_level INTEGER NOT NULL DEFAULT 1,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_game(self, game_data):
        """Сохранить игру для конкретного уровня"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            # Удаляем старое сохранение для этого уровня
            cursor.execute('DELETE FROM game_save WHERE level_number = ?',
                           (game_data['level_number'],))
            cursor.execute('DELETE FROM killed_enemies WHERE level_number = ?',
                           (game_data['level_number'],))

            # Создаём новое сохранение для уровня
            cursor.execute('''
                INSERT INTO game_save 
                (level_number, character_skin, weapon, player_x, player_y, 
                 player_health, enemies_killed, cards_collected, money_collected, total_cards, play_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_data['level_number'],
                game_data['character_skin'],
                game_data['weapon'],
                game_data['player_x'],
                game_data['player_y'],
                game_data['player_health'],
                game_data['enemies_killed'],
                game_data['cards_collected'],
                game_data['money_collected'],
                game_data['total_cards'],
                game_data['play_time']
            ))

            # Сохраняем индексы убитых врагов для этого уровня
            if 'killed_enemy_indices' in game_data:
                for enemy_index in game_data['killed_enemy_indices']:
                    cursor.execute('''
                        INSERT INTO killed_enemies (level_number, enemy_index)
                        VALUES (?, ?)
                    ''', (game_data['level_number'], enemy_index))

            # Обновляем текущий уровень в прогрессе
            cursor.execute('DELETE FROM game_progress')
            cursor.execute('''
                INSERT INTO game_progress (current_level)
                VALUES (?)
            ''', (game_data['level_number'],))

            conn.commit()
            print(f"Игра сохранена для уровня {game_data['level_number']}!")
            return 1
        except Exception as e:
            conn.rollback()
            print(f"Ошибка сохранения: {e}")
            return 0
        finally:
            conn.close()

    def load_game(self, level_number):
        """Загрузить сохранение для конкретного уровня"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM game_save WHERE level_number = ?', (level_number,))
            save = cursor.fetchone()

            if not save:
                return None

            # Получаем индексы убитых врагов для этого уровня
            cursor.execute('SELECT enemy_index FROM killed_enemies WHERE level_number = ?',
                           (level_number,))
            killed_enemies = [row['enemy_index'] for row in cursor.fetchall()]

            return {
                'level_number': save['level_number'],
                'character_skin': save['character_skin'],
                'weapon': save['weapon'],
                'player_x': save['player_x'],
                'player_y': save['player_y'],
                'player_health': save['player_health'],
                'enemies_killed': save['enemies_killed'],
                'cards_collected': save['cards_collected'],
                'money_collected': save['money_collected'],
                'total_cards': save['total_cards'],
                'play_time': save['play_time'],
                'killed_enemy_indices': killed_enemies
            }
        finally:
            conn.close()

    def has_save_for_level(self, level_number):
        """Проверить есть ли сохранение для конкретного уровня"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) as count FROM game_save WHERE level_number = ?',
                           (level_number,))
            result = cursor.fetchone()

            return result['count'] > 0
        finally:
            conn.close()

    def delete_save_for_level(self, level_number):
        """Удалить сохранение для конкретного уровня"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM game_save WHERE level_number = ?', (level_number,))
            cursor.execute('DELETE FROM killed_enemies WHERE level_number = ?', (level_number,))
            conn.commit()
        finally:
            conn.close()

    def delete_all_saves(self):
        """Удалить все сохранения (полный рестарт игры)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM game_save')
            cursor.execute('DELETE FROM killed_enemies')
            cursor.execute('DELETE FROM game_progress')
            conn.commit()
            print("Все сохранения удалены!")
        finally:
            conn.close()

    def save_current_level(self, level_number):
        """Сохранить текущий уровень в прогрессе"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            # Удаляем старую запись о прогрессе
            cursor.execute('DELETE FROM game_progress')

            # Сохраняем новый уровень
            cursor.execute('''
                INSERT INTO game_progress (current_level)
                VALUES (?)
            ''', (level_number,))

            conn.commit()
        finally:
            conn.close()

    def get_current_level(self):
        """Получить текущий уровень из прогресса"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            cursor.execute('SELECT current_level FROM game_progress ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()

            if result:
                return result['current_level']
            return 1  # По умолчанию первый уровень
        finally:
            conn.close()

    def has_any_save(self):
        """Проверить есть ли хотя бы одно сохранение"""
        conn = self.connect()
        try:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) as count FROM game_save')
            result = cursor.fetchone()

            return result['count'] > 0
        finally:
            conn.close()