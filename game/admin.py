from django.contrib import admin
from game.models import LoggedUser, Game, GameParameter, Instance, Action, InitState, TempState, WorkingState

admin.site.register(LoggedUser)
admin.site.register(Game)
admin.site.register(GameParameter)
admin.site.register(Instance)
admin.site.register(Action)
admin.site.register(InitState)
admin.site.register(TempState)
admin.site.register(WorkingState)