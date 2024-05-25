import requests
from tkinter import *
from PIL import Image, ImageTk

def get_ultra_srt_fcst_beach(service_key, base_date, base_time, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
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

def get_vilage_fcst_beach(service_key, base_date, base_time, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getVilageFcstBeach"
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

def get_wh_buoy_beach(service_key, search_time, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getWhBuoyBeach"
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

def get_tide_info_beach(service_key, base_date, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getTideInfoBeach"
    params = {
        'serviceKey': service_key,
        'base_date': base_date,
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

def get_sun_info_beach(service_key, base_date, beach_num, num_of_rows=10, page_no=1, data_type='JSON'):
    url = "http://apis.data.go.kr/1360000/BeachInfoservice/getSunInfoBeach"
    params = {
        'serviceKey': service_key,
        'base_date': base_date,
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

def search_beach_info():
    beach_code = location_entry.get()
    service_key = "J0vWouXboOOX6XyFANTjJQuyZagHIYvxwVy2K6LaSXLyCCPho9deGFO51xcBuhqYDTXAMwMe7uQCY5G5LL1bDw=="
    base_date = "20220622"
    base_time = "1230"
    search_time = "202205011600"

    # Collecting data from all APIs
    forecast_data = get_ultra_srt_fcst_beach(service_key, base_date, base_time, beach_code)
    short_term_forecast_data = get_vilage_fcst_beach(service_key, base_date, base_time, beach_code)
    wave_data = get_wh_buoy_beach(service_key, search_time, beach_code)
    tide_data = get_tide_info_beach(service_key, base_date, beach_code)
    sun_info_data = get_sun_info_beach(service_key, base_date, beach_code)
    water_temp_data = get_tw_buoy_beach(service_key, search_time, beach_code)

    # Update the UI with the fetched data
    nearby_listbox.delete(0, END)
    nearby_listbox.insert(END, f'Ultra Short Forecast: {forecast_data}')
    nearby_listbox.insert(END, f'Short Term Forecast: {short_term_forecast_data}')
    nearby_listbox.insert(END, f'Wave Info: {wave_data}')
    nearby_listbox.insert(END, f'Tide Info: {tide_data}')
    nearby_listbox.insert(END, f'Sun Info: {sun_info_data}')
    nearby_listbox.insert(END, f'Water Temperature: {water_temp_data}')

def open_second_window():
    second_window = Toplevel()
    second_window.title("두번째 창")

    label = Label(second_window, text="여기는 두번째 창입니다.")
    label.pack(pady=20)

    close_button = Button(second_window, text="닫기", command=second_window.destroy)
    close_button.pack(pady=10)

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

    fishing_frame = Frame(bottom_frame, bg="white")
    fishing_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    fishing_label = Label(fishing_frame, text="조석 정보")
    fishing_label.pack(expand=True)

    water_temp_frame = Frame(bottom_frame, bg="white")
    water_temp_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    water_temp_label = Label(water_temp_frame, text="수온 정보")
    water_temp_label.pack(expand=True)

    wave_frame = Frame(bottom_frame, bg="white")
    wave_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    wave_label = Label(wave_frame, text="파고 정보")
    wave_label.pack(expand=True)

    sunrise_sunset_frame = Frame(bottom_frame, bg="white")
    sunrise_sunset_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    sunrise_sunset_label = Label(sunrise_sunset_frame, text="일출일몰 정보")
    sunrise_sunset_label.pack(expand=True)

    # Configure grid weights
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_rowconfigure(1, weight=1)
    bottom_frame.grid_rowconfigure(2, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    # Gmail and Telegram buttons
    contact_frame = Frame(window)
    contact_frame.place(x=10, y=730, width=580, height=50)

    gmail_image = Image.open("지메일.png")
    gmail_image = gmail_image.resize((40, 40), Image.Resampling.LANCZOS)  # Adjust size as needed
    gmail_photo = ImageTk.PhotoImage(gmail_image)

    telegram_image = Image.open("텔레그램.png")
    telegram_image = telegram_image.resize((40, 40), Image.Resampling.LANCZOS)  # Adjust size as needed
    telegram_photo = ImageTk.PhotoImage(telegram_image)

    gmail_button = Button(contact_frame, image=gmail_photo)
    gmail_button.pack(side=LEFT, padx=20, pady=5, expand=True)

    telegram_button = Button(contact_frame, image=telegram_photo)
    telegram_button.pack(side=RIGHT, padx=20, pady=5, expand=True)

    gmail_button.image = gmail_photo
    telegram_button.image = telegram_photo

    window.mainloop()

MainGUI()
