from django.shortcuts import render
from openpyxl import Workbook
from appGestEvenements.forms import ParticipantsForm, AvisForm
from appGestEvenements.models import Participant, Evenement, Avis
from appGestEvenements.utils import sending_email
from django.http import HttpResponse


def inscription(request, even_id):
    # generation code inscription
    # code_id = f"{date.today().month}-{code_generator(6)}-{date.today().day}"
    # form = ParticipantsForm(request.POST or None, initial={"code_insc": code_id, "evenement": evenement})

    evenement = Evenement.objects.get(pk=even_id)
    form = ParticipantsForm(request.POST or None, initial={"evenement": evenement})
    participants = len(Participant.objects.filter(evenement=evenement))

    if request.method == 'POST':
        code_id = form.data["code_insc"]
        print(code_id)
        if form.is_valid():
            if evenement.inscription_limite > participants:
                if not Participant.objects.filter(evenement=evenement, email=form.data["email"]):
                    form.save(commit=True)
                    # sending email to participant by email adress
                    sending_email(recip_email=form.data["email"],
                                  evenement=evenement,
                                  message=f"Merci pour votre inscription {form.data['name']}."
                                          f" Ceci:  {code_id}  est votre code d'accès."
                                          f" Veuillez l'enregistrer, ce dernier vous permettra de noter l'événement")
                    # end sending
                    form.clean()
                    return render(request, 'appGestEvenements/success-full-inscription.html',
                                  context={"code_insc": code_id, "even": evenement})
                else:
                    context = {"form": form, "errors": f"l'adresse *{form.data['email']}* "
                                                       f"existe déjà dans la liste des participants",
                               'even': evenement}
                    return render(request, "appGestEvenements/inscription-form.html", context=context)

            else:
                return render(request, 'appGestEvenements/inscription-termine.html', {"even": evenement})

        else:
            context = {"form": form, "errors": form.errors, 'even': evenement}
            return render(request, "appGestEvenements/inscription-form.html", context=context)

    context = {'form': form, 'even': evenement}
    return render(request, 'appGestEvenements/inscription-form.html', context=context)


def note_form(request, even_id):
    evenement = Evenement.objects.get(pk=even_id)
    form = AvisForm(request.POST, initial={'evenement': evenement})

    if request.method == "POST":
        if form.is_valid():
            participant = Participant.objects.filter(code_insc=form.data['code_id']).first()
            if participant:
                test_avis = Avis.objects.filter(participant=participant)
                if not test_avis:
                    Avis.objects.create(
                        evenement=evenement,
                        participant=participant,
                        sujets_que_vous_aimeriez_voir_abordes=form.data[
                            "sujets_que_vous_aimeriez_voir_abordes"],
                        participer_a_autres_evenements_de_ce_type=form.data[
                            "participer_a_autres_evenements_de_ce_type"],
                        l_themes_abord_ont_ils_ete_pertinents_sln_vous=form.data[
                            "l_themes_abord_ont_ils_ete_pertinents_sln_vous"],
                        inviteriez_vous_une_amie_prochainement=form.data["inviteriez_vous_une_amie_prochainement"],
                        avez_vous_besoin_d_un_accompagnement_personalise=form.data[
                            "avez_vous_besoin_d_un_accompagnement_personalise"],
                        vos_attentes_ont_elles_ete_comblees=form.data["vos_attentes_ont_elles_ete_comblees"],
                        quelles_etaient_vos_attentes=form.data["quelles_etaient_vos_attentes"],
                        que_pensez_vous_du_concept=form.data["que_pensez_vous_du_concept"],
                    )
                    return render(request, "appGestEvenements/success-full-note.html", context={"even": evenement})
                else:
                    context = {'form': form, 'even': evenement,
                               "errors": f"l'avis du participant(e) {participant.email} existe déjà"}
                    return render(request, 'appGestEvenements/avis-form.html', context=context)

            else:
                context = {'form': form, 'even': evenement,
                           "errors": f"code d'acces **{form.data['code_id']}** incorrect"}
                return render(request, 'appGestEvenements/avis-form.html', context=context)
        else:
            context = {'form': form, 'even': evenement, "errors": form.errors}
            return render(request, 'appGestEvenements/avis-form.html', context=context)
    context = {'form': form, 'even': evenement}
    return render(request, template_name="appGestEvenements/avis-form.html", context=context)


def export_avis_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="avis.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Avis"
    headers = [
        "Que_ pensez_vous_du_concept",
        "Quelles_etaient_vos_attentes",
        "Vos_attentes_ont_elles_ete_comblees",
        "Les_themes_abordes_ont_ils_ete_pertinents_selon_vous",
        "Souhaiteriez_vous_participer_a_autres_evenements_de_ce_type",
        "Quels_sont_les_sujets_que_vous_aimeriez_voir_abordes_lors_des_prochaines_rencontres",
        "Inviteriez_vous_une_amie_prochainement",
        "Avez_vous_besoin_un_accompagnement_personalise",
        "CreatedAt",
        "Evenement",
        "Participant"]

    ws.append(headers)
    x_avis = Avis.objects.all()
    for avis in x_avis:
        ws.append([avis.que_pensez_vous_du_concept, avis.quelles_etaient_vos_attentes,
                   avis.vos_attentes_ont_elles_ete_comblees, avis.l_themes_abord_ont_ils_ete_pertinents_sln_vous,
                   avis.participer_a_autres_evenements_de_ce_type,
                   avis.sujets_que_vous_aimeriez_voir_abordes,
                   avis.inviteriez_vous_une_amie_prochainement,
                   avis.avez_vous_besoin_d_un_accompagnement_personalise,
                   str(avis.created_at),
                   avis.evenement.name_evenement, avis.participant.name])

    wb.save(response)
    return response


def export_participants_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="participants.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Participant"
    headers = ["Id", "Code_insc", "Nom_&Prenom", "Email",
               "Residence", "Telephone", "Profession",
               "Secteur_Activite",
               "Commment_avez_vous_entendu_parler_des_rencontres_ELLE",
               "Connaissez_vous_archer_Capital",
               "Recevoir_infos",
               "Created_At"]

    ws.append(headers)
    participants = Participant.objects.all()
    for participant in participants:
        ws.append([participant.id, participant.code_insc,
                   participant.name, participant.email,
                   participant.residence, participant.phone_number,
                   participant.profession.libelle,
                   participant.secteur_activite.intitule,
                   participant.cmt_avz_entendu_parler_d_activite,
                   participant.cnssez_vous_larcher_capital,
                   participant.recevoir_infos,
                   str(participant.created_at)
                   ])

    wb.save(response)
    return response
