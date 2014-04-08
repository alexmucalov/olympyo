from django.contrib import admin
from game.models import ActionArch, GameObjectArch, GameObjectArchAttribute, Game, GameObjectSet, WaitRoomUser, GameObjectInstance, GameObjectInstanceAttribute, Action


class ActionArchAdmin(admin.ModelAdmin):
    list_display = ('action_arch',)


class GameObjectArchAdmin(admin.ModelAdmin):
    list_display = ('game_object_arch',)


class GameObjectArchAttributeAdmin(admin.ModelAdmin):
    list_display = ('game_object_arch', 'attribute', 'default_value',)


class GameAdmin(admin.ModelAdmin):
    list_display = ('name','rules',)


class GameObjectSetAdmin(admin.ModelAdmin):
    list_display = ('game', 'game_object', 'no_of_objects',)


class WaitRoomUserAdmin(admin.ModelAdmin):
    list_display = ('game','user',)


class GameObjectInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'game_object_instance',)


class GameObjectInstanceAttributeAdmin(admin.ModelAdmin):
    list_display = ('game_object_instance', 'attribute', 'value',)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'initiator','action','parameters','affected',)


admin.site.register(ActionArch, ActionArchAdmin)
admin.site.register(GameObjectArch, GameObjectArchAdmin)
admin.site.register(GameObjectArchAttribute, GameObjectArchAttributeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameObjectSet, GameObjectSetAdmin)
admin.site.register(WaitRoomUser, WaitRoomUserAdmin)
admin.site.register(GameObjectInstance, GameObjectInstanceAdmin)
admin.site.register(GameObjectInstanceAttribute, GameObjectInstanceAttributeAdmin)
admin.site.register(Action, ActionAdmin)