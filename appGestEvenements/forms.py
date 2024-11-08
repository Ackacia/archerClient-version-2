from datetime import date

from django import forms
from django.forms import TextInput, Select, Textarea

from appGestEvenements.models import Participant, Avis, YES_OR_NO_CHOICES, Evenement, YES_OR_NO_OR_PT_CHOICES, \
    EvenProfession, EvenSecteurActivite
from appGestEvenements.utils import code_generator


class ParticipantsForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre nom et prénom'
    }))

    email = forms.EmailField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre email'
    }))

    phone_number = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre Téléphone'
    }))

    residence = forms.ChoiceField(choices=Participant.RESIDENCE_CHOICES, widget=Select(attrs={
        'class': 'form-control',
    }))

    proffession = forms.ModelChoiceField(queryset=EvenProfession.objects, widget=Select(attrs={
        'class': 'form-control',
        'placeholder': 'Votre profession'
    }))

    secteur_activite = forms.ModelChoiceField(queryset=EvenSecteurActivite.objects, widget=Select(attrs={
        'class': 'form-control',
        'placeholder': "Votre secteur d'activité"
    }))

    cmt_avz_entendu_parler_d_activite = forms.ChoiceField(choices=Participant.PIST_CHOICES,
                                                          widget=Select(
                                                                                  attrs={'class': 'form-control',
                                                                                         }))

    cnssez_vous_larcher_capital = forms.ChoiceField(choices=YES_OR_NO_CHOICES,
                                                    required=True,
                                                    widget=forms.RadioSelect(attrs={'class': 'form-control-inline'}),
                                                    )

    recevoir_infos = forms.BooleanField(required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-control-inline',
                                                                          'style': 'width: 18px; height: 18px;'}))
    # generation code inscription
    code_id = f"{date.today().month}-{code_generator(6)}-{date.today().day}"

    code_insc = forms.CharField(max_length=200, initial=code_id,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Code Iscription'}))
    evenement = forms.ModelChoiceField(queryset=Evenement.objects,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Participant
        fields = "__all__"


class AvisForm(forms.ModelForm):
    code_id = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "2-DG6EG-203"
    }))

    que_pensez_vous_du_concept = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'style': 'height: 130px;'
    }), required=False, empty_value=True)

    quelles_etaient_vos_attentes = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'style': 'height: 130px;'
    }), required=False, empty_value=True)

    vos_attentes_ont_elles_ete_comblees = forms.ChoiceField(choices=YES_OR_NO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    l_themes_abord_ont_ils_ete_pertinents_sln_vous = forms.ChoiceField(choices=YES_OR_NO_CHOICES,
                                                                       widget=forms.Select(attrs={
                                                                                 'class': 'form-control',
                                                                             }))

    participer_a_autres_evenements_de_ce_type = forms.ChoiceField(
        choices=YES_OR_NO_CHOICES, widget=forms.Select(attrs={
            'class': 'form-control',
        }))

    sujets_que_vous_aimeriez_voir_abordes = forms.CharField(
        widget=Textarea(attrs={
            'class': 'form-control', 'style': 'height: 130px;'
        }), required=False, empty_value=True)

    inviteriez_vous_une_amie_prochainement = forms.ChoiceField(choices=YES_OR_NO_OR_PT_CHOICES,
                                                               widget=Select(attrs={
                                                                   'class': 'form-control'}))

    avez_vous_besoin_d_un_accompagnement_personalise = forms.ChoiceField(choices=YES_OR_NO_CHOICES, widget=Select(attrs={
        'class': 'form-control'}))

    participant = forms.ModelChoiceField(required=False, queryset=Participant.objects,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    evenement = forms.ModelChoiceField(required=False, queryset=Evenement.objects,
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Avis
        fields = "__all__"
