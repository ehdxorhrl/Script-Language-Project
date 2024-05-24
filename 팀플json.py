import requests


def get_beach_weather_forecast(service_key, base_date, base_time, beach_num, num_of_rows=10, page_no=1,
                               data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getUltraSrtFcstBeach"
    params = {
        'serviceKey': service_key,
        'base_date': base_date,
        'base_time': base_time,
        'beach_num': beach_num,
        'numOfRows': num_of_rows,
        'pageNo': page_no,
        'dataType': data_type
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        if data_type == 'JSON':
            return response.json()
        elif data_type == 'XML':
            return response.text
    else:
        return f"Error: {response.status_code}"


# Example usage
service_key = "J0vWouXboOOX6XyFANTjJQuyZagHIYvxwVy2K6LaSXLyCCPho9deGFO51xcBuhqYDTXAMwMe7uQCY5G5LL1bDw=="
base_date = "20240524"
base_time = "1230"
beach_num = 1

forecast_data = get_beach_weather_forecast(service_key, base_date, base_time, beach_num)
print(forecast_data)
