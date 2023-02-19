import functions_framework
from dotenv import dotenv_values

config = dotenv_values('.env')


@functions_framework.http
def send_mail(request):
    return config["HUB_MAIL"]
