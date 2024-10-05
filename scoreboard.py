import os, pygame, sys
from utilities import init_pygame

def display_top_scores_gui():
    screen, screen_size = init_pygame()
    pygame.display.set_caption("Top Scores")

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    background_image = pygame.image.load("image/1400912.png")  # 背景画像のパスを適宜変更
    background_image = pygame.transform.scale(background_image, screen_size)  # 画面サイズに合わせてリサイズ

    # "Main Menu" ボタンの設定
    button_color = (0, 255, 0)
    button_rect = pygame.Rect(screen_size[0] / 2 - 100, 550, 200, 50)
    button_text = font.render('Main Menu', True, (255, 255, 255))

    if not os.path.exists("scores.txt"):
        scores = []
    else:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
        scores = [(int(score), initials) for initials, score in [line.strip().split() for line in scores]]
        scores.sort(reverse=True)

    while len(scores) < 5:
        scores.append((0, "----"))

    top_scores = scores[:5]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    print("Returning to main menu...")
                    running = False  # この行をループ内に移動

        screen.blit(background_image, (0, 0))

        # スコアを中央に表示
        for index, (score, initials) in enumerate(top_scores, start=1):
            text = font.render(f"{index}. {initials} - {score}", True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen_size[0] / 2, 50 + index * 60))
            screen.blit(text, text_rect)

        # メインメニューボタンを描画
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.display.flip()
        clock.tick(60)



