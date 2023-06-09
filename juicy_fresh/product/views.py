from django.shortcuts import render, redirect
from .models import fruits, comment
from django.http import JsonResponse
from django.core.cache import cache

# Create your views here.

def test(r):
    return render(r,'text.html')

def about(r):
    idnum=r.GET['id']
    obj=fruits.objects.get(id=idnum)
    if 'recent' in r.session:
        if idnum in r.session['recent']:
            r.session['recent'].remove(idnum)
        data=fruits.objects.filter(id__in=r.session['recent'])
        r.session['recent'].insert(0,idnum )
        if len(r.session['recent'])>=5:
            r.session['recent'].pop()
    else:
        r.session['recent']=[idnum]
        data=[]
    r.session.modified=True   
    return render(r,'about.html',{'fruit':obj,'rec':data})

def about2(r): #with cache, without recents
    idnum = r.GET['id']
    if cache.get(idnum):
        obj=cache.get(idnum)
        print("DATA FROM CACHE")
    else:
        obj = fruits.objects.get(id=idnum)
        cache.set(idnum, obj)
        print("DATA FROM DATABASE")

    return render(r,'about.html',{'fruit':obj})


def cmt(r):
    uc = r.GET['usercomment']
    un = r.GET['user']
    pid = r.GET['pid']
    obj = comment.objects.create(proid_id=pid, user=un, msg=uc, like=0)
    obj.save()
    return redirect('/product/?id='+pid)

def like(r):
    cmtid = r.GET['id']
    obj = comment.objects.filter(id=cmtid)
    likes = int(obj[0].like) + 1
    obj.update(like=str(likes))
    return redirect('/product/?id='+str(obj[0].proid_id))
    
def autocmplt(r):
    if 'term' in r.POST:
        data = r.POST['term']
        obj = fruits.objects.filter(name__istartswith=data)
        f_list=[]
        for f in obj:
            f_list.append(f.name)
        print(f_list)
        return JsonResponse(f_list,safe=False)
    return render(r, 'test.html')