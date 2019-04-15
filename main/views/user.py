from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['last_name', 'first_name', 'email']
    template_name = 'user_edit.html'

    def get_success_url(self):
        return reverse_lazy('userpage', args=[self.object.id])
