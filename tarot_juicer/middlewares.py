from django.http import HttpResponseRedirect
from django.urls import reverse


def authentication_middleware(get_response):

    def middleware(request):
        if not request.user.is_authenticated and request.path != reverse('index'):
            return HttpResponseRedirect(reverse('index'))

        response = get_response(request)

        return response

    return middleware
