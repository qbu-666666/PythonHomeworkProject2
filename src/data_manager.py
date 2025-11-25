# data_manager.py
import json
import os
from datetime import datetime

class DataManager:
    """管理游戏数据的持久化存储"""
    
    def __init__(self, filename='game_data.json'):
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self):
        """加载游戏数据，如果文件不存在则创建默认数据"""
        default_data = {
            "high_score": 0,
            "games_played": 0,
            "total_score": 0,
            "total_aliens_killed": 0,
            "total_bullets_fired": 0,
            "best_level": 1,
            "game_history": [],
            "settings": {
                # 只保存音效设置，完全移除颜色相关设置
                "sound_enabled": True
            }
        }
        
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    loaded_data = json.load(f)
                    # 确保不包含颜色设置
                    if "settings" in loaded_data and "last_bg_color" in loaded_data["settings"]:
                        del loaded_data["settings"]["last_bg_color"]
                    return loaded_data
            else:
                # 文件不存在，创建默认数据文件
                self._save_data(default_data)
                return default_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 无法加载游戏数据，使用默认数据 ({e})")
            return default_data
    
    def _save_data(self, data=None):
        """保存数据到文件"""
        if data is None:
            data = self.data
            
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError as e:
            print(f"错误: 无法保存游戏数据 ({e})")
            return False
    
    def update_high_score(self, score):
        """更新最高分"""
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            self._save_data()
            return True
        return False
    
    def add_game_session(self, score, level, aliens_killed, bullets_fired, ships_left):
        """添加游戏会话记录"""
        session_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "level": level,
            "aliens_killed": aliens_killed,
            "bullets_fired": bullets_fired,
            "ships_left": ships_left
        }
        
        self.data["game_history"].insert(0, session_data)  # 添加到开头
        self.data["games_played"] += 1
        self.data["total_score"] += score
        self.data["total_aliens_killed"] += aliens_killed
        self.data["total_bullets_fired"] += bullets_fired
        
        # 更新最佳等级
        if level > self.data["best_level"]:
            self.data["best_level"] = level
        
        # 只保留最近50条记录
        if len(self.data["game_history"]) > 50:
            self.data["game_history"] = self.data["game_history"][:50]
        
        self._save_data()
    
    def get_statistics(self):
        """获取游戏统计信息"""
        games_played = self.data["games_played"]
        if games_played > 0:
            avg_score = self.data["total_score"] / games_played
            avg_aliens = self.data["total_aliens_killed"] / games_played
            accuracy = (self.data["total_aliens_killed"] / self.data["total_bullets_fired"]) * 100 if self.data["total_bullets_fired"] > 0 else 0
        else:
            avg_score = 0
            avg_aliens = 0
            accuracy = 0
            
        return {
            "high_score": self.data["high_score"],
            "games_played": games_played,
            "average_score": round(avg_score),
            "total_aliens_killed": self.data["total_aliens_killed"],
            "average_aliens_per_game": round(avg_aliens),
            "accuracy": round(accuracy, 1),
            "best_level": self.data["best_level"],
            "recent_games": self.data["game_history"][:10]  # 最近10场游戏
        }
    
    def save_settings(self, bg_color, sound_enabled):
        """保存游戏设置 - 完全忽略背景颜色参数"""
        # 重要：不再保存背景颜色，只保存音效设置
        self.data["settings"]["sound_enabled"] = sound_enabled
        self._save_data()
        print(f"保存设置: 音效={sound_enabled}, 背景颜色设置被忽略")
    
    def load_settings(self):
        """加载游戏设置"""
        return self.data["settings"]
    
    def reset_data(self):
        """重置所有游戏数据（除设置外）"""
        settings = self.data["settings"]
        default_data = {
            "high_score": 0,
            "games_played": 0,
            "total_score": 0,
            "total_aliens_killed": 0,
            "total_bullets_fired": 0,
            "best_level": 1,
            "game_history": [],
            "settings": settings
        }
        self.data = default_data
        self._save_data()
        return True