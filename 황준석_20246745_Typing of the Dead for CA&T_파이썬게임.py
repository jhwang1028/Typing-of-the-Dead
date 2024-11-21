# -*- coding: utf-8 -*-
import pygame
import random
import requests
from bs4 import BeautifulSoup
import certifi
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress the InsecureRequestWarning only if necessary
warnings.simplefilter('ignore', InsecureRequestWarning)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1920, 1080  # Adjusted screen size to 1920x1080
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chung-Ang University Department of Art and Engineering")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Load the font that supports Hangul characters
font_path = "NotoSansKR-VariableFont_wght.ttf"
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path, 24)

# Load Korean text from the internet
def get_korean_text():
    url = "https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=1700"
    try:
        response = requests.get(url, verify=certifi.where())
    except requests.exceptions.SSLError:
        # Log SSL error and retry without verification
        print("SSL verification failed. Retrying without verification.")
        response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ''
    for paragraph in paragraphs:
        text += paragraph.get_text()
    return text

korean_text = get_korean_text()
print("Fetched Korean text:", korean_text[:200], "...")  # Debug: print the first 200 characters

# Extract words from the Korean text
words = korean_text.split()
words = [word for word in words if any('가' <= char <= '힣' for char in word)]
print("Extracted words:", words[:10])  # Debug: print the first 10 words

# Check if words list is empty
if not words:
    raise ValueError("No Korean words found in the fetched text.")

# Set up the game variables
clock = pygame.time.Clock()
fall_speed = 0.5  # Adjusted fall speed to make the text fall a little faster
score = 0
input_text = ''

class FallingWord:
    def __init__(self, word):
        self.word = word
        self.text_surface = font.render(self.word, True, white)
        self.width, self.height = self.text_surface.get_size()
        self.x = random.randint(0, width - self.width)
        self.y = random.randint(-100, -40)
        self.speed = random.uniform(0.2, fall_speed)  # Adjusted speed range to increase falling speed

    def draw(self, win):
        win.blit(self.text_surface, (self.x, self.y))

    def fall(self):
        self.y += self.speed

def draw_window(falling_words, score, input_text):
    win.fill(black)
    for word in falling_words:
        word.draw(win)
    score_text = small_font.render("Score: " + str(score), True, white)
    win.blit(score_text, (10, 10))
    input_text_render = small_font.render(input_text, True, white)
    win.blit(input_text_render, (10, height - 50))
    pygame.display.update()

def main():
    global fall_speed, score, input_text
    run = True
    falling_words = [FallingWord(random.choice(words)) for _ in range(10)]

    while run:
        clock.tick(90)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.TEXTINPUT:
                input_text += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for word in falling_words:
                        if input_text == word.word:
                            score += 1
                            fall_speed += 0.05
                            falling_words.remove(word)
                            falling_words.append(FallingWord(random.choice(words)))
                            break
                    input_text = ''  # Clear the input text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

        for word in falling_words:
            word.fall()
            if word.y > height:
                run = False

        draw_window(falling_words, score, input_text)

    pygame.quit()

if __name__ == "__main__":
    main()
