from App.models import UserModel


def get_user(username):
    try:
        user = UserModel.objects.get(u_name=username)
        return user
    except:
        return None
