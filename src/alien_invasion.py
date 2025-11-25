import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from sound import SoundManager
from data_manager import DataManager


class Slider:
    """滑动条组件"""
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_radius = 15
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
        # 初始化字体
        try:
            self.font = pygame.font.SysFont("simsun", 28)
        except:
            try:
                self.font = pygame.font.SysFont("microsoftyahei", 28)
            except:
                self.font = pygame.font.SysFont(None, 28)
        
        # 计算初始滑块位置
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width
        
    def draw(self, screen):
        # 绘制轨道
        pygame.draw.rect(screen, (100, 100, 100), self.rect, border_radius=5)
        
        # 绘制滑块
        knob_pos = (int(self.knob_x), self.rect.centery)
        pygame.draw.circle(screen, (70, 130, 180), knob_pos, self.knob_radius)
        pygame.draw.circle(screen, (255, 255, 255), knob_pos, self.knob_radius - 3, 2)
        
        # 绘制标签和值
        label_text = self.font.render(f"{self.label}: {self.value:.1f}", True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 30))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.knob_x - self.knob_radius <= event.pos[0] <= self.knob_x + self.knob_radius and
                self.rect.y - self.knob_radius <= event.pos[1] <= self.rect.y + self.knob_radius):
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # 更新滑块位置
            self.knob_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            
            # 计算值
            ratio = (self.knob_x - self.rect.left) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            return True
            
        return False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.knob_x - self.knob_radius <= event.pos[0] <= self.knob_x + self.knob_radius and
                self.rect.y - self.knob_radius <= event.pos[1] <= self.rect.y + self.knob_radius):
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # 更新滑块位置
            self.knob_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            
            # 计算值
            ratio = (self.knob_x - self.rect.left) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            return True
            
        return False


class SettingsGUI:
    """设置GUI主类"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.sound_manager = ai_game.sound_manager
        self.visible = False
        
        # 初始化字体
        self._init_fonts()
        
        # 创建UI组件
        self._create_ui_components()
        
    def _init_fonts(self):
        """初始化字体"""
        try:
            # 尝试使用系统中可能存在的支持中文的字体
            self.title_font = pygame.font.SysFont("simsun", 48)  # 宋体
            self.font = pygame.font.SysFont("simsun", 28)        # 宋体
            self.small_font = pygame.font.SysFont("simsun", 24)  # 宋体
        except:
            try:
                # 如果simsun不可用，尝试其他中文字体
                self.title_font = pygame.font.SysFont("microsoftyahei", 48)  # 微软雅黑
                self.font = pygame.font.SysFont("microsoftyahei", 28)
                self.small_font = pygame.font.SysFont("microsoftyahei", 24)
            except:
                try:
                    # 如果还不行，尝试使用Arial Unicode MS
                    self.title_font = pygame.font.SysFont("arialunicodems", 48)
                    self.font = pygame.font.SysFont("arialunicodems", 28)
                    self.small_font = pygame.font.SysFont("arialunicodems", 24)
                except:
                    # 最后使用默认字体
                    self.title_font = pygame.font.SysFont(None, 48)
                    self.font = pygame.font.SysFont(None, 28)
                    self.small_font = pygame.font.SysFont(None, 24)
                    print("警告: 使用默认字体，中文可能显示为方块")
        
    def _create_ui_components(self):
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        
        # 计算面板位置（居中）
        panel_width = 500
        panel_height = 500
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # 创建滑动条
        slider_x = panel_x + 50
        slider_y = panel_y + 80
        slider_width = 400
        
        self.ship_speed_slider = Slider(slider_x, slider_y, slider_width, 10, 0.5, 3.0, 
                                       self.settings.ship_speed, "飞船速度")
        
        self.bullet_speed_slider = Slider(slider_x, slider_y + 60, slider_width, 10, 1.0, 10.0,
                                         self.settings.bullet_speed, "子弹速度")
        
        self.alien_speed_slider = Slider(slider_x, slider_y + 120, slider_width, 10, 0.5, 3.0,
                                        self.settings.alien_speed, "外星人速度")
        
        self.music_volume_slider = Slider(slider_x, slider_y + 180, slider_width, 10, 0.0, 1.0,
                                         self.settings.music_volume, "音乐音量")
        
        self.effects_volume_slider = Slider(slider_x, slider_y + 240, slider_width, 10, 0.0, 1.0,
                                           self.settings.effects_volume, "音效音量")
        
        # 创建复选框
        checkbox_y = slider_y + 300
        self.sound_checkbox_rect = pygame.Rect(slider_x, checkbox_y, 20, 20)
        self.sound_checkbox_checked = self.settings.sound_enabled
        
        # 创建按钮
        button_y = panel_y + panel_height - 60
        self.apply_button_rect = pygame.Rect(slider_x, button_y, 120, 40)
        self.cancel_button_rect = pygame.Rect(slider_x + 140, button_y, 120, 40)
        self.reset_button_rect = pygame.Rect(slider_x + 280, button_y, 120, 40)
        
        # 存储面板尺寸用于绘制背景
        self.panel_rect = pygame.Rect(panel_x - 20, panel_y - 20, panel_width + 40, panel_height + 40)
        
    def draw(self):
        if not self.visible:
            return
            
        # 绘制半透明背景
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        self.screen.blit(overlay, (0, 0))
        
        # 绘制面板背景
        pygame.draw.rect(self.screen, (50, 50, 70), self.panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 100, 130), self.panel_rect, 3, border_radius=15)
        
        # 绘制标题
        title_text = self.title_font.render("游戏设置", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 40))
        self.screen.blit(title_text, title_rect)
        
        # 绘制所有UI组件
        self.ship_speed_slider.draw(self.screen)
        self.bullet_speed_slider.draw(self.screen)
        self.alien_speed_slider.draw(self.screen)
        self.music_volume_slider.draw(self.screen)
        self.effects_volume_slider.draw(self.screen)
        
        # 绘制复选框
        pygame.draw.rect(self.screen, (200, 200, 200), self.sound_checkbox_rect, 2, border_radius=4)
        if self.sound_checkbox_checked:
            pygame.draw.rect(self.screen, (70, 130, 180), self.sound_checkbox_rect.inflate(-8, -8), border_radius=2)
        label_text = self.font.render("启用音效", True, (255, 255, 255))
        self.screen.blit(label_text, (self.sound_checkbox_rect.right + 10, self.sound_checkbox_rect.y))
        
        # 绘制按钮
        pygame.draw.rect(self.screen, (0, 135, 0), self.apply_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.apply_button_rect, 2, border_radius=8)
        apply_text = self.font.render("应用", True, (255, 255, 255))
        apply_rect = apply_text.get_rect(center=self.apply_button_rect.center)
        self.screen.blit(apply_text, apply_rect)
        
        pygame.draw.rect(self.screen, (180, 0, 0), self.cancel_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.cancel_button_rect, 2, border_radius=8)
        cancel_text = self.font.render("取消", True, (255, 255, 255))
        cancel_rect = cancel_text.get_rect(center=self.cancel_button_rect.center)
        self.screen.blit(cancel_text, cancel_rect)
        
        pygame.draw.rect(self.screen, (180, 100, 0), self.reset_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.reset_button_rect, 2, border_radius=8)
        reset_text = self.font.render("重置默认", True, (255, 255, 255))
        reset_rect = reset_text.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(reset_text, reset_rect)
        
    def handle_event(self, event):
        if not self.visible:
            return False
            
        # 处理所有UI组件的事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了面板外部（关闭设置）
            if not self.panel_rect.collidepoint(event.pos):
                self.hide()
                return True
                
            # 处理复选框
            if self.sound_checkbox_rect.collidepoint(event.pos):
                self.sound_checkbox_checked = not self.sound_checkbox_checked
                return True
                
            # 处理按钮
            if self.apply_button_rect.collidepoint(event.pos):
                self.apply_settings()
                self.hide()
                return True
            elif self.cancel_button_rect.collidepoint(event.pos):
                self.hide()
                return True
            elif self.reset_button_rect.collidepoint(event.pos):
                self.reset_to_default()
                return True
                
        # 处理滑动条
        self.ship_speed_slider.handle_event(event)
        self.bullet_speed_slider.handle_event(event)
        self.alien_speed_slider.handle_event(event)
        self.music_volume_slider.handle_event(event)
        self.effects_volume_slider.handle_event(event)
            
        return False
        
    def apply_settings(self):
        """应用设置到游戏"""
        # 更新游戏设置
        self.settings.ship_speed = self.ship_speed_slider.value
        self.settings.bullet_speed = self.bullet_speed_slider.value
        self.settings.alien_speed = self.alien_speed_slider.value
        self.settings.music_volume = self.music_volume_slider.value
        self.settings.effects_volume = self.effects_volume_slider.value
        self.settings.sound_enabled = self.sound_checkbox_checked
        
        # 更新音效管理器
        if hasattr(self.sound_manager, 'set_music_volume'):
            self.sound_manager.set_music_volume(self.settings.music_volume)
        if hasattr(self.sound_manager, 'set_volume'):
            self.sound_manager.set_volume(self.settings.effects_volume)
        
        # 根据音效设置播放或暂停音乐
        if self.settings.sound_enabled:
            if hasattr(self.sound_manager, 'unpause_background_music'):
                self.sound_manager.unpause_background_music()
        else:
            if hasattr(self.sound_manager, 'pause_background_music'):
                self.sound_manager.pause_background_music()
            
        # 保存配置到文件
        self.settings.save_config()
        
        print("设置已应用并保存")
        
    def reset_to_default(self):
        """重置为默认设置"""
        # 重新加载默认设置
        self.settings = Settings()
        self.ai_game.settings = self.settings
        
        # 重新创建UI组件以反映默认值
        self._create_ui_components()
        
        print("已重置为默认设置")
        
    def show(self):
        """显示设置界面"""
        self.visible = True
        # 刷新UI组件值
        self._create_ui_components()
        
    def hide(self):
        """隐藏设置界面"""
        self.visible = False


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        # 创建数据管理器
        self.data_manager = DataManager()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建音效管理器实例
        self.sound_manager = SoundManager(self.settings)

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")
        
        # 添加统计信息按钮
        self.stats_button = Button(self, "Stats")
        self.stats_button.rect.y += 60  # 在Play按钮下方
        
        # 添加设置按钮
        self.settings_button = Button(self, "Settings")
        self.settings_button.rect.y += 120  # 在Stats按钮下方
        
        # 添加设置GUI
        self.settings_gui = SettingsGUI(self)
        
        # 添加按键状态跟踪
        self.keys_pressed = set()
        
        # 是否显示统计信息
        self.showing_stats = False
        
        # 加载保存的设置
        self._load_saved_settings()

    def _load_saved_settings(self):
        """加载保存的游戏设置 - 确保不覆盖配置文件中的背景颜色"""
        saved_settings = self.data_manager.load_settings()
        
        # 重要：不再从保存的数据中加载背景颜色！
        # 背景颜色只从 config.json 读取
        
        # 只设置音效
        if "sound_enabled" in saved_settings:
            self.settings.sound_enabled = saved_settings["sound_enabled"]
            if not self.settings.sound_enabled:
                self.sound_manager.pause_background_music()
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active and not self.settings_gui.visible:
                self._update_ship_movement()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 游戏退出前保存设置
                self.data_manager.save_settings(
                    self.settings.bg_color, 
                    self.settings.sound_enabled
                )
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 先检查设置GUI
                if self.settings_gui.visible:
                    if self.settings_gui.handle_event(event):
                        continue
                # 然后检查按钮
                self._check_play_button(mouse_pos)
                self._check_stats_button(mouse_pos)
                self._check_settings_button(mouse_pos)

    def _check_stats_button(self, mouse_pos):
        """检查统计信息按钮点击"""
        if self.showing_stats or self.settings_gui.visible:
            return
            
        button_clicked = self.stats_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.showing_stats = True

    def _check_settings_button(self, mouse_pos):
        """检查设置按钮点击"""
        if self.showing_stats or self.settings_gui.visible or self.game_active:
            return
        
        button_clicked = self.settings_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.settings_gui.show()

    def _update_ship_movement(self):
        """基于当前按下的键更新飞船移动状态"""
        # 获取所有当前按下的键
        current_keys = pygame.key.get_pressed()
        
        # 重置移动状态
        self.ship.moving_right = False
        self.ship.moving_left = False
        
        # 检查方向键
        if current_keys[pygame.K_RIGHT]:
            self.ship.moving_right = True
        if current_keys[pygame.K_LEFT]:
            self.ship.moving_left = True
            
        # 检查WASD键
        if current_keys[pygame.K_d]:
            self.ship.moving_right = True
        if current_keys[pygame.K_a]:
            self.ship.moving_left = True

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.showing_stats or self.settings_gui.visible:
            return
            
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # 播放背景音乐
            if self.settings.sound_enabled:
                self.sound_manager.play_background_music()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            # 退出前保存设置
            self.data_manager.save_settings(
                self.settings.bg_color, 
                self.settings.sound_enabled
            )
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_m:  # 添加静音切换功能
            self.settings.sound_enabled = not self.settings.sound_enabled
            if self.settings.sound_enabled:
                self.sound_manager.unpause_background_music()
            else:
                self.sound_manager.pause_background_music()
        elif event.key == pygame.K_F1:  # 重新加载配置
            old_color = self.settings.bg_color
            self.settings = Settings()
            self.sound_manager = SoundManager(self.settings)
            self.sb = Scoreboard(self)
            print(f"配置已重新加载，背景颜色从 {old_color} 变为 {self.settings.bg_color}")
        elif event.key == pygame.K_F2:  # 保存配置
            self.settings.save_config()
        elif event.key == pygame.K_F3:  # 调试：重置飞船移动状态
            self.ship.moving_right = False
            self.ship.moving_left = False
            print("飞船移动状态已重置")
        elif event.key == pygame.K_s and not self.game_active:  # 显示统计信息
            self.showing_stats = True
        elif event.key == pygame.K_ESCAPE:  # ESC键处理
            if self.settings_gui.visible:
                self.settings_gui.hide()
            elif self.showing_stats:
                self.showing_stats = False
        elif event.key == pygame.K_r and not self.game_active and not self.showing_stats:  # 重置数据
            self.data_manager.reset_data()
            self.stats.high_score = 0
            self.sb.prep_high_score()
            print("游戏数据已重置")
        elif event.key == pygame.K_TAB and not self.game_active:  # TAB键打开设置
            self.settings_gui.show()
        
        # 方向键处理
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_d:  # WASD支持
            self.ship.moving_right = True
        elif event.key == pygame.K_a:  # WASD支持
            self.ship.moving_left = True

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        # 我们不再在这里处理移动键的释放，而是在_update_ship_movement中处理
        pass

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # 播放射击音效
            self.sound_manager.play_shoot()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            # 播放外星人爆炸音效
            self.sound_manager.play_alien_explosion()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            # 播放等级提升音效
            self.sound_manager.play_level_up()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # 播放飞船被击中音效
        self.sound_manager.play_ship_hit()
        
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            # 播放游戏结束音效
            self.sound_manager.play_game_over()
            # 停止背景音乐
            self.sound_manager.stop_background_music()
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _draw_statistics(self):
        """绘制统计信息界面"""
        # 半透明背景
        s = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))  # 半透明黑色
        self.screen.blit(s, (0, 0))
        
        # 获取统计数据
        stats = self.data_manager.get_statistics()
        
        # 尝试加载中文字体，如果失败则使用默认字体
        try:
            # 尝试使用系统中可能存在的支持中文的字体
            title_font = pygame.font.SysFont("simsunnsimsun", 64)
            font = pygame.font.SysFont("simsunnsimsun", 36)
            small_font = pygame.font.SysFont("simsunnsimsun", 24)
            hint_font = pygame.font.SysFont("simsunnsimsun", 28)
        except:
            # 如果找不到中文字体，使用默认字体
            title_font = pygame.font.SysFont(None, 64)
            font = pygame.font.SysFont(None, 36)
            small_font = pygame.font.SysFont(None, 24)
            hint_font = pygame.font.SysFont(None, 28)
        
        # 标题
        title = title_font.render("Game Statistics", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 50))
        self.screen.blit(title, title_rect)
        
        # 主要统计数据
        y_pos = 120
        line_height = 40
        
        stats_texts = [
            f"High Score: {stats['high_score']}",
            f"Games Played: {stats['games_played']}",
            f"Average Score: {stats['average_score']}",
            f"Total Aliens Killed: {stats['total_aliens_killed']}",
            f"Average Aliens Per Game: {stats['average_aliens_per_game']}",
            f"Accuracy: {stats['accuracy']}%",
            f"Best Level: {stats['best_level']}"
        ]
        
        for text in stats_texts:
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (100, y_pos))
            y_pos += line_height
        
        # 最近游戏记录
        y_pos += 20
        recent_title = font.render("Recent Games:", True, (255, 255, 255))
        self.screen.blit(recent_title, (100, y_pos))
        y_pos += line_height
        
        for i, game in enumerate(stats['recent_games']):
            if i >= 5:  # 只显示最近5场
                break
            game_text = f"{game['date']} - Score: {game['score']}, Level: {game['level']}, Kills: {game['aliens_killed']}"
            game_surface = small_font.render(game_text, True, (200, 200, 200))
            self.screen.blit(game_surface, (120, y_pos))
            y_pos += 30

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        
        if self.settings_gui.visible:
            self.settings_gui.draw()
        elif self.showing_stats:
            self._draw_statistics()
        else:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)

            # Draw the score information.
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.game_active:
                self.play_button.draw_button()
                self.stats_button.draw_button()
                self.settings_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()