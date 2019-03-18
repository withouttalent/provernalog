from django.shortcuts import render_to_response, render, redirect
from django.template.loader import render_to_string
from provernalog.models import *
from django.core.mail import send_mail
from provernalog.utils import ParcelMainInformation, RequestWord
from django.shortcuts import get_object_or_404
from user_profile.models import Report, SourceReport
from django.core.mail import EmailMessage
from django.views.generic import View
from .forms import SupportForm, WordForm


class CommonView(View):
    template_name = 'index.html'
    title = "ПроверьНалог"

    def get(self, request):
        return render_to_response(self.template_name, {"Title": self.title})


class SearchView(View):

    def get(self, request):
        try:
            parcel = Parcel.objects.get(cadastral_number=request.GET.get('cadastral_number'))
            context = {"Title": "Данные объекта",
                       'support_form': SupportForm({"cadastral_number": parcel.cadastral_number}),
                       'word_form': WordForm({"cadastral_number": parcel.cadastral_number}),
                       'thanks': request.GET.get('thanks'),
                       'parcel': ParcelMainInformation(parcel)
                       }
            return render(request, "provernalog/search.html", context)
        except Parcel.DoesNotExist:
            source_reports = SourceReport.objects.all()
            return render(request, "provernalog/non-search.html", {"empty_cadastral_number": request.GET['cadastral_number'],
                                                       "source_reports": source_reports, "Title": "Объект не найден"})

    def post(self, request):
        support = SupportForm(request.POST)
        if support.is_valid():
            support = support.save()
            parcel = Parcel.objects.get(cadastral_number=support.cadastral_number)
            if request.POST.get('factors'):
                parcel_context = ParcelMainInformation(parcel)
                message = render_to_string('EmailKit/email.html', context={"parcel": parcel_context})
                title = f'Данные объекта {support.cadastral_number}'
                send_mail(title, message, "robot@provernalog.ru", recipient_list=[support.email],
                          fail_silently=False, html_message=message)
                thanks = 'Спасибо за обращение. Письмо с подробностями о вашем объекте отправлено на указанный почтовый адрес.'
            if request.POST.get('word'):
                email = EmailMessage(
                    'Заявление в ГБУ',
                    '',
                    'robot@provernalog.ru',
                    [support.email],
                )
                try:
                    word = RequestWord(parcel, support)
                    docx = word.create_word_file()
                    email.attach(f'{support.cadastral_number}.docx', docx.read(), 'application/word')
                    email.send()
                    thanks = "Бланк заявления отправлен на указанный адрес"
                except ValueError:
                    thanks = "Форма для вашего региона еще не создана"
            return redirect(f'/search-res/?cadastral_number={request.POST["cadastral_number"]}&thanks={thanks}')



def analytics(request, region=None):
    context = {}
    if region:
        reports = Report.objects.filter(city__region=int(region))
        context['reports'] = reports
    else:
        reports = Report.objects.all()[:10]
        context['reports'] = reports
    return render_to_response('user_profile/analytics.html', context)


def report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    context = {
        "report": report,
    }
    return render_to_response('user_profile/report.html', context=context)
