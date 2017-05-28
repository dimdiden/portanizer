from posts.forms import TagMultiplyForm


def get_formMultyTag(request):
    return {'formMultyTag': TagMultiplyForm()}
