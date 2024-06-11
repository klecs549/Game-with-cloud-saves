import pygame
import sys
import json
from code.settings import *
from code.level import Level
import requests


# save = [3, 2]


class Game:
    def __init__(self, save=None):
        self.screen = SCREEN
        pygame.display.set_caption("Project")
        self.clock = pygame.time.Clock()
        # print(save)
        self.level = Level(save)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return self.level.save
                    # sys.exit()

            self.screen.fill((30, 30, 30))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


class Load_save:
    def __init__(self):
        SCREEN.fill((94, 129, 162))
        self.text = pygame.font.Font(None, 50)
        self.ng = self.text.render('New Game', False, (0, 0, 0))
        self.ng_rect = self.ng.get_rect(center=(WIDTH / 3, HEIGHT / 2))
        self.choise = None

    def run(self):
        SCREEN.blit(self.ng, self.ng_rect)
        if self.ng_rect.collidepoint(pygame.mouse.get_pos()):
            return False
        pygame.display.update()
        return True, self.choise


def prepare():
    while True:
        option = input("Would you like to do(New game,Offline save, Cloud save): ")
        if option == "New game":
            return [
                [98, 17],
                {"1824": 0, "4512": 0, "8496": 1},
                {"Sword": 0, "Hammer": 0, "Dash": 0},
                {"GiantFrog": 0, "GiantRacoon": 0, "GiantRacoonGold": 0}]
        elif option == "Cloud save":
            try:
                r = requests.get("http://127.0.0.1:8000/save/get-save/")
                saves = []
                id = 1
                for data in r.json()[::-1]:
                    if data["user"] == 1:
                        print(id, data["data"])
                        saves.append(data["data"])
                        id += 1
                while True:
                    option = input("Choose a save: ")
                    try:
                        return saves[int(option) - 1]
                    except IndexError:
                        print("Invalid save")
            except ConnectionRefusedError:
                print("Server not available")
        elif option == "Offline save":
            with open("save.json") as f:
                try:
                    return json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    ...


if __name__ == "__main__":
    save = prepare()
    # with open("save.json") as f:
    #     save = json.loads(f.read())
    game = Game(save)
    save = game.run()
    with open("save.json", "w") as file:
        file.write(json.dumps(save))
    requests.post("http://127.0.0.1:8000/save/create-save/",
                  data={
                      "name": "Save",
                      "user": 1,
                      "data": json.dumps(save)
                  })
    sys.exit()
