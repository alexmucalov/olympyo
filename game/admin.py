from django.contrib import admin
from game.models import GameRule, ArchAction, ArchAttribute, ArchGameObject, ArchGameObjectAttributeValue, GameObjectSet, GameObject, AttributeValue, Game, WaitRoomUser, GameInstance, GameInstanceObject, GameInstanceObjectAttributeValue, Action


class GameRuleAdmin(admin.ModelAdmin):
    list_display = ('game_rules',)


class ArchActionAdmin(admin.ModelAdmin):
    list_display = ('arch_action',)


class ArchAttributeAdmin(admin.ModelAdmin):
    list_display = ('arch_attribute',)


class ArchGameObjectAdmin(admin.ModelAdmin):
    list_display = ('arch_game_object',)


class ArchGameObjectAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('arch_game_object', 'attribute', 'default_value',)


class GameObjectSetAdmin(admin.ModelAdmin):
    list_display = ('game_object_set',)


class GameObjectAdmin(admin.ModelAdmin):
    list_display = ('game_object_set','game_object','attribute_set',)


class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute_set','attribute','value',)


class GameAdmin(admin.ModelAdmin):
    list_display = ('game_object_set','game_rules',)


class WaitRoomUserAdmin(admin.ModelAdmin):
    list_display = ('game',)


class GameInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','game',)


class GameInstanceObjectAdmin(admin.ModelAdmin):
    list_display = ('game_instance', 'game_object',)


class GameInstanceObjectAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('game_instance_object', 'attribute', 'value',)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'initiator','action','parameters','affected',)


admin.site.register(GameRule, GameRuleAdmin)
admin.site.register(ArchAction, ArchActionAdmin)
admin.site.register(ArchAttribute, ArchAttributeAdmin)
admin.site.register(ArchGameObject, ArchGameObjectAdmin)
admin.site.register(ArchGameObjectAttributeValue, ArchGameObjectAttributeValueAdmin)
admin.site.register(GameObjectSet, GameObjectSetAdmin)
admin.site.register(GameObject, GameObjectAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(WaitRoomUser, WaitRoomUserAdmin)
admin.site.register(GameInstance, GameInstanceAdmin)
admin.site.register(GameInstanceObject, GameInstanceObjectAdmin)
admin.site.register(GameInstanceObjectAttributeValue, GameInstanceObjectAttributeValueAdmin)
admin.site.register(Action, ActionAdmin)