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
        """Initialize fonts"""
        try:
            # 使用Consolas等宽字体
            self.title_font = pygame.font.SysFont("Consolas", 36, bold=True)
            self.font = pygame.font.SysFont("Consolas", 24)
            self.small_font = pygame.font.SysFont("Consolas", 18)
        except:
            # 如果Consolas不可用，使用默认字体
            self.title_font = pygame.font.SysFont(None, 36, bold=True)
            self.font = pygame.font.SysFont(None, 24)
            self.small_font = pygame.font.SysFont(None, 18)
        
    def _create_ui_components(self):
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        
        # Calculate panel position (centered)
        panel_width = 600
        panel_height = 650
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Store panel dimensions for background drawing
        self.panel_rect = pygame.Rect(panel_x - 20, panel_y - 20, panel_width + 40, panel_height + 40)
        
    def draw(self):
        if not self.visible:
            return
            
        # Draw semi-transparent background
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw panel background
        pygame.draw.rect(self.screen, (50, 50, 70), self.panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 100, 130), self.panel_rect, 3, border_radius=15)
        
        # Draw title
        title_text = self.title_font.render("Game Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw settings information with proper spacing
        start_y = self.panel_rect.y + 90
        line_height = 32
        
        settings_info = [
            f"Ship Speed:          {self.settings.ship_speed:.1f}",
            f"Bullet Speed:        {self.settings.bullet_speed:.1f}",
            f"Bullets Allowed:     {self.settings.bullets_allowed}",
            f"Alien Speed:         {self.settings.alien_speed:.1f}",
            f"Alien Points:        {self.settings.alien_points}",
            f"Ship Limit:          {self.settings.ship_limit}",
            f"Fleet Drop Speed:    {self.settings.fleet_drop_speed}",
            f"Speedup Scale:       {self.settings.speedup_scale:.1f}",
            f"Score Scale:         {self.settings.score_scale:.1f}",
            f"Music Volume:        {self.settings.music_volume:.1f}",
            f"Effects Volume:      {self.settings.effects_volume:.1f}",
            f"Sound Enabled:       {'Yes' if self.settings.sound_enabled else 'No'}",
            f"Screen Size:         {self.settings.screen_width} x {self.settings.screen_height}",
            f"Background Color:    {self.settings.bg_color}"
        ]
        
        for i, info in enumerate(settings_info):
            text_surface = self.font.render(info, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midleft=(self.panel_rect.x + 40, start_y + i * line_height))
            self.screen.blit(text_surface, text_rect)
        
        # Draw separator line
        separator_y = start_y + len(settings_info) * line_height + 20
        pygame.draw.line(self.screen, (100, 100, 100), 
                        (self.panel_rect.x + 40, separator_y),
                        (self.panel_rect.x + self.panel_rect.width - 40, separator_y), 2)
        
        # Draw instructions with more space
        instructions = [
            "Note: To change settings, please edit the config.json file",
            "located in the game directory. You can modify values."
        ]
        
        instructions_y = separator_y + 30
        for i, instruction in enumerate(instructions):
            color = (180, 180, 255) if i < 2 else (200, 200, 200)
            text_surface = self.small_font.render(instruction, True, color)
            text_rect = text_surface.get_rect(center=(self.panel_rect.centerx, instructions_y + i * 22))
            self.screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if not self.visible:
            return False
            
        # Handle close events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked outside panel (close settings)
            if not self.panel_rect.collidepoint(event.pos):
                self.hide()
                return True
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.hide()
                return True
                
        return False
        
    def show(self):
        """Show settings interface"""
        self.visible = True
        
    def hide(self):
        """Hide settings interface"""
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
        
        # 使用Consolas字体
        try:
            title_font = pygame.font.SysFont("Consolas", 48, bold=True)
            font = pygame.font.SysFont("Consolas", 32)
            small_font = pygame.font.SysFont("Consolas", 20)
            hint_font = pygame.font.SysFont("Consolas", 24)
        except:
            # 如果Consolas不可用，使用默认字体
            title_font = pygame.font.SysFont(None, 48, bold=True)
            font = pygame.font.SysFont(None, 32)
            small_font = pygame.font.SysFont(None, 20)
            hint_font = pygame.font.SysFont(None, 24)
        
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
        
        # 提示文字
        hint_text = hint_font.render("Press ESC to return", True, (150, 150, 255))
        hint_rect = hint_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 50))
        self.screen.blit(hint_text, hint_rect)

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