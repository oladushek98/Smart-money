from django.shortcuts import redirect
from main.models import Transaction


class TransactionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            trans = 'transaction'
            cur_path = request.path.split('/')

            if trans in request.path and cur_path[-1].isdigit():
                # cur_path = request.path.split('/')
                cur_id = int(cur_path[-1])
                cur_trans = Transaction.objects.filter(id=cur_id).first()

                if cur_trans.delete:
                    return redirect('userpage')

            response = self.get_response(request)

            return response

        except ValueError:

            pass
