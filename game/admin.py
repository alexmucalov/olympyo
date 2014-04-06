from django.contrib import admin
from game.models import Game, GameObject, WaitRoom, GameInstance, GameInstanceObject, Action


class GameAdmin(admin.ModelAdmin):
    list_display = ('id','name','rules')


class GameObjectAdmin(admin.ModelAdmin):
    list_display = ('id','game','type','label','default_value')


class WaitRoomAdmin(admin.ModelAdmin):
    list_display = ('id','game','user')


class GameInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','game')


class GameInstanceObjectAdmin(admin.ModelAdmin):
    list_display = ('id','instance','game_object')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id','instance','turn', 'initiator','function','parameters','affected')


admin.site.register(Game, GameAdmin)
admin.site.register(GameObject, GameObjectAdmin)
admin.site.register(WaitRoom, WaitRoomAdmin)
admin.site.register(GameInstance, GameInstanceAdmin)
admin.site.register(GameInstanceObject, GameInstanceObjectAdmin)
admin.site.register(Action, ActionAdmin)