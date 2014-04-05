from django.contrib import admin
from game.models import ActiveUser, Game, GameParameter, Instance, Action, InitState, TempState, WorkingState


class ActiveUserAdmin(admin.ModelAdmin):
	list_display = ('user','game','launched')


class GameAdmin(admin.ModelAdmin):
	list_display = ('id','rules')


class GameParameterAdmin(admin.ModelAdmin):
	pass


class InstanceAdmin(admin.ModelAdmin):
	list_display = ('id','type','user')


class ActionAdmin(admin.ModelAdmin):
	pass


class InitStateAdmin(admin.ModelAdmin):
	list_display = ('game','instance','attribute', 'value')


class TempStateAdmin(admin.ModelAdmin):
	pass


class WorkingStateAdmin(admin.ModelAdmin):
	pass


admin.site.register(ActiveUser, ActiveUserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameParameter)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Action)
admin.site.register(InitState, InitStateAdmin)
admin.site.register(TempState)
admin.site.register(WorkingState)