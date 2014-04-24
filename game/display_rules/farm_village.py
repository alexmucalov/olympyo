from game.models import GameInstanceObject

def centre_displays(game_instance):
    players = GameInstanceObject.objects.filter(game_instance=game_instance, game_object__game_object__arch_game_object="player")
    labour = GameInstanceObject.objects.filter(game_instance=game_instance, game_object__game_object__arch_game_object="labour")
    player_count = players.count()
    labour_count = labour.count()
    centre_display = [('Players', player_count), ('Labour', labour_count)]
    return centre_display