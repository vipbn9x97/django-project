from datetime import datetime
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import logging
import pandas as pd
from django.db import transaction

# Create your views here.


def index(request):
    return render(request, './pth/index.html')

# (method, url, body=None, headers={})


@transaction.atomic
@api_view(['GET'])
def getOutput(request):
    passValue = []
    failValue = []
    yieldrate = []
    data = []
    failData = 0
    passData = 0
    # data = (pd.DataFrame(columns=['NULL'],
    #                          index=pd.date_range('2022-03-22T07:30:00Z', '2022-03-22T19:30:00Z',
    #                                              freq='1H')).to_json())
    # logger.info(data)
    listTime = (pd.DataFrame(columns=['NULL'],
                             index=pd.date_range('2022-03-22T07:30:00Z', '2022-03-22T19:30:00Z',
                                                 freq='1H'))
                .between_time('08:30', '19:30')
                .index.strftime('%Y-%m-%d %H:%M:%S')
                .tolist()
                )
    # query = "select case when "
    # for index, time in enumerate(listTime):
    try:
        logger = logging.getLogger('django')
        with connection.cursor() as cursor:
            query = "select date_bin('1 hour', Time, TIMESTAMP '2022-03-24 07:30:00') as Time, Status, count (*) as Total \
                from tbl_pcb_result where time between '2022-03-22 07:30:00' and '2022-03-22 19:30:00' group by time, status order by time, status desc"
            cursor.execute(query)
            rows = cursor.fetchall()
            for time in listTime:
                count = 0
                for row in rows:
                    if(time == row[0].strftime('%Y-%m-%d %H:%M:%S')):
                        count = 1
                        if(row[1] == 'PASS'):
                            passData = row[2]

                        if(row[1] == 'FAIL'):
                            failData = row[2]
                if count == 1:
                    yieldrate.append(passData/(failData + passData)*100)
                    if passData != 0:
                        passValue.append(passData)
                        passData = 0
                    elif passData == 0:
                        passValue.append(0)
                    if failData != 0:
                        failValue.append(failData)
                        failData = 0
                    elif failData == 0:
                        failValue.append(0)
                else:
                    passValue.append(0)
                    failValue.append(0)
                    yieldrate.append(0)
    finally:
        cursor.close()
    data.append(passValue)
    data.append(failValue)
    data.append(yieldrate)
    return JsonResponse(data, safe=False)


@ api_view(['GET'])
def getDPMO(request):
    data = {}
    try:
        logger = logging.getLogger('django')
        with connection.cursor() as cursor:
            query = "select status, count(id) from tbl_pcb_component_pin where (time between '2022-03-22 07:30:00' and '2022-03-22 19:30:00') group by status"
            cursor.execute(query)
            rows = cursor.fetchall()
        # logger.info(rows)
            for row in rows:
                if(row[0] == 'FAIL'):
                    failPinValue = row[1]
                else:
                    passPinValue = row[1]
        dpmo = (failPinValue/(failPinValue+passPinValue))*1000000
        with connection.cursor() as cursor:
            query = "select status,count(id) from tbl_pcb_result where (time between '2022-03-22 07:30:00' and '2022-03-22 19:30:00') group by status"
            cursor.execute(query)
            rows = cursor.fetchall()
        for row in rows:
            if(row[0] == 'FAIL'):
                failResultValue = row[1]
            else:
                passResultValue = row[1]
        yieldrate = (passResultValue/(failResultValue+passResultValue))*100
        data["pass"] = passResultValue
        data["fail"] = failResultValue
        data["yieldrate"] = yieldrate
        data["dpmo"] = dpmo
    finally:
        cursor.close()
    return JsonResponse(data, safe=False)


@ api_view(['GET'])
def getDefect(request):
    data = []
    try:
        logger = logging.getLogger('django')
        with connection.cursor() as cursor:
            query = "select error_code, count(*) from tbl_pcb_component_pin pin inner join \
                tbl_component_result cresult on pin.component_result_id = cresult.id inner join\
                tbl_pcb_result presult on cresult.pcb_result_id = presult.id where presult.status = 'FAIL'\
                and pin.status ='FAIL' and (presult.time between '2022-03-22 07:30:00' and '2022-03-22 19:30:00')\
                group by error_code"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                data.append({row[0]: row[1]})
    finally:
        cursor.close()
    return JsonResponse(data, safe=False)
