import pygame
import os

class SoundManager:
    """管理游戏中的所有音效"""
    
    def __init__(self, settings):
        """初始化音效管理器"""
        self.settings = settings
        pygame.mixer.init()
        self.sounds_loaded = False
        self.music_available = False
        self._load_sounds()
    
    def _load_sounds(self):
        """加载所有音效文件"""
        # 确保sounds目录存在
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            print("创建了sounds目录，请将音效文件放入此目录")
            self._create_dummy_sounds()
            return
            
        try:
            # 检查并加载射击音效
            if os.path.exists('sounds/shoot.wav'):
                self.shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
                self.shoot_sound.set_volume(self.settings.effects_volume * 0.5)
                print("加载射击音效成功")
            else:
                print("警告: 找不到 sounds/shoot.wav 文件")
                self.shoot_sound = None
            
            # 检查并加载外星人爆炸音效
            if os.path.exists('sounds/explosion.wav'):
                self.alien_explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
                self.alien_explosion_sound.set_volume(self.settings.effects_volume * 0.6)
                print("加载爆炸音效成功")
            else:
                print("警告: 找不到 sounds/explosion.wav 文件")
                self.alien_explosion_sound = None
            
            # 检查并加载飞船被撞音效
            if os.path.exists('sounds/ship_hit.wav'):
                self.ship_hit_sound = pygame.mixer.Sound('sounds/ship_hit.wav')
                self.ship_hit_sound.set_volume(self.settings.effects_volume * 0.7)
                print("加载飞船被撞音效成功")
            else:
                print("警告: 找不到 sounds/ship_hit.wav 文件")
                self.ship_hit_sound = None
            
            # 检查并加载游戏结束音效
            if os.path.exists('sounds/game_over.wav'):
                self.game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
                self.game_over_sound.set_volume(self.settings.effects_volume * 0.8)
                print("加载游戏结束音效成功")
            else:
                print("警告: 找不到 sounds/game_over.wav 文件")
                self.game_over_sound = None
            
            # 检查并加载等级提升音效
            if os.path.exists('sounds/level_up.wav'):
                self.level_up_sound = pygame.mixer.Sound('sounds/level_up.wav')
                self.level_up_sound.set_volume(self.settings.effects_volume * 0.6)
                print("加载等级提升音效成功")
            else:
                print("警告: 找不到 sounds/level_up.wav 文件")
                self.level_up_sound = None
            
            # 检查背景音乐
            if os.path.exists('sounds/background_music.mp3'):
                self.music_available = True
                print("背景音乐文件可用")
            else:
                print("背景音乐文件 sounds/background_music.mp3 不存在")
                self.music_available = False
            
            # 分别统计音效和背景音乐的可用性
            sound_effects_available = any([self.shoot_sound, self.alien_explosion_sound, 
                                         self.ship_hit_sound, self.game_over_sound, 
                                         self.level_up_sound])
            
            # 更新加载状态
            self.sounds_loaded = sound_effects_available
            
            # 输出详细的音频状态
            print("=== 音频系统状态 ===")
            if self.music_available:
                print("✓ 背景音乐: 可用")
            else:
                print("✗ 背景音乐: 不可用")
                
            if self.sounds_loaded:
                print("✓ 音效: 可用")
                # 列出可用的音效
                available_sounds = []
                if self.shoot_sound: available_sounds.append("射击")
                if self.alien_explosion_sound: available_sounds.append("爆炸")
                if self.ship_hit_sound: available_sounds.append("飞船被撞")
                if self.game_over_sound: available_sounds.append("游戏结束")
                if self.level_up_sound: available_sounds.append("等级提升")
                print(f"  可用音效: {', '.join(available_sounds)}")
            else:
                print("✗ 音效: 不可用")
                
            if not self.music_available and not self.sounds_loaded:
                print("警告: 背景音乐和音效都不可用，游戏将在完全静音模式下运行")
            elif not self.sounds_loaded:
                print("注意: 音效不可用，但背景音乐可用")
            elif not self.music_available:
                print("注意: 背景音乐不可用，但音效可用")
            print("===================")
                
        except pygame.error as e:
            print(f"加载音效时出错: {e}")
            print("游戏将继续运行，但没有音效")
            self._create_dummy_sounds()
    
    def _create_dummy_sounds(self):
        """创建空的音效对象作为备选"""
        self.shoot_sound = None
        self.alien_explosion_sound = None
        self.ship_hit_sound = None
        self.game_over_sound = None
        self.level_up_sound = None
        self.sounds_loaded = False
        self.music_available = False
    
    def play_shoot(self):
        """播放射击音效"""
        if self.settings.sound_enabled and self.sounds_loaded and self.shoot_sound:
            self.shoot_sound.play()
    
    def play_alien_explosion(self):
        """播放外星人爆炸音效"""
        if self.settings.sound_enabled and self.sounds_loaded and self.alien_explosion_sound:
            self.alien_explosion_sound.play()
    
    def play_ship_hit(self):
        """播放飞船被击中音效"""
        if self.settings.sound_enabled and self.sounds_loaded and self.ship_hit_sound:
            self.ship_hit_sound.play()
    
    def play_game_over(self):
        """播放游戏结束音效"""
        if self.settings.sound_enabled and self.sounds_loaded and self.game_over_sound:
            self.game_over_sound.play()
    
    def play_level_up(self):
        """播放等级提升音效"""
        if self.settings.sound_enabled and self.sounds_loaded and self.level_up_sound:
            self.level_up_sound.play()
    
    def play_background_music(self):
        """播放背景音乐"""
        if not self.settings.sound_enabled or not self.music_available:
            return
            
        try:
            pygame.mixer.music.load('sounds/background_music.mp3')
            pygame.mixer.music.set_volume(self.settings.music_volume)
            pygame.mixer.music.play(-1)  # -1 表示循环播放
            print("背景音乐已加载并播放")
        except pygame.error as e:
            print(f"无法加载背景音乐: {e}")
            self.music_available = False
    
    def stop_background_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
    
    def pause_background_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()
    
    def unpause_background_music(self):
        """恢复背景音乐"""
        if self.settings.sound_enabled and self.music_available:
            pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """设置所有音效的音量 (0.0 到 1.0)"""
        self.settings.effects_volume = volume
        if self.sounds_loaded:
            if self.shoot_sound:
                self.shoot_sound.set_volume(volume * 0.5)
            if self.alien_explosion_sound:
                self.alien_explosion_sound.set_volume(volume * 0.6)
            if self.ship_hit_sound:
                self.ship_hit_sound.set_volume(volume * 0.7)
            if self.game_over_sound:
                self.game_over_sound.set_volume(volume * 0.8)
            if self.level_up_sound:
                self.level_up_sound.set_volume(volume * 0.6)
    
    def set_music_volume(self, volume):
        """设置背景音乐音量 (0.0 到 1.0)"""
        self.settings.music_volume = volume
        if self.music_available:
            pygame.mixer.music.set_volume(volume)
    
    def are_sounds_available(self):
        """检查是否有任何音效可用"""
        return self.sounds_loaded and self.settings.sound_enabled
    
    def is_music_available(self):
        """检查背景音乐是否可用"""
        return self.music_available and self.settings.sound_enabled
    
    def get_missing_sounds(self):
        """返回缺失的音效文件列表"""
        missing = []
        if not os.path.exists('sounds/shoot.wav'):
            missing.append('shoot.wav')
        if not os.path.exists('sounds/explosion.wav'):
            missing.append('explosion.wav')
        if not os.path.exists('sounds/ship_hit.wav'):
            missing.append('ship_hit.wav')
        if not os.path.exists('sounds/game_over.wav'):
            missing.append('game_over.wav')
        if not os.path.exists('sounds/level_up.wav'):
            missing.append('level_up.wav')
        if not os.path.exists('sounds/background_music.mp3'):
            missing.append('background_music.mp3')
        return missing
    
    def get_audio_status(self):
        """返回音频系统的详细状态"""
        return {
            'sound_enabled': self.settings.sound_enabled,
            'sounds_loaded': self.sounds_loaded,
            'music_available': self.music_available,
            'effects_volume': self.settings.effects_volume,
            'music_volume': self.settings.music_volume
        }