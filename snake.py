import pygame, sys, time, random
from mainmenu import main_menu


speed = 13

frame_width = 1280  # 仮の画面幅
frame_height = 720  # 仮の画面高さ
square_size = 36

# 実際のフレームサイズをスクエアサイズの整数倍に調整
frame_size_x = (frame_width // square_size) * square_size
frame_size_y = (frame_height // square_size) * square_size

check_error = pygame.init()

if check_error[1] > 0:
    print(f"エラーが発生しました {check_error[1]}")
else:
    print("ゲームの初期化に成功しました")

pygame.display.set_caption("Snake game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()


def init_vars():
    global head_pos, snake_body, heart_pos, heart_spawn, score, direction, current_arrow_direction
    direction = "RIGHT"
    initial_x = (frame_size_x // square_size // 2) * square_size
    initial_y = (frame_size_y // square_size // 2) * square_size
    head_pos = [initial_x, initial_y]
    snake_body = [[initial_x, initial_y]]
    heart_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                 random.randrange(1, (frame_size_y // square_size)) * square_size]
    heart_spawn = True
    current_arrow_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    score = 0


init_vars()

def load_heart_image(path):
    # 画像をロードしてサイズを調整
    try:
        heart_image = pygame.image.load(path)
        # 元の画像のアスペクト比を維持しつつ、グリッドのサイズの1.2倍の新しいサイズに合わせるための計算
        scale_factor = 1.5  # サイズを1.2倍にする
        new_size = int(square_size * scale_factor)
        # アスペクト比を維持するために元のサイズを基に新しいサイズを計算
        original_width = heart_image.get_width()
        original_height = heart_image.get_height()
        aspect_ratio = original_height / original_width
        new_height = int(new_size * aspect_ratio)
        new_width = new_size
        if new_height > new_size:
            # 縦長の場合、幅を基準に高さを調整
            new_height = new_size
            new_width = int(new_size / aspect_ratio)
        # サイズを変更した画像を生成
        heart_image = pygame.transform.scale(heart_image, (new_width, new_height))
        return heart_image
    except pygame.error as e:
        print(f"画像の読み込みに失敗しました: {e}")
        sys.exit()

heart_image = load_heart_image('image/24789657.png')

def load_background_image(path, frame_size):
    try:
        # 背景画像をロード
        background_image = pygame.image.load(path)
        # ゲームウィンドウに合わせて画像のサイズを変更
        background_image = pygame.transform.scale(background_image, frame_size)
        return background_image
    except pygame.error as e:
        print(f"背景画像の読み込みに失敗しました: {e}")
        sys.exit()

def load_eye_image(path, size=(60, 60)):
    try:
        # 目の画像をロードしてサイズを調整
        eye_image = pygame.image.load(path)
        eye_image = pygame.transform.scale(eye_image, size)
        return eye_image
    except pygame.error as e:
        print(f"目の画像の読み込みに失敗しました: {e}")
        sys.exit()


def spawn_heart():
    global heart_pos, heart_spawn, current_arrow_direction
    # ハートのスポーン位置をグリッド上に正確に合わせる
    heart_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                 random.randrange(1, (frame_size_y // square_size)) * square_size]
    heart_spawn = True
    current_arrow_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)


def game_over_screen():
    global game_window, fps_controller, score

    input_active = True  # イニシャル入力が可能な状態
    initials = ""  # ユーザーが入力するイニシャル
    options = ["New Game", "Main Menu", "Quit"]
    selected_option = 0  # 選択されているオプション
    message = "Game Over! Your score: " + str(score)  # スコア表示メッセージ

    while True:
        game_window.fill(black)

        # スコア表示
        score_surface = pygame.font.SysFont('consolas', 35).render(message, True, white)
        score_rect = score_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2 - 120))
        game_window.blit(score_surface, score_rect)

        # イニシャル入力とオプション選択のメッセージ
        if input_active:
            initials_msg = "Enter initials: " + initials + "_" * (3 - len(initials))
        else:
            initials_msg = "Select Option:"
        message_surface = pygame.font.SysFont('consolas', 35).render(initials_msg, True, white)
        message_rect = message_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2 - 60))
        game_window.blit(message_surface, message_rect)

        # オプション表示
        if not input_active:
            for index, option in enumerate(options):
                color = green if index == selected_option else white
                option_surface = pygame.font.SysFont('consolas', 35).render(option, True, color)
                option_rect = option_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2 + 40 * index))
                game_window.blit(option_surface, option_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and len(initials) == 3:
                        input_active = False  # イニシャル入力終了
                        # ここでスコアとイニシャルを保存する処理を実装できます
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1] if len(initials) > 0 else ''
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()
                else:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected_option]  # 選択されたオプションに応じた行動を実行

        pygame.display.flip()
        fps_controller.tick(30)  # フレームレートを制御


def save_score(score):
    initials = ''
    while len(initials) != 3:
        initials = input("Enter your initials (3 letters): ").upper()
        if len(initials) != 3:
            print("Invalid input. Please enter exactly 3 letters.")

    with open("scores.txt", "a") as file:
        file.write(f"{initials} {score}\n")


def draw_arrow(direction, position):
    font_size = 45# フォントサイズ
    font = pygame.font.SysFont('arial', font_size)
    font.set_bold(True)  # フォントを太字に設定
    arrow_color = pygame.Color(0, 0, 0)  # 矢印の色

    if direction == 'UP':
        arrow = "↑"
    elif direction == 'DOWN':
        arrow = "↓"
    elif direction == 'LEFT':
        arrow = "←"
    elif direction == 'RIGHT':
        arrow = "→"

    text = font.render(arrow, True, arrow_color)
    text_rect = text.get_rect(center=position)
    game_window.blit(text, text_rect)



def draw_heart_and_arrow():
    # ハートの中心座標を計算（画像の左上角の座標を調整）
    heart_center_x = heart_pos[0] + (square_size - heart_image.get_width()) // 2
    heart_center_y = heart_pos[1] + (square_size - heart_image.get_height()) // 2
    game_window.blit(heart_image, (heart_center_x, heart_center_y))

    # 矢印をハートの中心に描画
    arrow_center = (heart_pos[0] + square_size // 2, heart_pos[1] + square_size // 2)
    draw_arrow(current_arrow_direction, arrow_center)


game_over = False

def draw_snake_eyes(window, eyes_image, snake_head_pos, direction):
    # 目のサイズに基づいてオフセットを計算
    eye_offset_x = eyes_image.get_width() // 2
    eye_offset_y = eyes_image.get_height() // 2

    # 蛇の頭の中心座標を計算
    eyes_center_x = snake_head_pos[0] + square_size // 2 - eye_offset_x
    eyes_center_y = snake_head_pos[1] + square_size // 2 - eye_offset_y

    # 目の画像を蛇の頭の向きに合わせて回転させる
    if direction == 'UP':
        rotated_eyes_image = pygame.transform.rotate(eyes_image, 0)
    elif direction == 'DOWN':
        rotated_eyes_image = pygame.transform.rotate(eyes_image, 180)
    elif direction == 'LEFT':
        rotated_eyes_image = pygame.transform.rotate(eyes_image, 90)
    elif direction == 'RIGHT':
        rotated_eyes_image = pygame.transform.rotate(eyes_image, -90)

    # 回転させた画像を蛇の頭の位置に描画する
    window.blit(rotated_eyes_image, (eyes_center_x, eyes_center_y))

# 目の画像をロード（サイズを適宜調整してください）
eyes_image = load_eye_image('image/eyes_image.png', size=(60, 60)) # 目の画像のサイズを調整


def draw_grid():
    grid_color = pygame.Color(200, 200, 200)  # グリッドの色
    for x in range(0, frame_size_x, square_size):
        pygame.draw.line(game_window, grid_color, (x, 0), (x, frame_size_y))
    for y in range(0, frame_size_y, square_size):
        pygame.draw.line(game_window, grid_color, (0, y), (frame_size_x, y))


background_image = load_background_image('image/1400912.png', (frame_size_x, frame_size_y))


def game_over_screen():
    global game_window, fps_controller, score

    input_active = True  # イニシャル入力がアクティブ
    initials = ""  # ユーザーが入力するイニシャル
    options = ["New Game", "Main Menu", "Quit"]
    selected_option = 0  # 現在選択されているオプションのインデックス
    message = "Game Over! Press SPACE to enter initials."  # 初期メッセージ

    while True:
        game_window.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and len(initials) == 3:
                        save_score(initials, score)
                        input_active = False  # イニシャル入力を終了
                        message = "Select Option:"  # オプション選択のメッセージに変更
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()
                else:  # イニシャル入力が終了し、オプション選択がアクティブ
                    if event.key == pygame.K_w:
                        selected_option = (selected_option - 1) % len(options)  # 上のオプションを選択
                    elif event.key == pygame.K_s:
                        selected_option = (selected_option + 1) % len(options)  # 下のオプションを選択
                    elif event.key == pygame.K_RETURN:
                        return options[selected_option]  # 選択したオプションを返す

        # イニシャル入力とオプション選択の表示
        if input_active:
            display_message = f"Enter initials: {initials + '_ ' * (3 - len(initials))}"
        else:
            display_message = message
        message_surface = pygame.font.SysFont('consolas', 35).render(display_message, True, white)
        message_rect = message_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2 - 40))
        game_window.blit(message_surface, message_rect)

        # オプション選択がアクティブな場合にのみオプションを表示
        if not input_active:
            for index, option in enumerate(options):
                color = green if index == selected_option else white
                option_surface = pygame.font.SysFont('consolas', 35).render(option, True, color)
                option_rect = option_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2 + 40 * index))
                game_window.blit(option_surface, option_rect)

        pygame.display.flip()
        fps_controller.tick(speed)


def save_score(initials, score):
    # Assuming this function writes the initials and score to a file
    with open("scores.txt", "a") as file:
        file.write(f"{initials} {score}\n")

def start_game():
    init_vars()
    game_over = False

def pause_game():
    paused = True
    texts = ["Paused.", "Press C to continue,", "Q to quit,", "R to restart,", "M for menu"]
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    paused = False
                    start_game()
                elif event.key == pygame.K_m:
                    paused = False
                    main_menu()

        game_window.fill(black)
        pause_font = pygame.font.Font(None, 48)

        # テキスト行の総高さを計算（すべてのテキスト行と間隔の合計）
        total_height = sum(pause_font.size(text)[1] for text in texts) + (len(texts) - 1) * 10  # テキスト間の間隔を10ピクセルとする

        # 最初のテキスト行の開始Y座標
        start_y = frame_size_y / 2 - total_height / 2

        for i, text in enumerate(texts):
            pause_surface = pause_font.render(text, True, white)
            pause_rect = pause_surface.get_rect(center=(frame_size_x / 2, start_y + i * (pause_font.size(text)[1] + 10)))
            game_window.blit(pause_surface, pause_rect)

        pygame.display.flip()
        fps_controller.tick(5)

def start_game():
    global direction, head_pos, snake_body, heart_pos, heart_spawn, score, current_arrow_direction, game_over
    init_vars()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != "DOWN":
            direction = "UP"
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != "UP":
            direction = "DOWN"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != "LEFT":
            direction = "RIGHT"
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != "RIGHT":
            direction = "LEFT"

        if direction == "UP":
            head_pos[1] -= square_size
        elif direction == "DOWN":
            head_pos[1] += square_size
        elif direction == "RIGHT":
            head_pos[0] += square_size
        else:  # LEFT
            head_pos[0] -= square_size

        # 壁に当たった時の処理を修正
        if head_pos[0] < 0:
            head_pos[0] = frame_size_x - square_size
        elif head_pos[0] >= frame_size_x:
            head_pos[0] = 0
        if head_pos[1] < 0:
            head_pos[1] = frame_size_y - square_size
        elif head_pos[1] >= frame_size_y:
            head_pos[1] = 0

        snake_body.insert(0, list(head_pos))  # 頭の位置をスネークの体の先頭に追加

        # ハートを取得したかどうかをチェック
        if head_pos[0] == heart_pos[0] and head_pos[1] == heart_pos[1] and direction == current_arrow_direction:
            score += 100
            heart_spawn = False
        # ハートを再スポーンする
        else:
            snake_body.pop()  # ハートを取得していない場合、スネークの末尾を削除

        if not heart_spawn:
            spawn_heart()

        game_window.blit(background_image, (0, 0))
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0] + 2, pos[1] + 2, square_size - 2, square_size - 2))


        draw_snake_eyes(game_window, eyes_image, snake_body[0], direction)
        draw_grid()
        draw_heart_and_arrow()
        show_score(1, black, 'consolas', 20)

        pygame.display.update()
        fps_controller.tick(speed)

        for block in snake_body[1:]:
            if head_pos[0] == block[0] and head_pos[1] == block[1]:
                game_over = True

            # ゲームオーバー時の処理
        if game_over:
            action = game_over_screen()  # ゲームオーバー画面を表示してユーザーの選択を取得
            if action == "New Game":
                init_vars()  # ゲーム変数を初期化して新しいゲームを開始
                game_over = False  # ゲームオーバー状態をリセット
                continue  # メインループの先頭に戻る
            elif action == "Main Menu":
                main_menu()  # mainmenu.py 内のメインメニュー関数を呼び出してメニューに戻る
                break  # ゲームループを終了（メインメニューに戻る）
            elif action == "Quit":
                pygame.quit()
                sys.exit()

        if keys[pygame.K_p]:
            pause_game()


if __name__ == "__main__":
    start_game()