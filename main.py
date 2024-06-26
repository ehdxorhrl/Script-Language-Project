from tkinter import *
from tkinter import messagebox
import requests
import io
import os
from PIL import Image, ImageTk
import googlemaps
import pandas as pd
from geopy.distance import geodesic
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import telepot
from telepot.loop import MessageLoop
import requests
import sys
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import spam
sys.path.append(r'C:\Python\스크립트 언어\Script-Language-Project')

# Google API 키 설정
Google_API_Key = 'AIzaSyB3wJJMRzVwJBGLJXkfLOEHXWHH2nV6lXw'

# Google Maps 클라이언트 초기화
gmaps = googlemaps.Client(key=Google_API_Key)
zoom = 13

# 봇의 API 토큰
bot = telepot.Bot('7314248046:AAFoNlzyPuPH07inksK3kD6SI8D569NMXwg')

def open_input_gmail():
    global beach_name

    subject = "놀러와요 해수욕장에서 요청한 " + beach_name + " 정보입니다."
    to_email = mail_entry.get()
    password = "ttxwchmnhlbxyyzm"
    from_email = "ehdxorhrl@gmail.com"
    body = search_beach_info()

    img_path = "images/" + beach_name + "_1.jpg"
    success = send_email_gmail(subject, body, to_email, from_email, password, img_path)

    if success:
        messagebox.showinfo("이메일 전송 성공", "이메일을 성공적으로 보냈습니다.")
    else:
        messagebox.showerror("이메일 전송 실패", "이메일을 보내는 동안 문제가 발생했습니다. 다시 시도해주세요.")

def send_email_gmail(subject, body, to_email, from_email, password, attachment_path):
    # SMTP 서버와 포트 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 메시지 구성
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = 'image.jpg'

    # 이미지 첨부
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)

    try:
        # SMTP 서버에 연결
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS 보안 시작
        server.login(from_email, password)  # 로그인
        # 이메일 보내기
        server.sendmail(from_email, to_email, msg.as_string())
        print("이메일을 성공적으로 보냈습니다.")
        return True
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
        return False
    finally:
        server.quit()  # 서버 연결 종료

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
    global weather_data, service_key, base_date
    service_key = "J0vWouXboOOX6XyFANTjJQuyZagHIYvxwVy2K6LaSXLyCCPho9deGFO51xcBuhqYDTXAMwMe7uQCY5G5LL1bDw=="
    base_date, base_time, search_time = spam.get_datetime()

    print(f"Base Date: {base_date}")
    print(f"Base Time: {base_time}")
    print(f"Search Time: {search_time}")

    # Collecting data from all APIs
    weather_data = get_ultra_srt_fcst_beach(service_key, base_date, base_time, beach_code)
    short_term_forecast_data = get_vilage_fcst_beach(service_key, base_date, base_time, beach_code)
    wave_data = get_wh_buoy_beach(service_key, search_time, beach_code)
    tide_data = get_tide_info_beach(service_key, base_date, beach_code)
    sun_data = get_sun_info_beach(service_key, base_date, beach_code)
    water_temp_data = get_tw_buoy_beach(service_key, search_time, beach_code)

    info_message = ""

    # 초단기 예보 정보
    try:
        items = weather_data['response']['body']['items']['item']
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
            '1': '맑음',
            '3': '구름많음',
            '4': '흐림'
        }

        for item in items:
            category = item['category']
            if category in forecast_data:
                if category == 'PTY':
                    forecast_data[category] = pty_dict.get(item['fcstValue'], '알 수 없음')
                elif category == 'SKY':
                    forecast_data[category] = sky_dict.get(item['fcstValue'], '알 수 없음')
                else:
                    forecast_data[category] = item['fcstValue']

        info_message += (
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
    except (KeyError, IndexError):
        info_message += "초단기 예보 정보를 가져올 수 없습니다.\n"

    # 파고 정보 업데이트
    try:
        wh_value = wave_data['response']['body']['items']['item'][0]['wh']
        wave_label.config(text=f"파고 정보 : {wh_value} M")
        info_message += f"파고 정보: {wh_value} M\n"
    except (KeyError, IndexError) as e:
        wave_label.config(text="파고 정보를 가져올 수 없습니다.")
        info_message += "파고 정보를 가져올 수 없습니다.\n"

    # 수온 정보 업데이트
    try:
        tw_value = water_temp_data['response']['body']['items']['item'][0]['tw']
        water_temp_label.config(text=f"수온 정보 : {tw_value} °C")
        info_message += f"수온 정보: {tw_value} °C\n"
    except (KeyError, IndexError) as e:
        water_temp_label.config(text="수온 정보를 가져올 수 없습니다.")
        info_message += "수온 정보를 가져올 수 없습니다.\n"

    # 조석 정보 업데이트
    try:
        tide_items = tide_data['response']['body']['items']['item']
        tide_info = ""
        for item in tide_items:
            if item['tiType'].startswith("ET"):
                tiType = "저(간조)"
            elif item['tiType'].startswith("FT"):
                tiType = "고(만조)"
            else:
                tiType = "알 수 없음"
            tide_info += f"{item['tiStnld']} - {item['tiTime']} - {tiType} - {item['tilevel']} cm\n"
        tide_label.config(text=f"조석 정보\n{tide_info}")
        info_message += f"조석 정보:\n{tide_info}\n"
    except (KeyError, IndexError) as e:
        tide_label.config(text="조석 정보를 가져올 수 없습니다.")
        info_message += "조석 정보를 가져올 수 없습니다.\n"

    # 일출일몰 정보 업데이트
    try:
        sun_info = sun_data['response']['body']['items']['item'][0]
        sunrise = sun_info['sunrise']
        sunset = sun_info['sunset']
        sunrise_sunset_label.config(text=f"일출 시간 : {sunrise}\n일몰 시간 : {sunset}")
        info_message += f"일출 시간: {sunrise}\n일몰 시간: {sunset}\n"
    except (KeyError, IndexError) as e:
        sunrise_sunset_label.config(text="일출일몰 정보를 가져올 수 없습니다.")
        info_message += "일출일몰 정보를 가져올 수 없습니다.\n"

    return info_message

# 해수욕장과의 거리를 계산하여 정렬하는 함수
def find_nearest_beaches(df, user_location):
    df['distance'] = df.apply(
        lambda row: geodesic(user_location, (row['위도'], row['경도'])).km, axis=1
    )
    sorted_df = df.sort_values(by='distance').reset_index(drop=True)
    return sorted_df
def get_lat_lng(address):
    geocode_result = gmaps.geocode(address)
    if not geocode_result:
        print(f"주소를 찾을 수 없습니다: {address}")
        return None

    location = geocode_result[0]['geometry']['location']
    return (location['lat'], location['lng'])

def load_beach_data(file_path):
    df = pd.read_excel(file_path)
    return df

def update_listbox(location):
    # Listbox 업데이트 함수
    nearby_listbox.delete(0, END)
    for i, row in location.iterrows():
        nearby_listbox.insert(END, f"{i + 1}. {row['해수욕장']} - 거리: {row['distance']:.2f} km")

def search_location():
    # 위치 검색 버튼 클릭 시 실행되는 함수
    location = get_lat_lng(location_entry.get())
    print(location)
    nearest_beaches = find_nearest_beaches(beach_data, location)
    # 상위 20개의 해수욕장만 선택합니다.
    top_20_beaches = nearest_beaches.head(20)
    update_listbox(top_20_beaches)

def on_listbox_select(event):
    global beach_code, beach_name, search_term, image_path
    # Listbox 항목 선택 시 실행되는 함수
    selected_index = nearby_listbox.curselection()
    if not selected_index:
        return

    selected_beach = nearby_listbox.get(selected_index)
    beach_name = selected_beach.split(".")[1].split(" -")[0].strip()
    selected_row = beach_data[beach_data['해수욕장'] == beach_name].iloc[0]
    beach_location = (selected_row['위도'], selected_row['경도'])
    get_map(beach_location)

    beach_code = selected_row.name + 1

    search_beach_info()

    if image_path:
        os.remove(image_path)
        image_path = ""

    search_term = beach_name
    download_image(search_term, num_images=1)
    image_path = f'images/{search_term}_1.jpg'

    display_image(image_path, image_frame, 250, 90)


def get_map(location):
    # Google Maps Static API URL 생성
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={location[0]},{location[1]}&zoom={zoom}&size=600x300&maptype=roadmap&markers=color:red%7Clabel:S%7C{location[0]},{location[1]}&key={Google_API_Key}"

    # 지도 이미지 요청
    response = requests.get(map_url)
    image_data = response.content

    # 이미지를 PIL 형식으로 변환
    image = Image.open(io.BytesIO(image_data))
    map_image = ImageTk.PhotoImage(image)

    # 이미지 업데이트
    map_label.config(image=map_image)
    map_label.image = map_image

def open_weather_inform():
    second_window = Toplevel()
    second_window.title("날씨 예보")
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


def open_graph():
    global base_date, base_time
    graph_window = Toplevel()
    graph_window.title("Graph")
    graph_window.iconbitmap("icon.ico")
    graph_window.geometry("800x600")  # 창 크기 조정

    times = []
    temperatures = []

    try:
        # 전날의 날짜 계산
        yesterday_date = (datetime.strptime(base_date, "%Y%m%d") - timedelta(days=1)).strftime("%Y%m%d")

        # 현재 시간의 시간 단위를 구함 (00분으로 설정)
        current_time = datetime.now().replace(minute=0, second=0, microsecond=0)

        # 24시간 동안의 데이터를 수집
        for hour in range(24):
            next_hour = current_time + timedelta(hours=hour)
            base_time = next_hour.strftime("%H00")
            print(base_time)
            weather_data = get_ultra_srt_fcst_beach(service_key, yesterday_date, base_time, beach_code)
            items = weather_data['response']['body']['items']['item']
            for item in items:
                if item['category'] == 'T1H':
                    forecast_time = item['fcstTime']
                    temperature = float(item['fcstValue'])
                    times.append(yesterday_date + forecast_time)
                    temperatures.append(temperature)

        # times를 datetime 형식으로 변환
        times = [datetime.strptime(t, "%Y%m%d%H%M") for t in times]

    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return

    # 그래프 그리기
    fig, ax = plt.subplots()
    ax.bar(times, temperatures, width=0.03)
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (℃)')
    ax.set_title('24-Hour Temperature Forecast')
    plt.xticks(rotation=45)  # x축 레이블 각도 조정
    plt.tight_layout()  # 레이아웃 자동 조정

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    close_button = Button(graph_window, text="닫기", command=graph_window.destroy)
    close_button.pack(pady=10)




def download_image(search_term, num_images=1):
    url = f"https://www.google.com/search?q={search_term}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_tags = soup.find_all("img", limit=num_images + 1)
    image_urls = [img['src'] for img in image_tags[1:num_images + 1]]

    os.makedirs('images', exist_ok=True)
    image_paths = []

    for i, img_url in enumerate(image_urls):
        img_data = requests.get(img_url).content
        img_path = f'images/{search_term}_{i + 1}.jpg'
        with open(img_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image {i + 1} downloaded")
        image_paths.append(img_path)

    return image_paths



def display_image(image_path, parent_frame, width, height):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    img = Image.open(image_path)
    im = ImageTk.PhotoImage(img)

    image_label = Label(parent_frame, image=im)
    image_label.image = im
    image_label.pack()


# 들어오는 텔레그램 메시지를 처리하는 함수
def handle(msg):
    global beach_code
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'location':
        latitude = msg['location']['latitude']
        longitude = msg['location']['longitude']
        user_location = (latitude, longitude)
        nearest_beaches = find_nearest_beaches(beach_data, user_location)
        top_5_beaches = nearest_beaches.head(5)
        response_message = "근처의 해수욕장 목록:\n"
        for i, row in top_5_beaches.iterrows():
            response_message += f"{i + 1}. {row['해수욕장']} - 거리: {row['distance']:.2f} km\n"
        response_message += "\n원하는 해수욕장의 이름을 입력해 주세요."
        bot.sendMessage(chat_id, response_message)

    elif content_type == 'text':
        beach_name = msg['text']
        if beach_name in beach_data['해수욕장'].values:
            selected_row = beach_data[beach_data['해수욕장'] == beach_name].iloc[0]
            beach_code = selected_row.name + 1
            beach_info = search_beach_info()
            if beach_info:
                bot.sendMessage(chat_id, beach_info)
                image_paths = download_image(beach_name)
                if image_paths:
                    for img_path in image_paths:
                        with open(img_path, 'rb') as photo:
                            bot.sendPhoto(chat_id, photo)
            else:
                bot.sendMessage(chat_id, "선택한 해수욕장에 대한 정보를 찾을 수 없습니다.")
        else:
            # 입력한 텍스트가 해수욕장 이름이 아닌 경우 주소로 간주하여 위치를 찾음
            location = get_lat_lng(beach_name)
            if location:
                nearest_beaches = find_nearest_beaches(beach_data, location)
                top_5_beaches = nearest_beaches.head(5)
                response_message = "근처의 해수욕장 목록:\n"
                for i, row in top_5_beaches.iterrows():
                    response_message += f"{i + 1}. {row['해수욕장']} - 거리: {row['distance']:.2f} km\n"
                response_message += "\n원하는 해수욕장의 이름을 입력해 주세요."
                bot.sendMessage(chat_id, response_message)
            else:
                bot.sendMessage(chat_id, "입력한 해수욕장을 찾을 수 없습니다. 다시 입력해 주세요.")
# 메시지를 수신 대기
# MessageLoop(bot, handle).run_as_thread()

def run_bot():
    MessageLoop(bot, handle).run_forever()
    print('Listening ...')

def MainGUI():
    global location_entry, nearby_listbox, wave_label, water_temp_label, tide_label, sunrise_sunset_label, map_label, image_frame, search_term, image_path, mail_entry
    window = Tk()
    window.geometry("600x800")
    window.title("놀러와요 해수욕장")
    window.iconbitmap("icon.ico")
    window.resizable(False, False)

    # 캔버스를 사용하여 배경 이미지 설정
    canvas = Canvas(window, width=600, height=800)
    canvas.pack(fill="both", expand=True)

    # 배경 이미지 로드dD
    bg_image = PhotoImage(file="background.png")
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    # 위치 입력 및 검색
    location_frame = Frame(window)
    location_frame.place(x=10, y=10, width=580, height=50)

    location_label = Label(location_frame, text="위치 입력")
    location_label.pack(side=LEFT, padx=5)

    location_entry = Entry(location_frame)
    location_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

    search_button = Button(location_frame, text="검색", command=search_location)
    search_button.pack(side=LEFT, padx=5)

    # 근처 해상활동 리스트
    listbox_frame = Frame(window)
    listbox_frame.place(x=10, y=70, width=580, height=100)

    listbox_scrollbar = Scrollbar(listbox_frame)
    listbox_scrollbar.pack(side="right", fill="y")

    nearby_listbox = Listbox(listbox_frame, selectmode="extended", height=10, yscrollcommand=listbox_scrollbar.set)
    nearby_listbox.pack(fill=BOTH, expand=True)
    nearby_listbox.bind('<<ListboxSelect>>', on_listbox_select)

    #지도
    map_frame = Frame(window, bg="white")
    map_frame.place(x=10, y=180, width=580, height=250)

    map_label = Label(map_frame, bg="white")
    map_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # 하단 버튼 및 프레임들
    bottom_frame = Frame(window)
    bottom_frame.place(x=10, y=440, width=580, height=280)

    weather_button = Button(bottom_frame, text="날씨 예보", command=open_weather_inform)
    weather_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    image_frame = Frame(bottom_frame, bg="white", width=200, height=90)
    image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    tide_frame = Frame(bottom_frame, bg="white")
    tide_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    tide_label = Label(tide_frame, text="조석 정보")
    tide_label.pack(expand=True)

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

    graph_image = Image.open("그래프.png")
    graph_image = graph_image.resize((40, 40), Image.Resampling.LANCZOS)  # Adjust size as needed
    graph_photo = ImageTk.PhotoImage(graph_image)

    mail_entry = Entry(contact_frame)
    mail_entry.pack(side=LEFT, padx=20, fill=X, expand=True)

    gmail_button = Button(contact_frame, image=gmail_photo, command=open_input_gmail, bg="green")
    gmail_button.pack(side=LEFT, padx=20, pady=5, expand=True)

    graph_button = Button(contact_frame, image=graph_photo, command=open_graph, bg="green")
    graph_button.pack(side=RIGHT, padx=20, pady=5, expand=True)

    gmail_button.image = gmail_photo
    graph_button.image = graph_photo

    window.mainloop()

global search_term, image_path
search_term = None
image_path = ""


excel_file_path = "기상청48_전국해수욕장_날씨_조회서비스_오픈API활용가이드_최종/기상청48_전국해수욕장_날씨_조회서비스_위경도.xlsx"
beach_data = load_beach_data(excel_file_path)
#print(spam.strlen("hello world"))
threading.Thread(target=run_bot).start()
MainGUI()

# 앱 비밀번호: ttxw chmn hlbx yyzm