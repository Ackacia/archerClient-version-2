from io import BytesIO
import qrcode
from PIL import Image, ImageDraw
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook

from appServicesEvals.forms import EvaluationGlobalForm, EvaluationUniqueForm
from appServicesEvals.models import Conseiller, Evaluation


def export_conseiller_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="conseillers.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Export Cenceillers"

    headers = ["Created_At", "Id", "Nom du conseiller",
               "Email", "Telephone", "Profession",
               "Secteur d'activite", "Totale note"]

    ws.append(headers)
    conseillers = Conseiller.objects.all()

    for conseiller in conseillers:
        ws.append([str(conseiller.created_at),
                   conseiller.id, conseiller.nom_conseiller,
                   conseiller.email, conseiller.telephone, conseiller.profession.libelle,
                   conseiller.secteur_activite.intitule, len(conseiller.evaluations.all())])

    wb.save(response)
    return response


def export_evaluation_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="evaluation_services.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Evaluations des services"

    headers = ["created_At", "Id", "nom_client", "email_client",
               "telephone_client", "profession_client",
               "secteur_activite_client", "evaluation_sondages",
               "comment_avez_vous_connu_l'Archer_capital",
               "recommanderiez_vous_l'Archer_capital", "commentaire",
               "nous_suivez_vous_sur_les_reseaux",
               "produit_souscrit", "conseiller"]

    ws.append(headers)
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        ws.append([str(evaluation.created_at), evaluation.id,
                   evaluation.nom_client, evaluation.email_client,
                   evaluation.telephone_client, evaluation.profession_client.libelle,
                   evaluation.secteur_activite_client.intitule,
                   evaluation.evaluation_sondages.libelle, evaluation.comment_avez_vous_connu_lArcher_capital,
                   evaluation.recommanderiez_vous_lArcher_capital,
                   evaluation.commentaire, evaluation.nous_suivez_vous_sur_les_reseaux,
                   evaluation.produit_souscrit.nom_produit,
                   evaluation.conseiller.nom_conseiller])

    wb.save(response)
    return response


def download_global_qr_code(request):
    qr_image = qrcode.make(request.build_absolute_uri(f'/service-evaluation/global-form/'))
    canvas = Image.new("RGB", (qr_image.pixel_size, qr_image.pixel_size), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qr_image)
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    canvas.close()
    return HttpResponse(buffer.getvalue(),
                        content_type="test/png")


def dashboard(request):
    return render(request, template_name="appServicesEvals/dashboard.html", context={})


def evaluation_global_view(request):
    form = EvaluationGlobalForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit=True)
            return render(request, "appServicesEvals/merci.html", context={})
        else:
            return render(request, "appServicesEvals/eval_global_form.html", context={"form": form, "errors": form.errors})

    return render(request, "appServicesEvals/eval_global_form.html", context={"form": form})


def evaluation_unique_view(request, pk):
    form = EvaluationUniqueForm(request.POST or None, initial={"conseiller": Conseiller.objects.get(pk=pk)})

    if request.method == "POST":
        if form.is_valid():
            form.save(commit=True)
            return render(request, "appServicesEvals/merci.html", context={})
        else:
            return render(request, "appServicesEvals/eval_unique_form.html", context={"form": form, "errors": form.errors})

    return render(request, "appServicesEvals/eval_unique_form.html", context={"form": form})


