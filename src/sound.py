import pygame
import os

class SoundManager:
    """管理游戏中的所有音效"""
    
    def __init__(self, settings):
        """初始化音效管理器"""
        self.settings = settings
        pygame.mixer.init()
        self.sounds_loaded = False
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
            else:
                print("警告: 找不到 sounds/shoot.wav 文件")
                self.shoot_sound = None
            
            # 检查并加载外星人爆炸音效
            if os.path.exists('sounds/explosion.wav'):
                self.alien_explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
                self.alien_explosion_sound.set_volume(self.settings.effects_volume * 0.6)
            else:
                print("警告: 找不到 sounds/explosion.wav 文件")
                self.alien_explosion_sound = None
            
            # 检查并加载飞船被撞音效
            if os.path.exists('sounds/ship_hit.wav'):
                self.ship_hit_sound = pygame.mixer.Sound('sounds/ship_hit.wav')
                self.ship_hit_sound.set_volume(self.settings.effects_volume * 0.7)
            else:
                print("警告: 找不到 sounds/ship_hit.wav 文件")
                self.ship_hit_sound = None
            
            # 检查并加载游戏结束音效
            if os.path.exists('sounds/game_over.wav'):
                self.game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
                self.game_over_sound.set_volume(self.settings.effects_volume * 0.8)
            else:
                print("警告: 找不到 sounds/game_over.wav 文件")
                self.game_over_sound = None
            
            # 检查并加载等级提升音效
            if os.path.exists('sounds/level_up.wav'):
                self.level_up_sound = pygame.mixer.Sound('sounds/level_up.wav')
                self.level_up_sound.set_volume(self.settings.effects_volume * 0.6)
            else:
                print("警告: 找不到 sounds/level_up.wav 文件")
                self.level_up_sound = None
            
            # 如果有至少一个音效加载成功，则标记为已加载
            if any([self.shoot_sound, self.alien_explosion_sound, self.ship_hit_sound, 
                   self.game_over_sound, self.level_up_sound]):
                self.sounds_loaded = True
                print("音效加载完成（部分文件可能缺失）")
            else:
                print("没有找到任何音效文件，游戏将在静音模式下运行")
                self.sounds_loaded = False
                
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
        if not self.settings.sound_enabled:
            return
            
        try:
            if os.path.exists('sounds/background_music.mp3'):
                pygame.mixer.music.load('sounds/background_music.mp3')
                pygame.mixer.music.set_volume(self.settings.music_volume)
                pygame.mixer.music.play(-1)  # -1 表示循环播放
                print("背景音乐已加载并播放")
            else:
                print("背景音乐文件 sounds/background_music.mp3 不存在")
        except pygame.error as e:
            print(f"无法加载背景音乐: {e}")
    
    def stop_background_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
    
    def pause_background_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()
    
    def unpause_background_music(self):
        """恢复背景音乐"""
        if self.settings.sound_enabled:
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
        pygame.mixer.music.set_volume(volume)
    
    def are_sounds_available(self):
        """检查是否有任何音效可用"""
        return self.sounds_loaded and self.settings.sound_enabled
    
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