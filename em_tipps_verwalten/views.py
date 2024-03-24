from django.shortcuts import render
from .models import *
#from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

def startSeite(request):
    gruppen = Gruppen.objects.all()
    print(gruppen)
    ctx = {'gruppen': gruppen}
    return render(request, 'startSeite.html', ctx)

def paarungen(request):
    query = """
    select 
        g.id,
        g.gruppen_name, 
        ma.paarungen_id,
        ma.heim_mannschaft_id_id, 
        ma.gast_mannschaft_id_id,  
        ma.spiel_termin,
        ma.spiel_ort,
        m.mannschaft_id, m.mannschaft_name heim_mannschaft,
        m2.mannschaft_id, m2.mannschaft_name gast_mannschaft,
        ma.tore_heim_mannschaft,
        ma.tore_gast_mannschaft
        from 
            em_tipps_verwalten_gruppen g
        join em_tipps_verwalten_mannschaften m on g.id = m.gruppen_id_id
        join em_tipps_verwalten_paarungen ma on ma.heim_mannschaft_id_id = m.mannschaft_id
        join em_tipps_verwalten_mannschaften m2 on ma.gast_mannschaft_id_id = m2.mannschaft_id
        order by ma.spiel_termin asc
    """
    alle_paarungen = Gruppen.objects.raw(query)
    return render(request, 'paarungen.html', {'alle_paarungen' : alle_paarungen})

def gruppenspiele(request, id):
    query = """
    select 
        g.id,
        g.gruppen_name, 
        ma.paarungen_id,
        ma.heim_mannschaft_id_id, 
        ma.gast_mannschaft_id_id,  
        ma.spiel_termin,
        ma.spiel_ort,
        m.mannschaft_id, m.mannschaft_name heim_mannschaft,
        m2.mannschaft_id, m2.mannschaft_name gast_mannschaft,
        ma.tore_heim_mannschaft,
        ma.tore_gast_mannschaft
        from 
            em_tipps_verwalten_gruppen g
        join em_tipps_verwalten_mannschaften m on g.id = m.gruppen_id_id
        join em_tipps_verwalten_paarungen ma on ma.heim_mannschaft_id_id = m.mannschaft_id
        join em_tipps_verwalten_mannschaften m2 on ma.gast_mannschaft_id_id = m2.mannschaft_id
        where m.gruppen_id_id = %s 
        order by ma.spiel_termin asc
    """
    params = [id]
    gruppenspiele = Gruppen.objects.raw(query, params)
    return render(request, 'gruppenspiele.html', {'gruppenspiele' : gruppenspiele})

def tippen(request):
    query = """
    select 
            g.id,
            g.gruppen_name, 
            ma.paarungen_id,
            ma.heim_mannschaft_id_id, 
            ma.gast_mannschaft_id_id,  
            ma.spiel_termin,
            ma.spiel_ort,
            m.mannschaft_id, m.mannschaft_name heim_mannschaft,
            m2.mannschaft_id, m2.mannschaft_name gast_mannschaft,
            ma.tore_heim_mannschaft,
            ma.tore_gast_mannschaft,
            t.tipp_id,
            t.tipp_tore_heim_mannschaft tipp_tore_heim,
            t.tipp_tore_gast_mannschaft tipp_tore_gast,
            ti.tipper_id,
            ti.name,
            ti.vorname,
            ti.tippername tippername
            from 
                em_tipps_verwalten_gruppen g
            join em_tipps_verwalten_mannschaften m on g.id = m.gruppen_id_id
            join em_tipps_verwalten_paarungen ma on ma.heim_mannschaft_id_id = m.mannschaft_id
            join em_tipps_verwalten_mannschaften m2 on ma.gast_mannschaft_id_id = m2.mannschaft_id
            left join em_tipps_verwalten_tipps t on ma.paarungen_id = t.paarungen_id
            left join em_tipps_verwalten_tipper ti on ti.tipper_id = t.tipper_id
            order by ma.spiel_termin asc
    """
    tipps = Gruppen.objects.raw(query)
    if request.method == 'POST':
        # Dateneingabe von HTML Formular
        heimtore_list = request.POST.getlist('heim_tore')
        gasttore_list = request.POST.getlist('gast_tore')
        paarungen_id = request.POST.getlist('paarungen_id')
        tipp_id = request.POST.getlist('tipp_id')
        print(tipp_id)
        i = 0
        for tipp in tipps:
            print(f"Paarung:{paarungen_id[i]} Tore:{heimtore_list[i]} : {gasttore_list[i]} und User: {request.user.id} und tipp_id {tipp_id[i]}")
            #print(request.user.id)
            # Prüfen, ob create oder update!
            # Wenn es Tipps gibt, dann werden die in die DB geschrieben
            #print(tipp_id[i])
            if (heimtore_list[i] != tipp.tipp_tore_heim and heimtore_list[i] != '') or \
               (gasttore_list[i] != tipp.tipp_tore_gast and gasttore_list[i] != '') \
                and tipp_id[i] is not None:
                pass
                if tipp_id[i] != '':
                    print(tipp_id[i])
                #update_tipps = get_object_or_404(Tipps, tipp_id=tipp_id[i])
                #update_tipps.tipp_tore_heim_mannschaft = heimtore_list[i]
                #update_tipps.tipp_tore_gast_mannschaft = gasttore_list[i]
                #update_tipps.tipp_angabe = timezone.now()
                #update_tipps.save()
            if tipp_id[i] is None:
                print('Neuer Tipp')
            #    create_tipp = Tipps(tipper_id = 1, #request.user.id, 
            #                        paarungen_id = tipp.paarungen_id, 
            #                        tipp_tore_heim_mannschaft = heimtore_list[i], 
            #                        tipp_tore_gast_mannschaft = gasttore_list[i], 
            #                        tipp_angabe = timezone.now)
            #    create_tipp.save()
            i += 1
        return redirect('tippen')
    return render(request, 'tippen.html', {'tipps' : tipps})

@csrf_protect
def loginSeite(request):
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        passwort = request.POST['passwort']
        benutzer = authenticate(request, username=benutzername, password=passwort)
        print(f"{benutzer} und {passwort}")
        if benutzer is not None:
            login(request, benutzer)
            print(request)
            return redirect('tippen')
        else:
            print(benutzer)
            None #messages.error(request, 'Benutzername oder Passwort nicht korrekt')
    return render(request, 'loginSeite.html')

def logoutSeite(request):
    logout(request)
    return redirect('startSeite')


def registerSeite(request):
    return render(request, 'registerSeite.html')

def tippen_eingabe(request, id):
    print('Bin Hier')
    return render(request, 'tippen_eingabe.html', {})
