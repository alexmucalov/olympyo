from django.contrib import admin
from game.models import Game, GameObject, GameObjectProperty, WaitRoom, GameInstance, GameInstanceObject, GameInstanceObjectProperty, Action


class GameAdmin(admin.ModelAdmin):
    list_display = ('id','name','rules')


class GameObjectAdmin(admin.ModelAdmin):
    list_display = ('id','type')


class GameObjectPropertyAdmin(admin.ModelAdmin):
    list_display = ('id','game_object','property','init_value')


class WaitRoomAdmin(admin.ModelAdmin):
    list_display = ('id','game','user')


class GameInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','game')


class GameInstanceObjectAdmin(admin.ModelAdmin):
    list_display = ('id','instance','game_object')


class GameInstanceObjectPropertyAdmin(admin.ModelAdmin):
    list_display = ('id','game_instance_object','game_object_property','value')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id','instance','turn', 'initiator','function','parameters','affected')


admin.site.register(Game, GameAdmin)
admin.site.register(GameObject, GameObjectAdmin)
admin.site.register(GameObjectProperty, GameObjectPropertyAdmin)
admin.site.register(WaitRoom, WaitRoomAdmin)
admin.site.register(GameInstance, GameInstanceAdmin)
admin.site.register(GameInstanceObject, GameInstanceObjectAdmin)
admin.site.register(GameInstanceObjectProperty, GameInstanceObjectPropertyAdmin)
admin.site.register(Action, ActionAdmin)