from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class IDC(models.Model):
    '''机房表'''
    name=models.CharField(max_length=128,verbose_name='机房名称')
    def __str__(self):
        return self.name

class Account(models.Model):
    '''登录堡垒机的用户表'''
    user=models.OneToOneField(User)
    name=models.CharField(max_length=64,verbose_name='用户名')
    host_user_bind=models.ManyToManyField('HostUserBind',blank=True)
    host_group=models.ManyToManyField('HostGroup',blank=True)


class Host(models.Model):
    '''主机表，主机表的相关信息，用户需要通过堡垒机登录上的主机表'''
    hostname=models.CharField(max_length=64,unique=True,verbose_name='主机名')
    addr=models.GenericIPAddressField(verbose_name='ip地址')
    port=models.IntegerField(verbose_name='端口')
    idc=models.ForeignKey('IDC',verbose_name='关联到机房')
    enabled=models.BooleanField(default=True)  #主机是否可用
    def __str__(self):
        return "%s-%s"%(self.hostname,self  .addr)

class HostUser(models.Model):
    '''可以登录到主机上的用户表,每个主机都应有相应的人员去登录，这些账密统一给堡垒机去登录'''
    connection_type_choices=((1,'SSH-Type'),(2,'Account-Password'))
    connection_type=models.SmallIntegerField(choices=connection_type_choices,verbose_name='连接主机的方式')
    username = models.CharField(max_length=64, verbose_name='连接到主机的用户名')
    password = models.CharField(max_length=64, verbose_name='连接到远程主机的密码')
    def __str__(self):
        return "%s-%s-%s"%(self.get_connection_type_display(),self.username,self.password)
    class Meta:
        unique_together=('username','password')

class HostUserBind(models.Model):
    '''主机和账户关联起来'''
    host=models.ForeignKey('Host')
    host_user=models.ForeignKey('HostUser')
    class Meta:
        unique_together=('host','host_user')
    def __str__(self):
        return '%s-%s'%(self.host,self.host_user)

class HostGroup(models.Model):
    '''用户组表，用户属于哪个工作组'''
    name=models.CharField(max_length=64,verbose_name='主机组名',unique=True)
    host_user_binds=models.ManyToManyField('HostUserBind')   #关联到
    def __str__(self):
        return self.name

class AuditLog(models.Model):
    '''审计日志表，记录在主机上的操作'''
    session=models.ForeignKey('SessionLog')
    cmd=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s-%s'%(self.session,self.cmd)


class SessionLog(models.Model):
    account=models.ForeignKey('Account')
    host_user_bind=models.ForeignKey('HostUserBind')
    start_date=models.DateTimeField(auto_now_add=True)
    end_date=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "%s-%s"%(self.account,self.host_user_bind)
