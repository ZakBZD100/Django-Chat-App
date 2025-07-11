from django.contrib import admin
from .models import Room, Message, Role

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'text', 'date')
    list_filter = ('room', 'date', 'user')
    search_fields = ('text', 'user__username', 'room__name')
    date_hierarchy = 'date'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'role')
    list_filter = ('role', 'room')
    search_fields = ('user__username', 'room__name')
