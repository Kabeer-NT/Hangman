import pygame
from pygame import mixer
import random

pygame.init()
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption("Hangman")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


# Random Word from File
def random_word():
    f = open("{}.txt".format(category), "r")
    words = f.readlines()
    t = random.choice(words)
    t = t[:len(t) - 1]
    t = t.upper()
    return t


# Barebones
head = pygame.image.load("header.png")
header_font = pygame.font.Font("codebold.otf", 100)
title = header_font.render("H A N G M A N", True, (0, 0, 205))
category = random.choice(["animals", "colors","countries"])
text = random_word()
guessed_correct_positions = []
strike = 0
game_over = False
letters = list(text)
try:
    while True:
        letters.remove(" ")
except ValueError:
    pass
correct = []
wrong = []
attempts = []
background = pygame.image.load("white_paper.jpg")

# Game Over Text
word = pygame.font.Font("game_over.ttf", 300)

# YOU WIN Text
prompt = pygame.font.Font("sketchup.ttf", 200)

# Category Text
hint = pygame.font.Font("freesansbold.ttf", 30)


def num_unique_chars(string_x):
    unique = []
    count = 0
    for i in range(len(string_x)):
        if string_x[i] not in unique and string_x[i] != " ":
            unique.append(string_x[i])
            count += 1
    return count


def game_over_text():
    displaying = word.render("GAME OVER", True, "red")
    screen.blit(displaying, (250, 300))


def you_win_text():
    prompting = prompt.render("YOU WIN", True, "purple")
    screen.blit(prompting, (330, 300))


def draw_hangman(num):
    if num >= 1:
        pygame.draw.circle(screen, "black", (1100, 190), 40, 1)
    if num >= 2:
        pygame.draw.line(screen, "black", (1100, 230), (1100, 380))
    if num >= 3:
        pygame.draw.line(screen, "black", (1100, 305), (1150, 275))
    if num >= 4:
        pygame.draw.line(screen, "black", (1100, 305), (1050, 275))
    if num >= 5:
        pygame.draw.line(screen, "black", (1100, 380), (1150, 415))
    if num >= 6:
        pygame.draw.line(screen, "black", (1100, 380), (1050, 415))


def find_indexes(string_x, substring_x):
    lst = []
    for i in range(len(string_x)):
        if string_x[i] == substring_x:
            lst.append(i)
    return lst


def draw_box_string(word):
    box_length = 800 // len(word)
    word_text = pygame.font.Font("freesansbold.ttf", box_length // 2)
    x = 50
    for i in range(len(word)):
        if i in guessed_correct_positions or game_over == True:
            printer = word_text.render(word[i], True, (0, 0, 0))
            pygame.draw.line(screen, "black", (x + box_length // 7, 300), (x + box_length // 2, 300))
            screen.blit(printer, (x + box_length // 7, 300 - box_length // 2))

        elif word[i] == " ":
            printer = word_text.render("", True, (0, 0, 0))
            # pygame.draw.line(screen, "black", (x + box_length // 7, 300), (x + box_length // 2, 300))
            screen.blit(printer, (x + box_length // 7, 300 - box_length // 2))

        else:
            printer = word_text.render("--", True, (0, 0, 0))
            pygame.draw.line(screen, "black", (x + box_length // 7, 300), (x + box_length // 2, 300))
            screen.blit(printer, (x + box_length // 7, 300 - box_length // 2))
        x += box_length


def draw_stand():
    pygame.draw.lines(screen, "black", False, [(1100, 450), (1200, 450), (1300, 450)])
    pygame.draw.line(screen, "black", (1200, 100), (1200, 450))
    pygame.draw.line(screen, "black", (1200, 100), (1100, 100))
    pygame.draw.line(screen, "black", (1100, 100), (1100, 150))


def draw_boxes():
    x = 0
    for i in range(13):
        pygame.draw.rect(screen, "black", (x, 500, 100, 100), 1)
        pygame.draw.rect(screen, "black", (x, 600, 100, 100), 1)
        if chr(button_value(x + 1, 501)) in correct:
            pygame.draw.rect(screen, (50, 205, 50), (x, 500, 100, 100))
        if chr(button_value(x + 1, 601)) in correct:
            pygame.draw.rect(screen, (50, 205, 50), (x, 600, 100, 100))
        if chr(button_value(x + 1, 501)) in wrong:
            pygame.draw.rect(screen, (210, 4, 45), (x, 500, 100, 100))
        if chr(button_value(x + 1, 601)) in wrong:
            pygame.draw.rect(screen, (210, 4, 45), (x, 600, 100, 100))
        pygame.draw.rect(screen, "black", (x, 500, 100, 100), 1)
        pygame.draw.rect(screen, "black", (x, 600, 100, 100), 1)

        x += 100


def button_value(x, y):
    button_val = 0
    if 500 < y < 600:
        button_val += 1
    if 600 < y < 700:
        button_val += 14

    for i in range(1, 13):
        if i * 100 < x < (i + 1) * 100:
            button_val += i
    button_val += 64
    return button_val


def print_numbers():
    number_text = pygame.font.Font("freesansbold.ttf", 16)
    x = 45
    y = 550
    for i in range(13):
        numbers = number_text.render(chr(button_value(x, y)), True, (0, 0, 0))
        screen.blit(numbers, (x, y))
        x += 100
    x = 45
    y = 650
    for i in range(13):
        numbers = number_text.render(chr(button_value(x, y)), True, (0, 0, 0))
        screen.blit(numbers, (x, y))
        x += 100


def guess(x, y):
    ascii_val = button_value(x, y)
    if str(chr(ascii_val)) in text:
        indexes = find_indexes(text, chr(ascii_val))
        for _ in indexes:
            guessed_correct_positions.append(_)
        return True
    else:
        return False


def reset_game():
    global category, text, guessed_correct_positions, strike, game_over, letters
    global correct, wrong, attempts
    category = random.choice(["animals", "colors","countries"])
    text = random_word()
    guessed_correct_positions = []
    strike = 0
    game_over = False
    letters = list(text)
    try:
        while True:
            letters.remove(" ")
    except ValueError:
        pass
    correct = []
    wrong = []
    attempts = []

    if len(text) == 0:
        text = random_word()


running = True
# Main Loop
while running:
    restart = False
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(title, (300, 0))

    # screen.blit(title, (300, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y > 500:
                if not guess(x, y):
                    wrong_sound = mixer.Sound("wrong.wav")
                    wrong_sound.play()
                    wrong += chr(button_value(x, y))
                    if chr(button_value(x, y)) not in attempts:
                        strike += 1
                else:
                    correct_sound = mixer.Sound("correct.wav")
                    correct_sound.play()
                    correct += chr(button_value(x, y))
                    try:
                        while True:
                            letters.remove(chr(button_value(x, y)))
                    except ValueError:
                        pass
                attempts += chr(button_value(x, y))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    # Conditions
    if strike == 6:
        game_over = True
        game_over_text()
    if not letters:
        game_over = True
        you_win_text()
    if game_over and restart == True:
        reset_game()

    # Functions
    hint_text = hint.render("HINT = {}".format(category.title()), True, (34, 139, 34))
    screen.blit(hint_text, (0, 460))

    draw_stand()
    draw_boxes()
    print_numbers()
    draw_box_string(text)
    draw_hangman(strike)
    pygame.display.update()
