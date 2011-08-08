from django.contrib import admin

from postfixadmin.models import Domain, Alias, MailBox

class DomainAdmin(admin.ModelAdmin):
    pass
    
class AliasInline(admin.TabularInline):
    model = Alias
        
class MailBoxAdmin(admin.ModelAdmin):
    inlines = [AliasInline]
    
class AliasAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Domain, DomainAdmin)
admin.site.register(MailBox, MailBoxAdmin)
admin.site.register(Alias, AliasAdmin)
