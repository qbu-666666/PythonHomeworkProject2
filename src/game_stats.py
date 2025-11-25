# Copyright (c) 2025 tree_division
# Licensed under the MIT License

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0
        
        # 新增：用于数据统计的字段
        self.bullets_fired = 0
        self.aliens_killed = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        # 重置统计字段
        self.bullets_fired = 0
        self.aliens_killed = 0
        
    def record_game_session(self):
        """记录游戏会话到数据管理器"""
        if hasattr(self, '_ai_game'):  # 确保有引用到主游戏对象
            self._ai_game.data_manager.add_game_session(
                self.score, 
                self.level, 
                self.aliens_killed, 
                self.bullets_fired, 
                self.ships_left
            )