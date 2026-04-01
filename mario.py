import pygame
import sys

# --- AYARLAR ---
WIDTH, HEIGHT = 800, 450
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
GRAVITY = 0.8
JUMP_STRENGTH = -16

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- GÖRSELLER ---
try:
    mario_img = pygame.image.load("mario.png").convert_alpha()
    mario_img = pygame.transform.scale(mario_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    image_loaded = True
except:
    image_loaded = False
    mario_img = None

# --- DEĞİŞKENLER ---
player_rect = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
player_vel_y = 0
is_jumping = False
camera_x = 0
facing_right = True
lives = 3  # CAN SİSTEMİ

# Platformlar
platforms = [
    pygame.Rect(0, 400, 3000, 50),
    pygame.Rect(400, 300, 200, 30),
    pygame.Rect(700, 220, 150, 30)
]

# Düşman (Goomba)
enemy_rect = pygame.Rect(600, 360, 40, 40)
enemy_speed = 3

def main():
    global player_vel_y, is_jumping, camera_x, facing_right, enemy_speed, lives
    
    while True:
        screen.fill((135, 206, 235)) # Gökyüzü Mavisi
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        speed = 10 if keys[pygame.K_LSHIFT] else 6
        
        if keys[pygame.K_LEFT]:
            player_rect.x -= speed
            facing_right = False
        if keys[pygame.K_RIGHT]:
            player_rect.x += speed
            facing_right = True
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not is_jumping:
            player_vel_y = JUMP_STRENGTH
            is_jumping = True

        # Fizik ve Çarpışma
        player_vel_y += GRAVITY
        player_rect.y += player_vel_y

        on_ground = False
        for plat in platforms:
            if player_rect.colliderect(plat):
                if player_vel_y > 0:
                    player_rect.bottom = plat.top
                    player_vel_y = 0
                    on_ground = True
                elif player_vel_y < 0:
                    player_rect.top = plat.bottom
                    player_vel_y = 0
        if on_ground: is_jumping = False

        # Düşman Hareketi
        enemy_rect.x += enemy_speed
        if enemy_rect.x > 800 or enemy_rect.x < 400:
            enemy_speed *= -1

        # --- ÇARPIŞMA (Düşman vs Mario) ---
        if player_rect.colliderect(enemy_rect):
            # Üstüne zıplama kontrolü
            if player_vel_y > 0 and player_rect.bottom < enemy_rect.centery + 10:
                enemy_rect.x = -1000 # Düşman öldü
                player_vel_y = -10
            else:
                # Can kaybetme
                lives -= 1
                player_rect.x, player_rect.y = 100, 300 # Başlangıca dön
                pygame.time.delay(500) # Yarım saniye bekle
                if lives <= 0:
                    print("OYUN BİTTİ!")
                    lives = 3 # Oyunu sıfırla

        # Kamera
        camera_x = player_rect.centerx - WIDTH // 2

        # Çizimler
        for plat in platforms:
            pygame.draw.rect(screen, (139, 69, 19), (plat.x - camera_x, plat.y, plat.width, plat.height))
        
        pygame.draw.rect(screen, (128, 0, 128), (enemy_rect.x - camera_x, enemy_rect.y, 40, 40))
            
        if image_loaded and mario_img:
            display_img = mario_img if facing_right else pygame.transform.flip(mario_img, True, False)
            screen.blit(display_img, (player_rect.x - camera_x, player_rect.y))
        
        # CAN GÖSTERGESİ
        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"CAN: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
