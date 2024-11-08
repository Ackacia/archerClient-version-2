from django.db import models

YES_OR_NO_CHOICES = (
    ("OUI", "Oui"),
    ("NON", "Non")
)

YES_OR_NO_OR_PT_CHOICES = (
        ('OUI', 'Oui'),
        ('PEUT-ETRE', 'Peut-être'),
        ('NON', 'Non'),
    )


class EvenProfession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    libelle = models.CharField(max_length=250, unique=True)
    autre_infos = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Profession"
        verbose_name_plural = "Professions"

    def __str__(self):
        return self.libelle


class EvenSecteurActivite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    intitule = models.CharField(max_length=250, unique=True)
    autres_infos = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Secteur d'activité"
        verbose_name_plural = "Secteurs d'activités"

    def __str__(self):
        return self.intitule


class Evenement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name_evenement = models.CharField(max_length=250, null=False,
                                      unique=True)
    edition = models.CharField(max_length=300, null=False)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    inscription_limite = models.IntegerField(default=100)
    description = models.TextField(blank=True, null=True)
    banniere_1 = models.ImageField(upload_to="evenements/banniere/",
                                   null=True, blank=True,
                                   verbose_name="Bannière 1")
    banniere_2 = models.ImageField(upload_to="evenements/banniere/",
                                   null=True, blank=True,
                                   verbose_name="Bannière 2")

    def __str__(self):
        return self.name_evenement

    class Meta:
        verbose_name = "Evénement"
        verbose_name_plural = "Evénements"


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    code_insc = models.CharField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=300, null=False, db_index=True)
    email = models.EmailField(db_index=True, null=False)

    RESIDENCE_CHOICES = (
        ("BRAZZAVILLE", "Brazzaville"),
        ("POINTE-NOIRE", "Pointe-Noire"),
    )

    residence = models.CharField(max_length=200, choices=RESIDENCE_CHOICES, default="BRAZZAVILLE")
    phone_number = models.CharField(max_length=200, db_index=True, null=False)
    profession = models.ForeignKey(EvenProfession, on_delete=models.CASCADE)
    secteur_activite = models.ForeignKey(EvenSecteurActivite, on_delete=models.CASCADE)

    PIST_CHOICES = (
        ("PROSPECTION", "Prospection"),
        ("RESEAUX-SOCIAUX", "Réseaux sociaux"),
        ("BOUCHE-A-OREILLE", "Bouche à oreille")
    )

    cmt_avz_entendu_parler_d_activite = models.CharField(max_length=200,
                                                         choices=PIST_CHOICES,
                                                         default="PROSPECTION")
    cnssez_vous_larcher_capital = models.CharField(max_length=10, default="NON", choices=YES_OR_NO_CHOICES)
    recevoir_infos = models.BooleanField(default=False)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class EvenSondage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    libelle = models.CharField(max_length=250)

    def __str__(self):
        return self.libelle


class Avis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    que_pensez_vous_du_concept = models.CharField(max_length=300, null=True, blank=True)
    quelles_etaient_vos_attentes = models.CharField(max_length=300, null=True, blank=True)
    vos_attentes_ont_elles_ete_comblees = models.CharField(max_length=300,
                                                           choices=YES_OR_NO_CHOICES, default="OUI")
    l_themes_abord_ont_ils_ete_pertinents_sln_vous = models.CharField(max_length=300,
                                                                      choices=YES_OR_NO_CHOICES,
                                                                      default="OUI")
    participer_a_autres_evenements_de_ce_type = models.CharField(max_length=300,
                                                                 choices=YES_OR_NO_CHOICES,
                                                                 default="OUI")
    sujets_que_vous_aimeriez_voir_abordes = models.TextField(null=True, blank=True)
    inviteriez_vous_une_amie_prochainement = models.CharField(max_length=300, null=True, blank=True)
    avez_vous_besoin_un_accompagnement_personalise = models.CharField(max_length=300,
                                                                      choices=YES_OR_NO_CHOICES,
                                                                      default="NON")
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="avis")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} ({self.participant.name})"

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"





