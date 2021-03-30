from userpreferences.models import UserPreferences


def userpreferences(request):
    if request.user.is_authenticated:
        preferences = UserPreferences.objects.get(
            user=request.user
        )
        print(preferences)
        return{'preferences': preferences}
    else:
        return ''
