#SHADOWFALL FINAL

import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadowfall: Levels")

WHITE = (255, 255, 255)
GREY = (31, 27, 24)
RED = (255, 0, 0)
GREEN = (50, 255, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 36)
FPS = 60
clock = pygame.time.Clock()


# Menu variables
menu_active = True
level_1_completed = False

# defining fuctions (general)
def draw_text(text, x, y, color, center=False):
   message = font.render(text, True, color)
   if center:
       text_rect = message.get_rect(center=(x, y))
       screen.blit(message, text_rect)
   else:
       screen.blit(message, (x, y))


prologue_text = (
        "In a distant galaxy, the shadow of chaos looms over the peaceful colony of Zorath. "
        "You, an elite pilot, have been tasked with defending the colony from invaders and "
        "uncovering the secret behind the mysterious Shadowfall.")


def narrative_screen(text):
   screen.fill(GREY)
   lines = []
   words = text.split(" ")
   line = ""
   for word in words:
       test_line = line + word + " "
       if font.size(test_line)[0] <= SCREEN_WIDTH - 40:
           line = test_line
       else:
           lines.append(line)
           line = word + " "
   if line:
       lines.append(line)

   y_offset = (SCREEN_HEIGHT // 2) - (len(lines) * 20)
   for i, line in enumerate(lines):
       draw_text(line.strip(), SCREEN_WIDTH // 2, y_offset + i * 40, WHITE, center=True)
   draw_text("Press SPACE to continue", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, WHITE, center=True)
   pygame.display.flip()

   waiting = True
   while waiting:
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False



# Main menu code
def main_menu():
   screen.fill(GREY)
   title_img=pygame.image.load("title2.png")
   title_img=pygame.transform.scale(title_img, (250, 188))
   screen.blit(title_img, (270 , 25))
   draw_text("Press 1 to Play Level 1", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, WHITE, center=True)
   if level_1_completed:
       draw_text("Press 2 to Play Level 2", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, WHITE, center=True)
   else:
       draw_text("Level 2 Locked - Complete Level 1", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, RED, center=True)
   draw_text("Press Q to Quit", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, WHITE, center=True)
   pygame.display.flip()


# Level 1 Game code (Game 1)
def level_1():
   global level_1_completed

   narrative_screen("As the first wave of enemy ships closes in, you must navigate your fighter through the debris field and survive the onslaught. The safety of Zorath depends on your skill and courage.")

   # Loading assests
   ship_img = pygame.image.load("spaceship.png")
   ship_img = pygame.transform.scale(ship_img, (50, 50))
   enemy_img = pygame.image.load("enemy.png")
   enemy_img = pygame.transform.scale(enemy_img, (50, 50))
   background = pygame.image.load("background.png")


   # Music controls (1)
   pygame.mixer.music.load("bgmusic.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.play(-1)
  

   # Initial game settings
   ship_x = SCREEN_WIDTH // 2
   ship_y = SCREEN_HEIGHT - 100
   ship_speed = 5

   obstacles = []
   obstacle_speed = 4
   laser = []

   score = 0
   running = True
   game_over = False
   game_completed = False

   # Level 1 specifiec funtions
   def spawn_obstacle():
       while True:
           x = random.randint(0, SCREEN_WIDTH - 50)
           y = -50
           new_obstacle = pygame.Rect(x, y, 50, 50)
           overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles)
           if not overlap:
               obstacles.append(new_obstacle)
               break


   def spawn_laser():
       x = random.randint(0, SCREEN_WIDTH - 10)
       y = -20
       laser.append(pygame.Rect(x, y, 10, 20))


    # LEVEL 1 MAIN LOOP
   while running:
       screen.fill(GREY)
       screen.blit(background, (0, 0))

       # Checking events
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

       keys = pygame.key.get_pressed()
       if not game_over and not game_completed:
           if keys[pygame.K_LEFT] and ship_x > 0:
               ship_x -= ship_speed
           if keys[pygame.K_RIGHT] and ship_x < SCREEN_WIDTH - 50:
               ship_x += ship_speed
           if keys[pygame.K_UP] and ship_y > 0:
               ship_y -= ship_speed
           if keys[pygame.K_DOWN] and ship_y < SCREEN_HEIGHT - 50:
               ship_y += ship_speed

           if random.randint(1, 20) == 1:
               spawn_obstacle()
           if random.randint(1, 30) == 1:
               spawn_laser()

           for obstacle in obstacles:
               obstacle.y += obstacle_speed
               if obstacle.colliderect(pygame.Rect(ship_x, ship_y, 50, 50)):
                   game_over = True
               if obstacle.y > SCREEN_HEIGHT:
                   obstacles.remove(obstacle)
           for fire in laser:
               fire.y += obstacle_speed + 2
               if fire.colliderect(pygame.Rect(ship_x, ship_y, 50, 50)):
                   game_over = True
               if fire.y > SCREEN_HEIGHT:
                   laser.remove(fire)

           screen.blit(ship_img, (ship_x, ship_y))
           for obstacle in obstacles:
               screen.blit(enemy_img, (obstacle.x, obstacle.y))
           for fire in laser:
               pygame.draw.rect(screen, RED, fire)

           score += 1
           draw_text(f"Score: {score}", 10, 10, WHITE)
            
            # Game completion check
           if score >= 2000:
               game_completed = True

       elif game_completed:
           level_1_completed = True # For level 2
           draw_text("Congratulations! You Escaped!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, GREEN, center=True)
           draw_text("Press M to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, center=True)
           if keys[pygame.K_m]:
               running = False
               pygame.mixer.music.stop()
               pygame.mixer.music.unload() # unload music everytime go to menu

       else:
           draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, RED, center=True)
           draw_text("Press R to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, center=True)
           draw_text("Press M to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE, center=True)
           pygame.mixer.music.stop()

           if keys[pygame.K_m]:
               pygame.mixer.music.unload() # unload music everytime go to menu
               running = False
           if keys[pygame.K_r]:
               obstacles.clear() # reset variables
               laser.clear()
               score = 0
               game_over = False
               ship_x = SCREEN_WIDTH // 2
               ship_y = SCREEN_HEIGHT - 100
               pygame.mixer.music.play(-1)

       pygame.display.flip()
       clock.tick(FPS)


# Level 2 Game code (Game 2)
def level_2():

   narrative_screen("With the enemy fleet neutralized, you land on their mothership. Armed only with The Excaliber and the finest magical powers in the galaxy, you must confront Azorath, the alien leader, and destroy the ultimate weapon. THE MECH BOSS!")

   # Loading assets for Level 2
   background = pygame.image.load("background2.png")
   player_img = pygame.image.load("player.png").convert_alpha()
   player_img = pygame.transform.scale(player_img, (50, 50))
   monster_img = pygame.image.load("monster2.png").convert_alpha()
   monster_img = pygame.transform.scale(monster_img, (60, 60))
   boss_img = pygame.image.load("boss.png").convert_alpha()
   boss_img = pygame.transform.scale(boss_img, (150, 150))
   orb_img = pygame.image.load("orb.png").convert_alpha()
   orb_img = pygame.transform.scale(orb_img, (15, 15))

   # Level 2 music controls
   pygame.mixer.music.load("bgmusic2.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.play(-1)

   # Variables for level 2
   player_x = 50
   player_y = SCREEN_HEIGHT - 150
   player_speed = 5
   player_jump = -24
   player_gravity = 1
   player_velocity_y = 0
   is_jumping = False
   health = 100

   monsters = []
   monster_speed = 2
   monster_spawn_rate = 60  


   boss_active = False
   boss_health = 200
   boss_x = SCREEN_WIDTH - 200
   boss_y = SCREEN_HEIGHT - 200
   boss_attack_rate = 85  
   boss_projectiles = []


   orbs = []
   orb_spawn_rate = 120 
   orbs_collected = 0

   platforms = [
       pygame.Rect(SCREEN_WIDTH + i * 300, random.randint(200, SCREEN_HEIGHT - 150), 200, 20)
       for i in range(15)
   ]
   platform_color = GREEN
   bottom_platform = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)  # bottom platform

   running = True
   game_over = False
   game_completed = False
   frame_count = 0
   platforms_passed = 0


   # Level 2 specific functions
   def spawn_monster():
       if random.random() < 0.3:
           monsters.append(pygame.Rect(SCREEN_WIDTH, bottom_platform.y - 50, 50, 50))
       else:
           platform = random.choice(platforms)
           monsters.append(pygame.Rect(platform.x + platform.width // 2, platform.y - 50, 50, 50))

   def spawn_orb():
       x = random.randint(100, SCREEN_WIDTH - 100)
       y = random.randint(200, 500)
       orbs.append(pygame.Rect(x, y, 15, 15))

   def boss_attack():
       boss_projectiles.append(pygame.Rect(boss_x, boss_y + 50, 20, 20))


   # MAIN GAME LOOP LEVEL 2
   while running:
       screen.fill(GREY)
       screen.blit(background, (0, 0))
       keys = pygame.key.get_pressed()

        # checking events
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

       if not game_over and not game_completed:
           if keys[pygame.K_LEFT] and player_x > 0:
               player_x -= player_speed
           if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:
               player_x += player_speed

           if not is_jumping:
               if keys[pygame.K_SPACE]:
                   player_velocity_y = player_jump
                   is_jumping = True
           player_velocity_y += player_gravity
           player_y += player_velocity_y

           on_ground = False
           for platform in platforms:
               if (pygame.Rect(player_x, player_y + 50, 50, 1).colliderect(platform)
                       and player_velocity_y >= 0):
                   player_y = platform.y - 50
                   player_velocity_y = 0
                   is_jumping = False
                   on_ground = True

           if (pygame.Rect(player_x, player_y + 50, 50, 1).colliderect(bottom_platform)
                   and player_velocity_y >= 0):
               player_y = bottom_platform.y - 50
               player_velocity_y = 0
               is_jumping = False
               on_ground = True

           if not on_ground:
               is_jumping = True

           for platform in platforms:
               platform.x -= 2

           if platforms and platforms[0].x + platforms[0].width < 0:
               platforms.pop(0)
               platforms.append(
                   pygame.Rect(
                       platforms[-1].x + 300,
                       random.randint(200, SCREEN_HEIGHT - 150),200,20,)
                       )
               platforms_passed += 1

           frame_count += 1
           if frame_count % monster_spawn_rate == 0 and not boss_active:
               spawn_monster()

           for monster in monsters[:]:
               monster.x -= monster_speed
               if monster.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                   health -= 10
                   monsters.remove(monster)
               elif monster.x < 0:
                   monsters.remove(monster)

           if platforms_passed >= 15 and not boss_active:
               boss_active = True
               monsters.clear()
               platforms.clear()

           if boss_active:
               if frame_count % orb_spawn_rate == 0:
                   spawn_orb()

               for orb in orbs[:]:
                   if orb.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                       orbs_collected += 1
                       orbs.remove(orb)

               if keys[pygame.K_z] and orbs_collected > 0:
                   boss_health -= 10
                   orbs_collected -= 1

               if frame_count % boss_attack_rate == 0:
                   boss_attack()

               for projectile in boss_projectiles[:]:
                   projectile.x -= 5
                   if projectile.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                       health -= 20
                       boss_projectiles.remove(projectile)
                   elif projectile.x < 0:
                       boss_projectiles.remove(projectile)

               if boss_health <= 0:
                   game_completed = True

           screen.blit(player_img, (player_x, player_y))
           pygame.draw.rect(screen, BLUE, bottom_platform)
           for platform in platforms:
               pygame.draw.rect(screen, platform_color, platform)
           for monster in monsters:
               screen.blit(monster_img, (monster.x, monster.y))
           if boss_active:
               screen.blit(boss_img, (boss_x, boss_y))
               for projectile in boss_projectiles:
                   pygame.draw.rect(screen, RED, projectile)
               for orb in orbs:
                   screen.blit(orb_img, (orb.x, orb.y))

           draw_text(f"Health: {health}", 10, 10, WHITE)
           if boss_active:
               draw_text(f"Orbs: {orbs_collected}", 10, 40, YELLOW)
               draw_text(f"Boss Health: {boss_health}", SCREEN_WIDTH - 200, 10, RED)

           if health <= 0:
               game_over = True

       elif game_completed:
           screen.fill(GREY)
           draw_text("You Defeated the Boss!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, GREEN, center=True)
           draw_text("Press M to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, center=True)
           if keys[pygame.K_m]:
                    running = False
           pygame.display.flip()
           pygame.mixer.music.stop()
            
       elif game_over:
           screen.fill(GREY)
           draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, RED, center=True)
           draw_text("Press R to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, center=True)
           draw_text("Press M to Return to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE, center=True)
           pygame.display.flip()
           pygame.mixer.music.stop()

           if keys[pygame.K_m]:
                    running = False
           elif keys[pygame.K_r]:
                platforms = [
                    pygame.Rect(SCREEN_WIDTH + i * 300, random.randint(200, SCREEN_HEIGHT - 150), 200, 20)
                    for i in range(15)]
                monsters.clear() # resetting varaibles
                orbs.clear()
                boss_projectiles.clear()
                boss_active = False
                boss_health = 200
                orbs_collected = 0
                platforms_passed = 0
                player_x = 50
                player_y = SCREEN_HEIGHT - 150
                health = 100
                game_over = False
                frame_count = 0
                pygame.mixer.music.play(-1)

       pygame.display.flip()
       clock.tick(FPS)


# Main game loop (inc. menu)
narrative_screen(prologue_text)

while True:
   if menu_active:
       main_menu()

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

   keys = pygame.key.get_pressed()
   if keys[pygame.K_1]:
       menu_active = False
       level_1()
       menu_active = True
   if keys[pygame.K_2] and level_1_completed:
       menu_active = False
       level_2()
       menu_active = True
   if keys[pygame.K_q]:
       pygame.quit()
       sys.exit()

   clock.tick(FPS)