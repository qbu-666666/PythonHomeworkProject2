# Copyright (c) 2025 tree_division
# Licensed under the MIT License

import json
import os

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # 默认配置
        self.default_config = {
            "screen": {
                "width": 1200,
                "height": 800,
                "bg_color": [57, 197, 187]  # 使用配置文件中的颜色
            },
            "ship": {
                "speed": 1.5,
                "limit": 3
            },
            "bullet": {
                "width": 3,
                "height": 15,
                "color": [60, 60, 60],
                "speed": 25,  # 注意：这里速度是25，不是2.5
                "allowed": 10
            },
            "alien": {
                "speed": 1.0,
                "drop_speed": 10,
                "points": 50
            },
            "game": {
                "speedup_scale": 1.1,
                "score_scale": 1.5
            },
            "sound": {
                "enabled": True,
                "music_volume": 0.3,
                "effects_volume": 0.6
            }
        }
        
        # 加载配置文件
        self.config = self._load_config()
        
        # 初始化设置
        self._initialize_from_config()

    def _load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        config_file = 'config.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # 合并加载的配置和默认配置，确保所有必要字段都存在
                    return self._merge_configs(loaded_config, self.default_config)
            else:
                # 创建默认配置文件
                self._create_default_config(config_file)
                return self.default_config.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 无法加载配置文件，使用默认设置 ({e})")
            return self.default_config.copy()

    def _merge_configs(self, loaded, default):
        """合并加载的配置和默认配置"""
        merged = default.copy()
        
        # 递归合并配置
        def merge_dicts(d1, d2):
            for key, value in d2.items():
                if key in d1:
                    if isinstance(d1[key], dict) and isinstance(value, dict):
                        merge_dicts(d1[key], value)
                    else:
                        d1[key] = value
            return d1
        
        return merge_dicts(merged, loaded)

    def _create_default_config(self, config_file):
        """创建默认配置文件"""
        try:
            with open(config_file, 'w') as f:
                json.dump(self.default_config, f, indent=4)
            print(f"已创建默认配置文件: {config_file}")
        except IOError as e:
            print(f"警告: 无法创建配置文件 ({e})")

    def _initialize_from_config(self):
        """从配置字典初始化设置"""
        # Screen settings
        self.screen_width = self.config["screen"]["width"]
        self.screen_height = self.config["screen"]["height"]
        self.bg_color = tuple(self.config["screen"]["bg_color"])

        # Ship settings
        self.ship_speed = self.config["ship"]["speed"]
        self.ship_limit = self.config["ship"]["limit"]

        # Bullet settings
        self.bullet_width = self.config["bullet"]["width"]
        self.bullet_height = self.config["bullet"]["height"]
        self.bullet_color = tuple(self.config["bullet"]["color"])
        self.bullet_speed = self.config["bullet"]["speed"]
        self.bullets_allowed = self.config["bullet"]["allowed"]

        # Alien settings
        self.alien_speed = self.config["alien"]["speed"]
        self.fleet_drop_speed = self.config["alien"]["drop_speed"]
        self.alien_points = self.config["alien"]["points"]

        # Game settings
        self.speedup_scale = self.config["game"]["speedup_scale"]
        self.score_scale = self.config["game"]["score_scale"]

        # Sound settings
        self.sound_enabled = self.config["sound"]["enabled"]
        self.music_volume = self.config["sound"]["music_volume"]
        self.effects_volume = self.config["sound"]["effects_volume"]

    def initialize_dynamic_settings(self):
        """Initialize settings that can change throughout the game."""
        # 从配置重新加载初始速度
        self.ship_speed = self.config["ship"]["speed"]
        self.bullet_speed = self.config["bullet"]["speed"]
        self.alien_speed = self.config["alien"]["speed"]

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = self.config["alien"]["points"]

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def save_config(self):
        """保存当前设置到配置文件"""
        try:
            # 更新配置字典
            self.config["screen"]["width"] = self.screen_width
            self.config["screen"]["height"] = self.screen_height
            self.config["screen"]["bg_color"] = list(self.bg_color)
            
            self.config["ship"]["speed"] = self.ship_speed
            self.config["ship"]["limit"] = self.ship_limit
            
            self.config["bullet"]["width"] = self.bullet_width
            self.config["bullet"]["height"] = self.bullet_height
            self.config["bullet"]["color"] = list(self.bullet_color)
            self.config["bullet"]["speed"] = self.bullet_speed
            self.config["bullet"]["allowed"] = self.bullets_allowed
            
            self.config["alien"]["speed"] = self.alien_speed
            self.config["alien"]["drop_speed"] = self.fleet_drop_speed
            self.config["alien"]["points"] = self.alien_points
            
            self.config["game"]["speedup_scale"] = self.speedup_scale
            self.config["game"]["score_scale"] = self.score_scale
            
            self.config["sound"]["enabled"] = self.sound_enabled
            self.config["sound"]["music_volume"] = self.music_volume
            self.config["sound"]["effects_volume"] = self.effects_volume
            
            # 保存到文件
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            print("配置已保存到 config.json")
            
        except IOError as e:
            print(f"错误: 无法保存配置文件 ({e})")