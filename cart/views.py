from django.shortcuts import render
from django.http import HttpResponse


#def index(request):
#    return HttpResponse("Cart Page!")

#CPU
#GPU
#RAM
#HDD
#SSD
cart_content = dict()


def index(request):
    GPU=request.GET.get('GPU')
    CPU=request.GET.get('CPU')
    RAM=request.GET.get('RAM')
    HDD=request.GET.get('HDD')
    SSD=request.GET.get('SSD')
    if(GPU!=None):
        cart_content['GPU'] = GPU
    if(CPU!=None):
        cart_content['CPU'] = CPU
    if(RAM!=None):
        cart_content['RAM'] = RAM
    if(HDD!=None):
        cart_content['HDD'] = HDD
    if(SSD!=None):
        cart_content['SSD'] = SSD
    print(cart_content)

    return render(request,'cart.html',{'cart_content':cart_content})
    