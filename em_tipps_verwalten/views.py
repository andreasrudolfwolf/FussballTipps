from django.shortcuts import render
#from django.contrib import messages
#from django.contrib.auth import authenticate, login



def startSeite(request):
    return render(request, 'startSeite.html')

def paarungen(request):
    return render(request, 'paarungen.html')

def tippen(request):
    return render(request, 'tippen.html')

"""def loginSeite(request):
    #if request.method == 'POST':
     #   benutzername = request.POST['benutzername']
      #  passwort = request.POST['passwort']
        #benutzer = authenticate(request, username=benutzername, password=passwort)

        #if benutzer is not None:
        #    login(request, benutzer)
        #    return redirect('login')
        #else:
        #    messages.error(request, 'Benutzername oder Passwort nicht korrekt')

    return render(request, 'em_tipps/login.html')
"""
