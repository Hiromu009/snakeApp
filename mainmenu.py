import pygame
import os
import subprocess
import sys
from utilities import init_pygame
from scoreboard import display_top_scores_gui
# from snake import start_game


def main_menu():
    screen, screen_size = init_pygame()
    pygame.display.set_caption("Snake Game Menu")

    background_image = pygame.image.load('image/mainmenuimag.png')
    background_image = pygame.transform.scale(background_image, screen_size)  # 画像サイズを画面に合わせる

    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 30)  # ルールテキスト用の小さいフォント

    play_text = font.render('Play', True, (0, 0, 0))
    score_text = font.render('Score', True, (0, 0, 0))
    quit_text = font.render('Quit', True, (0, 0, 0))

    # ゲームのルールを記載するテキスト
    rules_text = [
        "Rules:",
        "1. Use arrow keys to move the snake.",
        "2. Eat the heart from the direction of the arrow.",
        "3. The walls are passable, so don't be afraid to go through them."
    ]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    pygame.quit()  # pygame 環境をクリーンアップ
                    os.system("python snake.py")  # snake.py スクリプトを直接実行
                    return  # main_menu関数から抜ける
                elif score_button.collidepoint(mouse_pos):
                    display_top_scores_gui()
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        screen.blit(background_image, (0, 0))

        # ボタンの位置を左側に寄せる
        buttons_x = 50  # ボタンのX座標を指定
        play_button = pygame.Rect(buttons_x, 150, 200, 50)
        score_button = pygame.Rect(buttons_x, 220, 200, 50)
        quit_button = pygame.Rect(buttons_x, 290, 200, 50)

        pygame.draw.rect(screen, (0, 255, 0), play_button)
        pygame.draw.rect(screen, (0, 255, 0), score_button)
        pygame.draw.rect(screen, (0, 255, 0), quit_button)

        screen.blit(play_text, (play_button.x + 50, play_button.y + 10))
        screen.blit(score_text, (score_button.x + 50, score_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

        # 右側にルールを記載
        for i, line in enumerate(rules_text):
            rule_text = small_font.render(line, True, (0, 0, 0))
            screen.blit(rule_text, (400, 30 + i * 30))  # Y座標はルールごとに30ピクセルずつ下げる

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main_menu()


