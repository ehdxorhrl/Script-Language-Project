import requests


def get_tw_buoy_beach(service_key, search_time, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getTwBuoyBeach"
    params = {
        'serviceKey': service_key,
        'searchTime': search_time,
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
search_time = "202205011600"
service_key = "J0vWouXboOOX6XyFANTjJQuyZagHIYvxwVy2K6LaSXLyCCPho9deGFO51xcBuhqYDTXAMwMe7uQCY5G5LL1bDw=="
beach_num = 1

water_temp_data = get_tw_buoy_beach(service_key, search_time, beach_num)
print(water_temp_data)
