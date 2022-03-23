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
    yieldRate = []
    data = []
    logger = logging.getLogger('django')
    data = (pd.DataFrame(columns=['NULL'],
                             index=pd.date_range('2022-03-22T07:30:00Z', '2022-03-22T19:30:00Z',
                                                 freq='1H')).to_json())
    logger.info(data)
    listTime = (pd.DataFrame(columns=['NULL'],
                             index=pd.date_range('2022-03-22T07:30:00Z', '2022-03-22T19:30:00Z',
                                                 freq='1H'))
                .between_time('07:30', '19:30')
                .index.strftime('%Y-%m-%d %H:%M:%S')
                .tolist()
                )
    for index, time in enumerate(listTime):
        try:
            if index < len(listTime)-1:
                with connection.cursor() as cursor:
                    query = "select status, count(id) from tbl_pcb_result where (time between '{}' and '{}') group by status, time".format(
                        time, listTime[index+1])
                    cursor.execute(query)
                    rows = cursor.fetchall()
                if(len(rows) > 0):
                    for row in rows:
                        if(row[0] == 'FAIL'):
                            failValue.append(row[1])
                        if(row[0] == 'PASS'):
                            passValue.append(row[1])
                    if(len(rows) == 1):
                        yieldRate.append(100)
                        failValue.append(0)
                    else:
                        yieldRate.append(rows[1][1]/(rows[0][1] + rows[1][1]) * 100)
                else:
                    passValue.append(0)
                    failValue.append(0)
                    yieldRate.append(0)
        finally:
            cursor.close()

    data.append(passValue)
    data.append(failValue)
    data.append(yieldRate)
    return JsonResponse(data, safe=False)
