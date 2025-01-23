from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=50)  # Prénom
    last_name = models.CharField(max_length=50)   # Nom
    email = models.EmailField(unique=True)        # Email unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Numéro de téléphone
    date_of_birth = models.DateField()            # Date de naissance
    is_active = models.BooleanField(default=True) # Statut actif/inactif

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Performance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # Liaison avec le membre
    date = models.DateField()                                     # Date de la performance
    distance = models.FloatField()                                # Distance en mètres
    time = models.FloatField()                                    # Temps en secondes
    heart_rate = models.IntegerField(blank=True, null=True)       # Fréquence cardiaque moyenne

    def __str__(self):
        return f"Performance of {self.member} on {self.date}"
