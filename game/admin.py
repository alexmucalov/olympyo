from django.contrib import admin
from game.models import GameRule, ArchAction, ArchAttribute, ArchGameObject, ArchAttributeSet, ArchGameObjectAttributeValue, ArchRelationship, GameObjectSet, GameObjectRelationshipSet, GameObject, GameObjectRelationship, GameObjectAttributeValue, Game, Waitroom, GameInstance, GameInstanceObject, GameInstanceObjectAttributeValue, GameInstanceObjectRelationship, Action, ArchLayoutType


class GameRuleAdmin(admin.ModelAdmin):
    list_display = ('game_rules',)


class ArchLayoutTypeAdmin(admin.ModelAdmin):
    list_display = ('arch_layout',)


class ArchActionAdmin(admin.ModelAdmin):
    list_display = ('arch_action',)


class ArchAttributeAdmin(admin.ModelAdmin):
    list_display = ('arch_attribute',)


class ArchGameObjectAdmin(admin.ModelAdmin):
    list_display = ('arch_game_object',)


class ArchAttributeSetAdmin(admin.ModelAdmin):
    list_display = ('attribute_set',)


class ArchGameObjectAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('arch_game_object', 'attribute', 'default_value',)


class ArchRelationshipAdmin(admin.ModelAdmin):
    list_display = ('arch_relationship',)


class GameObjectSetAdmin(admin.ModelAdmin):
    list_display = ('game_object_set',)


class GameObjectRelationshipSetAdmin(admin.ModelAdmin):
    list_display = ('game_object_relationship_set',)


class GameObjectAdmin(admin.ModelAdmin):
    list_display = ('id','game_object_set','game_object','attribute_set',)


class GameObjectRelationshipAdmin(admin.ModelAdmin):
    list_display = ('relationship_set','subject_game_object','relationship','object_game_object',)


class GameObjectAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute_set','attribute','value',)


class GameAdmin(admin.ModelAdmin):
    list_display = ('name','game_object_set','game_object_relationship_set','game_rules','turns',)


class WaitroomAdmin(admin.ModelAdmin):
    list_display = ('game',)


class GameInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','game','turn',)


class GameInstanceObjectAdmin(admin.ModelAdmin):
    list_display = ('id','game_instance', 'game_object','user',)


class GameInstanceObjectAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('game_instance_object', 'attribute', 'value',)


class GameInstanceObjectRelationshipAdmin(admin.ModelAdmin):
    list_display = ('game_instance','subject_game_instance_object','relationship','object_game_instance_object',)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'initiator','action','parameters','affected',)


admin.site.register(GameRule, GameRuleAdmin)
admin.site.register(ArchLayoutType, ArchLayoutTypeAdmin)
admin.site.register(ArchAction, ArchActionAdmin)
admin.site.register(ArchAttribute, ArchAttributeAdmin)
admin.site.register(ArchGameObject, ArchGameObjectAdmin)
admin.site.register(ArchAttributeSet, ArchAttributeSetAdmin)
admin.site.register(ArchGameObjectAttributeValue, ArchGameObjectAttributeValueAdmin)
admin.site.register(ArchRelationship, ArchRelationshipAdmin)
admin.site.register(GameObjectSet, GameObjectSetAdmin)
admin.site.register(GameObjectRelationshipSet, GameObjectRelationshipSetAdmin)
admin.site.register(GameObject, GameObjectAdmin)
admin.site.register(GameObjectRelationship, GameObjectRelationshipAdmin)
admin.site.register(GameObjectAttributeValue, GameObjectAttributeValueAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Waitroom, WaitroomAdmin)
admin.site.register(GameInstance, GameInstanceAdmin)
admin.site.register(GameInstanceObject, GameInstanceObjectAdmin)
admin.site.register(GameInstanceObjectAttributeValue, GameInstanceObjectAttributeValueAdmin)
admin.site.register(GameInstanceObjectRelationship, GameInstanceObjectRelationshipAdmin)
admin.site.register(Action, ActionAdmin)