from django.test import TestCase
from game.models import Game, GameObject

class GameTests(TestCase):

    def test_create_game(self):
        test_rules = 'These are the rules!'
        game = Game.objects.create(rules=test_rules)
        self.assertEqual(game.rules, test_rules)

class GameObjectTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create(rules='')

    def test_create_game_objects(self):
        test_label = 'Test Label'
        test_value = '1'
        game_object = GameObject.objects.create(game=self.game, label=test_label, default_value=test_value)
        self.assertEqual(game_object.game, self.game)
        self.assertEqual(game_object.label, test_label)
        self.assertEqual(game_object.default_value, test_value)
        
        # Why isn't 'type' attribute necessary to create GameObject?
        
class GameInstanceTests(TestCase):

    def test_create_game_instance_for_users(self):
        pass
        
    def test_game_instance_objects_copied_for_game_instance(self):
        pass