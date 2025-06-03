import pandas as pd
from django.http import HttpResponse

def generate_excel_template(columns):
    df = pd.DataFrame(columns=columns)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=template.xlsx'
    df.to_excel(response, index=False)
    return response

def read_excel_and_return_dataframe(file):
    try:
        return pd.read_excel(file)
    except Exception as e:
        return None
