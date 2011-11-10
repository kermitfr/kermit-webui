'''
Created on Sep 20, 2011

@author: mmornati
'''
import csv
#import xlwt
import logging
from webui.serverdetails import utils

logger = logging.getLogger(__name__)

def generate_csv_server(user, response):
    """
    Generates an CSV with servers list
    """
    writer = csv.writer(response, delimiter=';')
    writer.writerow(["UsedName","Name","BU","Projet","Status","Zone","Type"])
    servers = utils.extract_user_servers(user)
    logger.info("Generating servers CSV")
    logger.debug("Found %s servers" % len(servers))
    for server in servers:
        classes = []
        for i in range(0,5):
            values = server.puppet_classes.filter(level=i).values()
            if values:
                classes.append(values[0]['name'])
            else:
                classes.append('')
        writer.writerow([server.fqdn, server.hostname, classes[0], classes[1], classes[2], classes[3], classes[4]])

#def generate_xls_server(response):
#    wb = xlwt.Workbook()
#    ws = wb.add_sheet('Servers Farm')
#    
#    ws.write(0, 0, 'UsedName')
#    ws.write(0, 1, 'Name')
#    ws.write(0, 2, 'BU')
#    ws.write(0, 3, 'Projet')
#    ws.write(0, 4, 'Status')
#    ws.write(0, 5, 'Zone')
#    ws.write(0, 6, 'Type')
#    servers = Server.objects.all()
#    logger.info("Generating server XLS")
#    logger.debug("Found %s servers" % len(servers))
#    counter = 1
#    for server in servers:
#        classes = []
#        for i in range(0,5):
#            values = server.puppet_classes.filter(level=i).values()
#            if values:
#                classes.append(values[0]['name'])
#            else:
#                classes.append('')
#        ws.write(counter, 0, server.fqdn)
#        ws.write(counter, 1, server.hostname)
#        ws.write(counter, 2, classes[0])
#        ws.write(counter, 3, classes[1])
#        ws.write(counter, 4, classes[2])
#        ws.write(counter, 5, classes[3])
#        ws.write(counter, 6, classes[4])
#        counter = counter + 1
#
#    wb.save(response)
#    return response