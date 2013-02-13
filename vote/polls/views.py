from django.views.generic import TemplateView


class ListPollsView(TemplateView):
    template_name = "polls/list_polls.html"
