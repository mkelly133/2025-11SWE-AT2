import random

rooms = {
    1: [2, 4],
    2: [1, 3, 5],
    3: [2,6],
    4: [7, 5, 1],
    5: [4,8, 6, 2],
    6: [5, 9, 3],
    7: [4, 8],
    8: [7, 5, 9],
    9: [6, 8]
    }

class Character:
    def __init__(self, location):
        self.move_to(location)
    
    def move_to(self, location):
        self.location = location

class Player(Character):
    def __init__(self):
        self.arrows = 3
        super().__init__(1)
    
    def move_to(self, location):
        self.location = location
        self.nearby = rooms[location]
    
    def shoot(self):
        if self.arrows > 1:
            self.arrows -= 1
            return True
        else:
            return False
        
class Wumpus(Character):
    def __init__(self, location):
        super().__init__(location)

    def flee(self, player):
        while True:
            new_location = random.choice(list(rooms.keys()))
            if not new_location == self.location and not new_location == player.location:
                self.move_to(new_location)
                break

class HuntTheWumpus:
    def __init__(self):
        self.rooms = rooms
        self.new_game()
    
    def new_game(self):
        self.player = Player()
        self.wumpus = Wumpus(random.choice(list(self.rooms.keys())))
        self.game_on = True
        return "Welcome to Hunt the Wumpus!"
    
    def move(self, direction):
        if direction in self.player.nearby:
            self.player.move_to(direction)
            message = f"You are now in Room {direction}. "
            if self.check_for_wumpus():
                return f"The wumpus got you in Room {direction}!"
            if self.wumpus.location in self.player.nearby: ##Switch
                message += "You smell a wumpus. "
            return message
        else:
            return f"You are in room {self.player.location}, you can't go to room {direction}."
        
    def shoot_arrow(self, direction):
        if self.player.shoot():
            if direction == self.wumpus.location:
                self.game_on = False
                return "Congratulations! You defeated the Wumpus."
            else:
                self.wumpus.flee(self.player)
                #self.wumpus.move_to(random.choice(list(rooms.keys())))
                return f"You missed the Wumpus! You have {self.player.arrows} arrows left and the Wumpus has fled..."
        self.game_on = False
        return "You missed the Wumpus! You have no arrows left and the Wumpus has fled. You face certain death. Play again?"
    
    def check_for_wumpus(self):
        if self.wumpus.location == self.player.location:
            self.game_on = False
            return True

    def play(self, form):        
        if form['move_direction']:
            message = self.move(int(form['move_direction']))
        elif form['shoot_direction']:
            message = self.shoot_arrow(int(form['shoot_direction']))
        else:
            message = "Choose a direction to move or shoot. "
        return message
    
    def play_text(self):
        message = 'Welcome to Hunt the Wumpus! To move, enter a number, to shoot enter the letter s followed by a number.'
        while self.game_on:
            choice = input(message)
            if choice[0] == 's':
                message = self.shoot_arrow(int(choice[1]))
            else:
                message = self.move(int(choice[0]))

if __name__ == '__main__':
    game = HuntTheWumpus()
    game.play_text()
