import arcade
import random
import math
from core import *


class ParticleSystem:
    """Система управления частицами"""

    def __init__(self):
        self.particles = []
        self.particle_types = {
            'blood': {
                'color': PARTICLE_BLOOD_COLOR,
                'size': PARTICLE_SIZE_BLOOD,
                'lifetime': PARTICLE_BLOOD_LIFETIME,
                'count': PARTICLE_BLOOD_COUNT,
                'speed': PARTICLE_SPEED_BLOOD,
                'gravity': True
            },
            'run_dust': {
                'color': PARTICLE_DUST_COLOR,
                'size': PARTICLE_SIZE_DUST,
                'lifetime': PARTICLE_DUST_LIFETIME,
                'count': PARTICLE_DUST_COUNT,
                'speed': PARTICLE_SPEED_DUST,
                'gravity': False
            },
            'shot_spark_1': {  # Для оружия 1
                'color': PARTICLE_SPARK_COLOR_1,
                'size': PARTICLE_SIZE_SPARK,
                'lifetime': PARTICLE_SPARK_LIFETIME,
                'count': PARTICLE_SPARK_COUNT,
                'speed': PARTICLE_SPEED_SPARK,
                'gravity': False
            },
            'shot_spark_2': {  # Для оружия 2
                'color': PARTICLE_SPARK_COLOR_2,
                'size': PARTICLE_SIZE_SPARK,
                'lifetime': PARTICLE_SPARK_LIFETIME,
                'count': PARTICLE_SPARK_COUNT,
                'speed': PARTICLE_SPEED_SPARK,
                'gravity': False
            },
            'shot_spark_3': {  # Для оружия 3
                'color': PARTICLE_SPARK_COLOR_3,
                'size': PARTICLE_SIZE_SPARK,
                'lifetime': PARTICLE_SPARK_LIFETIME,
                'count': PARTICLE_SPARK_COUNT,
                'speed': PARTICLE_SPEED_SPARK,
                'gravity': False
            },
            'enemy_shot_spark': {  # Для врагов
                'color': PARTICLE_SPARK_COLOR_ENEMIES,
                'size': PARTICLE_SIZE_SPARK,
                'lifetime': PARTICLE_SPARK_LIFETIME,
                'count': PARTICLE_SPARK_COUNT,
                'speed': PARTICLE_SPEED_SPARK,
                'gravity': False
            },
            'hit': {
                'color': PARTICLE_HIT_COLOR,
                'size': PARTICLE_SIZE_HIT,
                'lifetime': PARTICLE_HIT_LIFETIME,
                'count': PARTICLE_HIT_COUNT,
                'speed': PARTICLE_SPEED_HIT,
                'gravity': False
            }
        }

    def create_particles(self, x, y, particle_type='blood', direction=0, spread=180):
        """Создать частицы в указанной точке"""
        if particle_type not in self.particle_types:
            return

        config = self.particle_types[particle_type]

        for _ in range(config['count']):
            angle = math.radians(direction + random.uniform(-spread / 2, spread / 2))
            speed = random.uniform(config['speed'] * 0.5, config['speed'] * 1.5)

            particle = {
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': random.uniform(config['size'] * 0.7, config['size'] * 1.3),
                'color': config['color'],
                'lifetime': random.uniform(config['lifetime'] * 0.7, config['lifetime'] * 1.3),
                'max_lifetime': config['lifetime'],
                'gravity': config['gravity'],
                'alpha': 255
            }
            self.particles.append(particle)

    def update(self, delta_time):
        """Обновить все частицы"""
        particles_to_remove = []

        for particle in self.particles:
            particle['x'] += particle['dx'] * delta_time
            particle['y'] += particle['dy'] * delta_time

            if particle['gravity']:
                particle['dy'] -= GRAVITY * 50 * delta_time

            particle['lifetime'] -= delta_time
            alpha_ratio = max(0.0, min(1.0, particle['lifetime'] / particle['max_lifetime']))
            particle['alpha'] = int(255 * alpha_ratio)

            if particle['lifetime'] <= 0:
                particles_to_remove.append(particle)

        for particle in particles_to_remove:
            self.particles.remove(particle)

    def draw(self):
        """Отрисовать все частицы"""
        for particle in self.particles:
            color = (*particle['color'][:3], particle['alpha'])
            arcade.draw_circle_filled(
                particle['x'],
                particle['y'],
                particle['size'],
                color
            )

    def clear(self):
        """Очистить все частицы"""
        self.particles.clear()


class ParticleEmitter:
    """Эмиттер частиц для привязки к объектам"""

    def __init__(self, particle_system):
        self.particle_system = particle_system
        self.run_timer = 0
        self.run_interval = 0.1  # Интервал между частицами при беге

    def emit_blood(self, x, y, direction=90):
        """Эмитировать частицы крови"""
        self.particle_system.create_particles(x, y, 'blood', direction)

    def emit_run_dust(self, x, y, direction=-90, facing_direction=1):
        """Эмитировать пыль при беге"""
        # Направление в зависимости от направления движения
        if facing_direction < 0:  # Бежит влево
            direction = 270  # Вниз и влево
        else:  # Бежит вправо
            direction = 270  # Вниз и вправо

        self.particle_system.create_particles(x, y - 10, 'run_dust', direction, 90)

    def emit_enemy_shot_spark(self, x, y, direction=0):
        """Эмитировать искры выстрела врага (всегда фиолетовые)"""
        self.particle_system.create_particles(x, y, 'enemy_shot_spark', direction, 60)

    def emit_shot_spark(self, x, y, direction=0, weapon_type=1):
        """Эмитировать искры выстрела игрока в зависимости от оружия"""
        spark_type = f'shot_spark_{weapon_type}'
        self.particle_system.create_particles(x, y, spark_type, direction, 30)

    def emit_hit(self, x, y, direction=0):
        """Эмитировать частицы при попадании"""
        self.particle_system.create_particles(x, y, 'hit', direction, 360)

    def update_run(self, delta_time, should_emit, x, y, facing_direction):
        """Обновить эмиттер бега"""
        self.run_timer += delta_time
        if should_emit and self.run_timer >= self.run_interval:
            self.run_timer = 0
            self.emit_run_dust(x, y, -90, facing_direction)