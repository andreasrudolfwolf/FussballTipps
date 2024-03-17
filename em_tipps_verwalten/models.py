from django.db import models
from django.utils.timezone import now

class Gruppen(models.Model):
    gruppen_id = models.AutoField(primary_key=True),
    gruppen_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.gruppen_name

class Laender(models.Model):
    land_id = models.AutoField(primary_key=True)
    laender_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.laender_name


class Mannschaften(models.Model):
    mannschaft_id = models.AutoField(primary_key=True)
    mannschaft_name = models.CharField(max_length=100)
    land_id = models.ForeignKey(Laender, models.DO_NOTHING)
    gruppen_id = models.ForeignKey(Gruppen, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.mannschaft_name

class Paarungen(models.Model):
    paarungen_id = models.AutoField(primary_key=True)
    heim_mannschaft_id = models.ForeignKey(Mannschaften, models.DO_NOTHING, related_name = 'heim_mannschaft_id')
    gast_mannschaft_id = models.ForeignKey(Mannschaften, models.DO_NOTHING, related_name = 'gast_mannschaft_id')
    tore_heim_mannschaft = models.IntegerField(default=None, blank=True, null=True)
    tore_gast_mannschaft = models.IntegerField(default=None, blank=True, null=True)
    spiel_termin = models.DateTimeField()
    spiel_ort = models.CharField(max_length=100, blank=True, null=True)
    bemerkung = models.TextField(blank=True, null=True)


class Finalspiele(models.Model):
    final_id = models.AutoField(primary_key=True),
    final_name = models.CharField(max_length=100),
    paarung_id = models.ForeignKey(Paarungen, models.DO_NOTHING, db_column='paarung_id')

    def __str__(self) -> str:
        return self.final_name


class Tipper(models.Model):
    tipper_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_column='Name')  
    vorname = models.CharField(max_length=100, db_column='Vorname') 
    tippername = models.CharField(max_length=100, db_column='Tippername', unique=True)

    def __str__(self) -> str:
        return self.name

class Tipps(models.Model):
    tipp_id = models.AutoField(primary_key=True)
    tipper_id = models.ForeignKey(Tipper, models.DO_NOTHING, db_column='tipper_id')
    paarungen_id = models.ForeignKey(Paarungen, models.DO_NOTHING, db_column='paarungen_id')
    tipp_tore_heim_mannschaft = models.IntegerField()
    tipp_tore_gast_mannschaft = models.IntegerField()
    tipp_angabe = models.DateTimeField(default=now, editable=False)