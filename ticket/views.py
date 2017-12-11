from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from utils.func import is_member

from .models import Ticket


class TicketCreateView(generic.CreateView):
    model = Ticket
    fields = ['type', 'details']
    template_name = "ticket/ticket_createview.html"
    success_url = reverse_lazy("ticket:applied_listview")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class AppliedListView(generic.ListView):
    model = Ticket
    template_name = "ticket/applied_listview.html"

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user).order_by('-status')


class ReceivedListView(generic.ListView):
    model = Ticket
    template_name = "ticket/received_listview.html"
    ordering = ['-status']


class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = "ticket/ticket_detailview.html"

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data()
        context['pk'] = self.object.pk
        if is_member(self.request.user, 'TicketSupportTeam'):
            context['support_team'] = True
        return context


def mark_as_solved(request, pk):
    if request.method == "POST":
        obj = Ticket.objects.get(id=pk)
        obj.propose_solution(request.user)
        return HttpResponseRedirect(reverse("ticket:ticket_detailview", args=[pk]))
    context = {
        "ticket_no": pk,
    }
    return render(request, "ticket/mark_as_solved.html", context)


def deny_ticket_solution(request, pk):
    if request.method == "POST":
        obj = Ticket.objects.get(id=pk)
        obj.deny_solution()
        return HttpResponseRedirect(reverse("ticket:ticket_detailview", args=[pk]))
    context = {
        "ticket_no": pk,
    }
    return render(request, "ticket/deny_ticket_solution.html", context)


def accept_ticket_solution(request, pk):
    if request.method == "POST":
        obj = Ticket.objects.get(id=pk)
        obj.accept_solution()
        return HttpResponseRedirect(reverse("ticket:ticket_detailview", args=[pk]))
    context = {
        "ticket_no": pk,
    }
    return render(request, "ticket/accept_ticket_solution.html", context)


def ticket_list(request):
    if is_member(request.user, 'TicketSupportTeam'):
        return HttpResponseRedirect(reverse("ticket:received_listview"))
    else:
        return HttpResponseRedirect(reverse("ticket:applied_listview"))

