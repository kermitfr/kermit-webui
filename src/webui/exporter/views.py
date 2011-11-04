# Create your views here.
from django.http import HttpResponse
from webui.exporter import utils

def export_servers_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=servers.csv'
    utils.generate_csv_server(request.user, response)
    return response

def export_servers_xls(request):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=servers.xls'
#    utils.generate_xls_server(response)
    return response