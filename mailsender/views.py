from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


from mailsender.forms import MailingForm, MailTextForm, CustomerCreateForm
from mailsender.models import Mailing, Logs, Customer


class DispatchMixin:
    """
    Класс, который запрещает доступ к объектам, создателями которых не является текущий пользователь
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator != self.request.user:
            return HttpResponseForbidden(
                "У вас нет прав на редактирование или удаление продукта, создателем которого вы не являетесь."
            )
        return super().dispatch(request, *args, **kwargs)


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_path'] = self.request.path
        return context


class HomeListView(ListView):
    """
    Класс для отображения главной страницы сайта.
    """
    model = Mailing
    template_name = 'mailsender/home.html'


class ContactsView(View):
    """
    Класс для отображения страницы поддержки.
    """
    template_name = 'mailsender/contacts.html'

    def get(self, request):
        return render(request, self.template_name)


class MailingManagementListView(LoginRequiredMixin, ContextMixin, ListView):
    """
    Представление для вкладки "Управление рассылками" в меню сайта
    """
    model = Mailing
    template_name = 'mailsender/mailing_management_list.html'


class MailingManagementDetailView(LoginRequiredMixin, ContextMixin, DispatchMixin, DetailView):
    """
    Представление для подробного просмотра рассылки
    """
    model = Mailing
    template_name = 'mailsender/mailing_management_detail.html'


class MailingManagementUpdateView(LoginRequiredMixin, ContextMixin, DispatchMixin, UpdateView):
    """
    Представление для обновления данных рассылки
    """
    model = Mailing
    form_class = MailingForm
    template_name = 'mailsender/mailing_management_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm(instance=self.object)
        context['mailtext_form'] = MailTextForm(instance=self.object.messages)
        return context

    def form_valid(self, form):
        mailing_form = MailingForm(self.request.POST, instance=self.object)
        mailtext_form = MailTextForm(self.request.POST, instance=self.object.messages)

        if mailing_form.is_valid() and mailtext_form.is_valid():
            mailing = mailing_form.save(commit=False)

            # получение из формы периодичности рассылки
            periodicity = self.request.POST.get('periodicity')
            if periodicity == 'every_day':
                mailing.every_day = True
                mailing.every_week = False
                mailing.every_month = False
            elif periodicity == 'every_week':
                mailing.every_day = False
                mailing.every_week = True
                mailing.every_month = False
            elif periodicity == 'every_month':
                mailing.every_day = False
                mailing.every_week = False
                mailing.every_month = True

            mailtext_form.save()
            mailing.save()
            return super().form_valid(form)

            mailtext_form.save()
            mailing.save()

            return super().form_valid(form)

        else:
            return render(self.request, self.template_name,
                          {'mailing_form': mailing_form, 'mailtext_form': mailtext_form})

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})


class MailingManagementCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания рассылки.
    """

    model = Mailing
    form_class = MailingForm
    template_name = 'mailsender/mailing_create.html'

    # Здесь передаем в контекст две формы для заполнения
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm
        context['mailtext_form'] = MailTextForm
        return context

    def form_valid(self, form):
        mail_text_form = MailTextForm(self.request.POST)

        mailing = form.save(commit=False)
        mail_text = mail_text_form.save(commit=False)

        mail_text.creator = self.request.user
        mail_text.save()

        mailing.messages = mail_text
        mailing.creator = self.request.user
        periodicity = self.request.POST.get('periodicity')
        if periodicity == 'every_day':
            mailing.every_day = True
        elif periodicity == 'every_week':
            mailing.every_week = True
        else:
            mailing.every_month = True

        logs = Logs.objects.create()
        mailing.logs = logs
        mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailsender:mailing_management_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DispatchMixin, DeleteView):
    """
    Класс для удаления рассылки
    """
    model = Mailing
    template_name = 'mailsender/mailing_delete.html'
    success_url = reverse_lazy('mailsender:home')


class CustomersListView(LoginRequiredMixin, ListView):
    """
    Представление для вкладки "Управление клиентами" в меню сайта
    """
    model = Customer
    template_name = 'mailsender/customers_list_view.html'


class CustomersCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания клиента
    """
    model = Customer
    template_name = 'mailsender/customers_create_view.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('mailsender:customers_list')

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.creator = self.request.user
        customer.save()
        return super().form_valid(form)


class CustomersUpdateView(LoginRequiredMixin, DispatchMixin, UpdateView):
    """
    Представление для обновления данных клиента
    """
    model = Customer
    template_name = 'mailsender/customers_update_view.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('mailsender:customers_list')


class CustomersDeleteView(LoginRequiredMixin, DispatchMixin, DeleteView):
    """
    Представление для обновления удаления клиента
    """
    model = Customer
    template_name = 'mailsender/customer_delete.html'
    success_url = reverse_lazy('mailsender:customers_list')
