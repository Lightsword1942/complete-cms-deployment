from django.db import models

class Domain(models.Model):

    domain = models.CharField(max_length=255)
    description  = models.CharField(max_length=255)
    aliases = models.BooleanField()
    mailboxes = models.BooleanField()
    maxqouta = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.domain

class MailBox(models.Model):

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain)
    password = models.CharField(max_length=255, default='$1$.2213700$AOdx3nlEm3dKANLVkAjim0')
    quota = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField()

    def __unicode__(self):
        return '%s@%s' % (self.username, self.domain.domain)    

class Alias(models.Model):

    username = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain)
    mailbox = models.ForeignKey(MailBox)
    active = models.BooleanField()

    def __unicode__(self):
        return '%s@%s -> %s@%s' % (self.username, self.domain.domain, self.mailbox.username, self.mailbox.domain.domain)    

"""
class Relocate(models.Model):
    mailbox = models.ForeignKey(MailBox)
    username = models.CharField(max_length=255, core=True)
    domain = models.ForeignKey(Domain)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField()

    def __str__(self):
        return '%s@%s -> %s@%s' % (self.mailbox.username, self.mailbox.domain.domain, self.username, self.domain.domain)
   
    class Admin:
        pass

"""
