from django.shortcuts import render
from django.views import generic
from itertools import chain
from django.http import JsonResponse

from .models import Thread, Message


class ThreadListView(generic.ListView):
    model = Thread
    template_name = "msgs/msgs-listview.html"

    def get_queryset(self):
        qs1 = Thread.objects.filter(user1=self.request.user)
        qs2 = Thread.objects.filter(user2=self.request.user)
        merged = chain(qs1, qs2)
        return merged


def fetch_msg(request, pk):
    msgs = Message.objects.filter(thread_id=pk)

    context = {
        "msgs": msgs,
    }
    return render(request, "msgs/fetch-msg.html", context)


def send_msg(request):
    if request.method == "POST":
        author = request.user
        text = request.POST.get('text', '')
        receiver = request.POST.get('receiver', '')

        if author.id < receiver.id:
            thread, created = Thread.objects.get_or_create(user1=author, user2=receiver, defaults={"user1_read": True, "user2_read": False})
        elif author.id > receiver.id:
            thread, created = Thread.objects.get_or_create(user1=receiver, user2=author, defaults={"user1_read": True, "user2_read": False})
        else:
            return

        message = Message.objects.create(thread=thread, author=author, text=text, receiver=receiver)

        return JsonResponse({"message": message})
    else:
        return

