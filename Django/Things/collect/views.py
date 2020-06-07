from django.views.generic.base import TemplateView

from accounts.models import User

class Index(TemplateView):

    template_name = 'collect/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_history'] = User.transaction_history.analyse('by_month', 'by_type', 'next_collection')
        return context

    # You can access the data for homepage this way:
    #
    # transaction_history.by_type —> a list of dictionary {column name: value} e.g.
    #
    # [
    # 	{“metal”: 3},
    # 	{“plastic”: 5},
    # 	…
    # ]
    # 
    # transaction_history.by_month —> a list of dictionary
    #
    # [
    # 	{“Jan”: 3},
    # 	{“Feb”: 5},
    # 	…
    # ]
    #
    # transaction_history.next_collection —> object
    #
    # day = object.day
    # month = object.month
    # year = object.year
