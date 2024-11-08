# Generated by Django 5.0.6 on 2024-11-08 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name_evenement', models.CharField(max_length=250, unique=True)),
                ('edition', models.CharField(max_length=300)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('inscription_limite', models.IntegerField(default=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('banniere_1', models.ImageField(blank=True, null=True, upload_to='evenements/banniere/', verbose_name='Bannière 1')),
                ('banniere_2', models.ImageField(blank=True, null=True, upload_to='evenements/banniere/', verbose_name='Bannière 2')),
            ],
            options={
                'verbose_name': 'Evénement',
                'verbose_name_plural': 'Evénements',
            },
        ),
        migrations.CreateModel(
            name='EvenProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('libelle', models.CharField(max_length=250, unique=True)),
                ('autre_infos', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Profession',
                'verbose_name_plural': 'Professions',
            },
        ),
        migrations.CreateModel(
            name='EvenSecteurActivite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('intitule', models.CharField(max_length=250, unique=True)),
                ('autres_infos', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': "Secteur d'activité",
                'verbose_name_plural': "Secteurs d'activités",
            },
        ),
        migrations.CreateModel(
            name='EvenSondage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, unique=True)),
                ('libelle', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code_insc', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(db_index=True, max_length=300)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('residence', models.CharField(choices=[('BRAZZAVILLE', 'Brazzaville'), ('POINTE-NOIRE', 'Pointe-Noire')], default='BRAZZAVILLE', max_length=200)),
                ('phone_number', models.CharField(db_index=True, max_length=200)),
                ('cmt_avz_entendu_parler_d_activite', models.CharField(choices=[('PROSPECTION', 'Prospection'), ('RESEAUX-SOCIAUX', 'Réseaux sociaux'), ('BOUCHE-A-OREILLE', 'Bouche à oreille')], default='PROSPECTION', max_length=200)),
                ('cnssez_vous_larcher_capital', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], default='NON', max_length=10)),
                ('recevoir_infos', models.BooleanField(default=False)),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestEvenements.evenement')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestEvenements.evenprofession')),
                ('secteur_activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestEvenements.evensecteuractivite')),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('que_pensez_vous_du_concept', models.CharField(blank=True, max_length=300, null=True)),
                ('quelles_etaient_vos_attentes', models.CharField(blank=True, max_length=300, null=True)),
                ('vos_attentes_ont_elles_ete_comblees', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], default='OUI', max_length=300)),
                ('l_themes_abord_ont_ils_ete_pertinents_sln_vous', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], default='OUI', max_length=300)),
                ('participer_a_autres_evenements_de_ce_type', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], default='OUI', max_length=300)),
                ('sujets_que_vous_aimeriez_voir_abordes', models.TextField(blank=True, null=True)),
                ('inviteriez_vous_une_amie_prochainement', models.CharField(blank=True, max_length=300, null=True)),
                ('avez_vous_besoin_un_accompagnement_personalise', models.CharField(choices=[('OUI', 'Oui'), ('NON', 'Non')], default='NON', max_length=300)),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis', to='appGestEvenements.evenement')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appGestEvenements.participant')),
            ],
            options={
                'verbose_name': 'Avis',
                'verbose_name_plural': 'Avis',
            },
        ),
    ]