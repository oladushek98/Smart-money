from django.shortcuts import redirect


class UserAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            redirect('userpage', args=[request.user.id])

        response = self.get_response(request)

        return response
