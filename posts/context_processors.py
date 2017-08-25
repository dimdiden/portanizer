from .forms import TagMultiplyForm

# https://stackoverflow.com/questions/2893724/creating-my-own-context-processor-in-django
def get_formMultyTag(request):
    if not request.user.is_anonymous:
        return {'formMultyTag': TagMultiplyForm(user=request.user)}
    else:
        return {}
