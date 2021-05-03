def reset_game():
    global category,text,guessed_correct_positions,strike,game_over,letters
    global correct,wrong,attemps
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