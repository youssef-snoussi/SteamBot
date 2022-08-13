class User:

    id = ""
    saved_games = []

    def __init__(self, user):
        self.id = user

    def save_game(self, game):
        self.saved_games.append(game)
