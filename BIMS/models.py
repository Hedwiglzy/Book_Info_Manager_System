from django.db import models

# Create your models here.

class User(models.Model):
    user_id     = models.AutoField(primary_key=True)              #用户ID
    user_name   = models.CharField(max_length=30)                 #用户名
    password    = models.CharField(max_length=30)                 #密码
    tel         = models.BigIntegerField(null=True)               #电话
    email       = models.EmailField(null=True)                    #邮箱
    sex         = models.IntegerField(null=True)                  #性别 1男 2女 0其他
    birthday    = models.DateField(null=True)                     #生日
    age         = models.IntegerField(null=True)                  #年龄
    locate      = models.CharField(max_length=50,null=True)       #所在地
    remark      = models.CharField(max_length=500,null=True)      #个人简介
    image       = models.ImageField(null=True)                    #头像
    create_date = models.DateField(null=True)                     #创建日期

    def __str__(self):
        return  self.user_name
    class Meta:
            verbose_name = "user_info_detail"