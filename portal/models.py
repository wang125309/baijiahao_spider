from django.db import models
import datetime

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=256)
    datetime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1) #1online 0offline
    def message(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'datetime' : self.datetime
        }
class FileType(models.Model):
    filePath = models.CharField(max_length=512)
    datetime = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type,null=True)
    def message(self):
        return {
            'id' : self.id,
            'filePath' : self.filePath,
            'type' : self.type
        }

class Data(models.Model):
    title = models.CharField(max_length=512)
    username = models.CharField(max_length=128)
    desc = models.CharField(max_length=256)
    datetime = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type,null=True)
    origin = models.CharField(max_length=128)
    origin_id = models.CharField(max_length=64)
    origin_user_id = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    o_url = models.CharField(max_length=256,null=True)
    related_id = models.CharField(max_length=64,null=True)
    def message(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'username' : self.username,
            'desc' : self.desc,
            'datetime' : self.datetime,
            'o_url' : self.o_url
        }

class DayMessage(models.Model):
    datetime = models.DateField(auto_now=True)
    baijiahao_count = models.IntegerField(null=True)
    op_count = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    same = models.FloatField(null=True)
    type = models.ForeignKey(Type,null=True)
    change = models.FloatField(null=True)
    def message(self):
        return {
            'id' : self.id,
            'baijiahao_count' : self.baijiahao_count,
            'op_count' : self.op_count,
            'weight' : self.weight,
            'same' : self.same,
            'type' : self.type.name,
            'change' : self.change,
            'datetime' : self.datetime.strftime('%Y-%m-%d')
        }


class UserResource(models.Model):
    user = models.CharField(max_length=256)
    url = models.CharField(max_length=512)
    op_user = models.CharField(max_length=256)
    op_url = models.CharField(max_length=512)
    datetime = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type,null=True)
    weight = models.IntegerField(default=0)
    change = models.IntegerField(default=0)
    def message(self):
        dt = datetime.datetime.today()
        dt = dt.replace(hour=0).replace(minute=0).replace(second=0)
        data = Data.objects.filter(datetime__gt=dt).filter(url=self.url)
        op_data = Data.objects.filter(datetime__gt=dt).filter(url=self.op_url)
        cnt = 0
        for i in data:
            for j in op_data:
                if i.title == j.title :
                    cnt += 1
        return {
            'id' : self.id,
            'user' : self.user,
            'url' : self.url,
            'cnt' : len(data),
            'weight' : self.weight,
            'op_user' : self.op_user,
            'op_url' : self.op_url,
            'op_cnt' : len(op_data),
            'same' : cnt,
            'datetime' : self.datetime,
            'type' : self.type.name,
            'change' : self.change,
            'title' : [i.message() for i in data],
            'op_title' : [i.message() for i in op_data]
        }