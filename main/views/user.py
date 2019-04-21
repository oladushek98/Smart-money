from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from wkhtmltopdf.views import PDFTemplateResponse, PDFTemplateView

from main.forms import EditBioForm
from main.models import UserAdditionalInfo, FinancialNode
from main.utils import PDFConverter


class UserUpdateBioView(LoginRequiredMixin, FormView):
    form_class = EditBioForm
    template_name = 'user_edit.html'

    def get(self, request, *args, **kwargs):

        user = User.objects.filter(id=request.user.id).first()
        additional = UserAdditionalInfo.objects.filter(user_id=request.user.id).first()

        last = user.last_name
        first = user.first_name
        email = user.email
        currency = additional.currency

        form = EditBioForm(initial={'last_name': last, 'first_name': first, 'email': email, 'currency': currency})

        return render(request, template_name='user_edit.html', context={'form': form})

    def form_valid(self, form):
        last_name = form.cleaned_data.get('last_name').title()
        first_name = form.cleaned_data.get('first_name').title()
        email = form.cleaned_data.get('email')

        User.objects.filter(id=self.request.user.id).update(last_name=last_name, first_name=first_name, email=email)

        currency = form.cleaned_data.get('currency')
        UserAdditionalInfo.objects.filter(user_id=self.request.user.id).update(currency=currency)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('userpage')


class GeneratePDF(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        template = get_template('report.html')
        operations = FinancialNode.objects.filter(user_id=request.user.id).prefetch_related('income')
        context = {
            'arg': 'Hello',
            'operations': operations
        }
        pdf = PDFConverter.render_to_pdf('report.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f'Report_{54}'
            content = f'inline; filename=\'{filename}\''
            download = request.GET.get("download")

            if download:
                content = f'attachment; filename=\'{filename}\''

            response['Content-Disposition'] = content

            return response

        return HttpResponse('Not found!')
