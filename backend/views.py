#coding=utf8
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
import json
from backend.models import *
import requests
from bs4 import BeautifulSoup
# Create your views here.
from portal.models import Data,Type,FileType, UserResource, DayMessage
import sys
import uuid
import xlrd
import xlwt
import datetime
import time
from django.core.cache import cache
reload(sys)
sys.setdefaultencoding('utf8')

def need_login(func):
    def _need_login(request):
        if not request.session.get("backuser", False):
            return JsonResponse({
                'error_no': '-1',
                'message': 'need login'
            })
        else:
            return func(request)

    return _need_login


def login(request):
    if request.POST.get('uname') == 'admin' and request.POST.get('passwd') == 'pppxx77!@#':
        request.session['backuser'] = 'baidu_user'
        return JsonResponse({
            "error_no": "0",
            "data": {
                "message": "login success"
            }
        })
    else:
        return JsonResponse({
            "error_no": "1",
            "data": {
                "message": "login fail"
            }
        })


@need_login
def get_types(request):
    t = Type.objects.filter(status=1)
    return JsonResponse({
        'error_no' : '0',
        'data' : [i.message() for i in t]
    })


@need_login
def new_type(request):
    name = request.GET.get('name')
    t = Type(name=name)
    t.save()
    return JsonResponse({
        'error_no' : '0'
    })

@need_login
def delete_type(request):
    t = Type.objects.filter(id=request.GET.get('id'))
    if len(t) == 0:
        return JsonResponse({
            'error_no' : '1',
            'data' : {
                'message' : 'no such id'
            }
        })
    else :
        t[0].status = 0
        t[0].save()
        return JsonResponse({
            'error_no' : '0',
        })
@need_login
def upload_data_resource(request):
    type = request.POST.get('type')
    file = request.FILES.get('file')

    ext = str(file).split(".")[-1].lower()
    path = "upload/" + str(uuid.uuid1()) + "." + ext
    des = open(path, 'wb+')
    for j in file.chunks():
        des.write(j)
    des.close()
    if len(FileType.objects.filter(type_id=type)) :
        f = FileType.objects.get(type_id=type)
        f.filePath = path
        f.save()
    else :
        f = FileType(filePath=path,type=Type.objects.get(id=type))
        f.save()

    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    for j in UserResource.objects.filter(type_id=type) :
        j.delete()
    for i in xrange(0,sheet.nrows) :
        row = sheet.row_values(i)
        u = UserResource(user=row[0],url=row[1],op_user=row[2],op_url=row[3],type_id=type)
        u.save()
    return JsonResponse({
        'error_no' : '0',
        'data' : path
    })

@need_login
def download_data_resource(request):
    type = request.GET.get('type')
    f = FileType.objects.get(type_id=type)

    return JsonResponse({
        'error_no' : '0',
        'data' : f.filePath
    })
@need_login
def get_data(request):
    u = UserResource.objects.filter(type=request.GET.get('type'))

    return JsonResponse({
        'error_no' : '0',
        'data' : [i.message() for i in u]
    })
@need_login
def change_weight(request):
    n = request.GET.get('n')
    id = request.GET.get('id')
    u = UserResource.objects.get(id=id)
    u.weight = int(n)
    u.save()
    return JsonResponse({
        'error_no' : '0'
    })
@need_login
def change_change(request):
    n = request.GET.get('n')
    id = request.GET.get('id')
    u = UserResource.objects.get(id=id)
    u.change = int(n)
    u.save()
    return JsonResponse({
        'error_no' : '0'
    })

def spider_youku(url,type):

    try:
        j_url = url.split('?')[0] + '/videos'+ '?' + url.split('?')[1]
        j = requests.get(j_url)
        soup = BeautifulSoup(j.text)
        for i in soup.find_all("div",class_='v-meta'):
            title = i.find("div",class_="v-meta-title").find("a").attrs.get('title') if i.find("div",class_="v-meta-title").find("a").attrs.get('title') is not None else i.find("div",class_="v-meta-title").find("a").string
            time = i.find("span",class_='v-publishtime').string
            dt1 = datetime.datetime.today()
            dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)
            l = time.find("分钟前")
            k = time.find("小时前")
            j = time.find("秒前")
            if l > 0:
                print l
                time = time[:l]
                print time
                dt = datetime.datetime.now() - datetime.timedelta(minutes=int(time))
                if dt > dt1:
                    if len(Data.objects.filter(title=title)) :
                        pass
                    else :
                        d = Data(title=title,origin_id='',origin=u'优酷',origin_user_id=url,url=url,type_id=type,datetime=dt)
                        d.save()
            if k > 0:
                print k
                time = time[:k]
                print time
                dt = datetime.datetime.now() - datetime.timedelta(hours=int(time))

                if dt > dt1:
                    if len(Data.objects.filter(title=title)) :
                        pass
                    else :
                        d = Data(title=title,origin_id='',origin=u'优酷',origin_user_id=url,url=url,type_id=type,datetime=dt)
                        d.save()
            if j > 0:
                time = time[:j]
                print j
                dt = datetime.datetime.now()
                if dt > dt1:
                    if len(Data.objects.filter(title=title)) :
                        pass
                    else :
                        d = Data(title=title,origin_id='',origin=u'优酷',origin_user_id=url,url=url,type_id=type,datetime=dt)
                        d.save()

    except Exception,e:
        print e

    return JsonResponse({
        "error_no" : "0"
    })
def spider_kuaibao(url,type):
    p = url.split('?')[1].split('=')
    key = p[1]
    json_url = 'https://kuaibao.qq.com/getMediaCardInfo?chlid=' + key
    j = requests.get(json_url)
    j_json = json.loads(j.text)

    for i in j_json['info']['newsList']:
        dt = datetime.datetime.fromtimestamp(i['timestamp'])
        dt1 = datetime.datetime.today()
        dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)

        if dt > dt1 :
            if len(Data.objects.filter(title=i['title']).filter(origin=u'快报')) :
                pass
            else :
                d = Data(title=i['title'],origin_id=i['id'],origin=u'快报',origin_user_id=key,url=url,type_id=type,datetime=dt)
                d.save()
    return JsonResponse({
        "error_no" : "0",
        "data" : j_json
    })


def spider_toutiao(url,type):
    p = url.split('?')[0].split('/')
    key = p[-2]
    json_url = 'http://www.toutiao.com/c/user/article/?page_type=1&user_id='+key+'&max_behot_time=0&count=20&as=A1359929377D835&cp=59972D3853655E1'
    j = requests.get(json_url)
    j_json = json.loads(j.text)

    for i in j_json['data']:
        dt = datetime.datetime.fromtimestamp(i['behot_time'])
        dt1 = datetime.datetime.today()
        dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)
        print dt>dt1
        if dt > dt1 :
            if len(Data.objects.filter(title=i['title']).filter(origin=u'头条号')) :
                pass
            else :
                d = Data(title=i['title'],origin_id=i['item_id'],origin=u'头条号',origin_user_id=key,url=url,type_id=type,datetime=dt)
                d.save()
    json_url = 'http://www.toutiao.com/c/user/article/?page_type=0&user_id='+key+'&max_behot_time=0&count=20&as=A1359929377D835&cp=59972D3853655E1'
    j = requests.get(json_url)
    j_json = json.loads(j.text)

    for i in j_json['data']:

        dt = datetime.datetime.fromtimestamp(i['behot_time'])
        dt1 = datetime.datetime.today()
        dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)
        if dt > dt1 :
            if len(Data.objects.filter(title=i['title']).filter(origin=u'头条号')) :
                pass
            else :
                d = Data(title=i['title'],origin_id=i['item_id'],origin=u'头条号',origin_user_id=key,url=url,type_id=type,datetime=dt)
                d.save()
    return JsonResponse({
        "error_no" : "0",
        "data" : j_json
    })


def spider_bilibili(url,type):
    p = url.split('?')[0].split('/')
    key = p[-1]
    json_url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid='+key+'&pagesize=25&tid=0&page=1&keyword=&order=pubdate'
    j = requests.get(json_url)
    j_json = json.loads(j.text)

    for i in j_json['data']['vlist']:
        dt = datetime.datetime.fromtimestamp(i['created'])
        dt1 = datetime.datetime.today()
        dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)
        if dt > dt1 :
            if len(Data.objects.filter(title=i['title']).filter(origin=u'bilibili')) :
                pass
            else :
                d = Data(title=i['title'],origin_id=i['mid'],origin=u'bilibili',origin_user_id=key,url=url,type_id=type,datetime=dt)
                d.save()
    return JsonResponse({
        "error_no" : "0",
        "data" : j_json
    })

def spider_baijiahao(url,type):
    p = url.split('?')[1].split('=')
    key = ''
    for i in xrange(len(p)):
        if p[i] == 'app_id':
            key = p[i+1]
            break
    json_url = 'http://baijiahao.baidu.com/api/content/article/listall?sk=super&ak=super&app_id='+key+'&_skip=0&_limit=10&status=in:publish,published&_preload_statistic=1&_timg_cover=50,172,1000&_cache=1'
    j = requests.get(json_url)
    j_json = json.loads(j.text)

    for i in j_json['items']:
        dt = datetime.datetime.strptime(i['updated_at'],'%Y-%m-%d %H:%M:%S')
        dt = dt - datetime.timedelta(hours=8)
        dt1 = datetime.datetime.today()
        dt1 = dt1.replace(hour=0).replace(minute=0).replace(second=0)
        if dt > dt1 :
            if len(Data.objects.filter(title=i['title']).filter(origin=u'百家号')) :
                pass
            else :
                d = Data(title=i['title'],origin_id=i['id'],origin=u'百家号',origin_user_id=key,url=url,type_id=type,datetime=dt)
                d.save()
    return JsonResponse({
        "error_no" : "0",
        "data" : j_json
    })

def spider(request):

    if cache.get('spider_flag') == True:
        return JsonResponse({
            'error_no' : '-1',
            'data' : {
                'message' : u'现在存在正在执行的任务，请不要重复执行'
            }
        })
    else :
        cache.set('spider_flag',False)
        u = UserResource.objects.all()
        for i in u:
            try :
                if i.url.split('.')[1] == 'baidu':
                    spider_baijiahao(i.url,i.type_id)
                if i.op_url.split('.')[1] == 'bilibili':
                    spider_bilibili(i.op_url,i.type_id)
                if i.op_url.split('.')[1] == 'youku':
                    spider_youku(i.op_url,i.type_id)
                if i.op_url.split('.')[1] == 'qq':
                    spider_kuaibao(i.op_url,i.type_id)
                if i.op_url.split('.')[1] == 'toutiao':
                    spider_toutiao(i.op_url,i.type_id)
            except Exception,e:
                print e
            time.sleep(10)
            cache.set('spider_flag',True)
    return JsonResponse({
        'error_no' : '0'
    })
@need_login
def get_total(request):
    u = UserResource.objects.filter(type=request.GET.get('type'))
    same = 0
    weight = 0
    cnt_baijiahao = 0
    op_cnt = 0
    change = 0
    for i in u:
        k = i.message()
        cnt_baijiahao += k['cnt']
        op_cnt += k['op_cnt']
        same += k['same']
        weight += k['weight']
        change += k['change']
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    d = DayMessage.objects.filter(datetime__year=year,datetime__month=month,datetime__day=day).filter(type_id=request.GET.get('type'))
    if len(d):
        d[0].baijiahao_count = cnt_baijiahao
        d[0].op_count = op_cnt
        d[0].same = float((same+weight))/float(op_cnt+change)
        d[0].weight = weight
        d[0].save()
    else :
        d = DayMessage(baijiahao_count=cnt_baijiahao,op_count=op_cnt,same=float((same+weight))/float(op_cnt+change),weight=weight,datetime=date,type_id=request.GET.get('type'))
        d.save()
    return JsonResponse({
        'error_no' : '0',
        'data' : {
            'cnt' : cnt_baijiahao,
            'op_cnt' : op_cnt,
            'same' : float((same+weight))/float(op_cnt+change),
            'weight' : weight
        }
    })


@need_login
def download_total(request):
    d = DayMessage.objects.filter(type_id=request.GET.get('type'))
    xls = xlwt.Workbook()
    sheet = xls.add_sheet("data")
    sheet.write(0, 0, u'id')
    sheet.write(0, 1, u'百家号更新数量')
    sheet.write(0, 2, u'竞品更新数量')
    sheet.write(0, 3, u'权重')
    sheet.write(0, 4, u'实时同步率')
    sheet.write(0, 5, u'类型')
    sheet.write(0, 6, u'日期')
    for i in xrange(0,len(d)):
        message = d[i].message()
        sheet.write(i+1, 0, message['id'])
        sheet.write(i+1, 1, message['baijiahao_count'])
        sheet.write(i+1, 2, message['op_count'])
        sheet.write(i+1, 3, message['weight'])
        sheet.write(i+1, 4, message['same'])
        sheet.write(i+1, 5, message['type'])
        sheet.write(i+1, 6, message['datetime'])
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    path = 'upload/'+date+'-'+str(d[0].type.name)+'-统计.xls'
    xls.save(path)

    return JsonResponse({
        'error_no' : '0',
        'data' : path
    })


@need_login
def download_excel(request):
    u = UserResource.objects.filter(type=request.GET.get('type'))
    xls = xlwt.Workbook()
    sheet = xls.add_sheet("data")
    sheet.write(0, 0, u'id')
    sheet.write(0, 1, u'百家号用户')
    sheet.write(0, 2, u'百家号url')
    sheet.write(0, 3, u'百家号发布数量')
    sheet.write(0, 4, u'权重')
    sheet.write(0, 5, u'竞品发布数量')
    sheet.write(0, 6, u'竞品url')
    sheet.write(0, 7, u'竞品发布数量')
    sheet.write(0, 8, u'同步数')
    for i in xrange(0,len(u)):
        message = u[i].message()
        sheet.write(i+1, 0, message['id'])
        sheet.write(i+1, 1, message['user'])
        sheet.write(i+1, 2, message['url'])
        sheet.write(i+1, 3, message['cnt'])
        sheet.write(i+1, 4, message['weight'])
        sheet.write(i+1, 5, message['op_user'])
        sheet.write(i+1, 6, message['op_url'])
        sheet.write(i+1, 7, message['op_cnt'])
        sheet.write(i+1, 8, message['same'])
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    path = 'upload/'+date+'-'+str(u[0].type.name)+'-列表.xls'
    xls.save(path)
    return JsonResponse({
        'error_no' : '0',
        'data' : path
    })

@need_login
def delete_user(request):
    u = UserResource.objects.get(id=request.GET.get('id'))
    u.delete()
    return JsonResponse({
        'error_no' : '0'
    })