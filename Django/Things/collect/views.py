from django.views.generic.base import TemplateView

from accounts.models import User

class Index(TemplateView):

    template_name = 'collect/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_history'] = User.transaction_history.analyse('by_month', 'by_type', 'next_collection')
        return context
