from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from game.models import Game, GameObjectSet, GameObject, GameObjectRelationshipSet, GameObjectRelationship, ExoActionSet, ExoAction

# Create the form class.
class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'game_object_set', 'game_object_relationship_set', 'exo_action_set', 'game_rules', 'turns',]
        labels = {
                'name': _('Game name'),
                'game_object_set': _('Objects'),
                'game_object_relationship_set': _('Relationships'),
                'exo_action_set': _('External actions'),
                'game_rules': _('Rules'),
                'turns': _('Turns'),
                }
# Creating a form to add an article.
#form = ArticleForm()

# Creating a form to change an existing article.
#article = Article.objects.get(pk=1)
#form = ArticleForm(instance=article)