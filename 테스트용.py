import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


# API 호출 함수
def get_ultra_srt_fcst_beach(service_key, base_date, base_time, beach_num, num_of_rows=60, page_no=1, data_type='JSON'):
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


# 두 번째 창 열기 함수
def open_second_window():
    second_window = Toplevel()
    second_window.title("두번째 창")
    second_window.geometry("400x400")

    # 초단기 예보 데이터 해석 및 표시
    forecast_data = {
        'T1H': 'N/A',
        'RN1': 'N/A',
        'SKY': 'N/A',
        'UUU': 'N/A',
        'VVV': 'N/A',
        'REH': 'N/A',
        'PTY': 'N/A',
        'VEC': 'N/A',
        'WSD': 'N/A'
    }
    pty_dict = {
        '0': '없음',
        '1': '비',
        '2': '비/눈',
        '3': '눈',
        '5': '빗방울',
        '6': '빗방울눈날림',
        '7': '눈날림'
    }
    sky_dict = {
        '0': '맑음',
        '1': '맑음',
        '2': '맑음',
        '3': '맑음',
        '4': '맑음',
        '5': '맑음',
        '6': '구름많음',
        '7': '구름많음',
        '8': '구름많음',
        '9': '흐림',
        '10': '흐림'
    }

    try:
        items = weather_data['response']['body']['items']['item']
        for item in items:
            category = item['category']
            if category in forecast_data:
                if category == 'PTY':
                    forecast_data[category] = pty_dict.get(item['fcstValue'], '알 수 없음')
                elif category == 'SKY':
                    forecast_data[category] = sky_dict.get(item['fcstValue'], '알 수 없음')
                else:
                    forecast_data[category] = item['fcstValue']

        forecast_info = (
            f"기온: {forecast_data['T1H']} ℃\n"
            f"1시간 강수량: {forecast_data['RN1']} mm\n"
            f"하늘상태: {forecast_data['SKY']}\n"
            f"동서바람성분: {forecast_data['UUU']} m/s\n"
            f"남북바람성분: {forecast_data['VVV']} m/s\n"
            f"습도: {forecast_data['REH']} %\n"
            f"강수형태: {forecast_data['PTY']}\n"
            f"풍향: {forecast_data['VEC']} deg\n"
            f"풍속: {forecast_data['WSD']} m/s\n"
        )
        weather_label = Label(second_window, text=forecast_info)
        weather_label.pack(pady=20)
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        weather_label = Label(second_window, text="초단기예보 정보를 가져올 수 없습니다.")
        weather_label.pack(pady=20)

    close_button = Button(second_window, text="닫기", command=second_window.destroy)
    close_button.pack(pady=10)


# 데이터 검색 함수
def search_beach_info():
    global weather_data
    beach_code = location_entry.get()
    service_key = "J0vWouXboOOX6XyFANTjJQuyZagHIYvxwVy2K6LaSXLyCCPho9deGFO51xcBuhqYDTXAMwMe7uQCY5G5LL1bDw=="
    base_date = "20240604"
    base_time = "1230"

    # 초단기 예보 데이터 가져오기
    weather_data = get_ultra_srt_fcst_beach(service_key, base_date, base_time, beach_code)

    # 데이터가 잘 불러와졌는지 확인
    print("Weather Data:", weather_data)

    # UI 업데이트
    nearby_listbox.delete(0, END)
    nearby_listbox.insert(END, f'Ultra Short Forecast: {weather_data}')


def MainGUI():
    global location_entry, nearby_listbox

    window = Tk()
    window.geometry("600x800")
    window.title("놀러와요 해수욕장")

    # 위치 입력 및 검색
    location_frame = Frame(window)
    location_frame.place(x=10, y=10, width=580, height=50)

    location_label = Label(location_frame, text="위치 입력")
    location_label.pack(side=LEFT, padx=5)

    location_entry = Entry(location_frame)
    location_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

    search_button = Button(location_frame, text="검색", command=search_beach_info)
    search_button.pack(side=LEFT, padx=5)

    # 근처 해상활동 리스트
    listbox_frame = Frame(window)
    listbox_frame.place(x=10, y=70, width=580, height=100)

    nearby_listbox = Listbox(listbox_frame)
    nearby_listbox.pack(fill=BOTH, expand=True)

    # 지도
    map_frame = Frame(window, bg="white")
    map_frame.place(x=10, y=180, width=580, height=250)

    map_label = Label(map_frame, text="지도", bg="white")
    map_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # 하단 버튼 및 프레임들
    bottom_frame = Frame(window)
    bottom_frame.place(x=10, y=440, width=580, height=280)

    weather_button = Button(bottom_frame, text="날씨 예보", command=open_second_window)
    weather_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    image_frame = Frame(bottom_frame, bg="white")
    image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    image_label = Label(image_frame, text="이미지")
    image_label.pack(expand=True)

    # Configure grid weights
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    window.mainloop()


MainGUI()
