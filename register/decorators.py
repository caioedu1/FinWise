from django.shortcuts import redirect


# Simple login_forbidden decorator
def login_forbidden(view_func):
    """
    Decorator for views that checks that the user is logged in, and not
    allowing user to access that views if so.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            # Caso contrário, execute a view normalmente
            return view_func(request, *args, **kwargs)
    return _wrapped_view