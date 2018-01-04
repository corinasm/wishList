from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Item


#==================================================#
#                  RENDER METHODS                  #
#==================================================#

def index(request):
    return render (request, 'wish_items/index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    try: 
        request.session['user_id']
    except KeyError:
        return redirect('/')  


    user = User.objects.get(id=request.session['user_id'])
    favoriteitems = user.favoriteitems.all().order_by('-created_at')
    other_wisheditems = Item.objects.exclude(fav_by=user).order_by('-created_at')
    
    context = {
        'user': user,
        'favoriteitems': favoriteitems,
        'others_wish_list': other_wisheditems
    }

    '''
    my_wisheditems = Item.objects.filter(wished_by=request.session['user_id'])
    other_wisheditems = Item.objects.exclude(wished_by=request.session['user_id'])
    
    context = {
        'user': user,
        'my_wish_list': my_wisheditems,
        'others_wish_list': other_wisheditems
        
    }
    '''
    return render(request, 'wish_items/dashboard.html', context)


def create(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user': user,
    }

    return render(request, 'wish_items/create.html', context)   


def show(request, item_id):
    
    item = Item.objects.get(id=item_id)
    # users = User.objects.filter(favoriteitems=item)
    
    context = {
        'item': item,
        # 'users': users, 
    }
    
    return render(request, 'wish_items/show.html', context)    



#==================================================#
#                 PROCESS METHODS                  #
#==================================================#

def registration (request):
    
    if request.method == "POST":

        result = User.objects.validate_registration(request.POST)

        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) 

        else:
            request.session['user_id'] = result.id 
            #messages.success(request, 'You have succesfully registered.') 
            return redirect('/dashboard')  
 
    return redirect ('/')

def login(request):   

    if request.method == "POST":

        result = User.objects.validate_login(request.POST)
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) 
                #print (tag, error_item)

        else:
            request.session['user_id'] = result.id 
            #messages.success(request, 'You have succesfully logged in.') 
            return redirect('/dashboard')  
 
    return redirect ('/')

def create_item(request):

    user_id = request.session['user_id']

    if request.method == "POST":
        result = Item.objects.validate_createItem(request.POST)
        
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) 
                print (tag, error_item)
            return redirect('/create')    

        else:
            return redirect('/dashboard')    
    else:
        messages.error(request, 'Error. Try again!')
        return redirect('/create')            

def delete_item(request, item_id):
    item=Item.objects.get(id=item_id).delete()
    return redirect ('/dashboard')

def addToMyWishlist(request, item_id):
    '''
    item=Item.objects.get(id=item_id)
    user_id = request.session['user_id']
    user=User.objects.get(id=user_id) 
    owner=User.objects.get(id=owner_id) 
    user.wisheditems.add(item)  
    '''
    user_id = request.session['user_id']
    user=User.objects.get(id=user_id)
    favorite_item = Item.objects.get(id=item_id)
    user.favoriteitems.add(favorite_item)
    
    return redirect ('/dashboard')

def removeFromMyWishlist(request, item_id):

    user_id = request.session['user_id']
    user=User.objects.get(id=user_id)
    favorite_item = Item.objects.get(id=item_id)
    user.favoriteitems.remove(favorite_item)

    return redirect ('/dashboard')
    
