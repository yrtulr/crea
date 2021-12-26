from flask import Flask, render_template  ## flask 라이브러리에서 Flask import
import createsoup

app = Flask(__name__)
soup = createsoup.create_soup('https://weather.naver.com/today/15800250')
dust = createsoup.create_dust('https://weather.naver.com/air/15800250')

@app.before_request
def weather_cast():
    global cast
    
    try:
        cast = soup.find("span", attrs={"class":"temperature down"}).get_text()
    except:
        a = 1
    try:
        cast = soup.find("span", attrs={"class":"temperature up"}).get_text()
    except:
        a = 1

    crr_temp = soup.find('strong', attrs={'class':'current'}).get_text().replace('현재 온도','').replace('°','')
    
    weather_slash = soup.find('span', attrs={'class':'weather before_slash'}).get_text()

    week_day = soup.find_all('strong', attrs={"class":"day"})
    week_day_txt = []
    for i in week_day:
        week_day_txt.append(i.get_text())
    
    week_date = soup.find_all('span', attrs={"class":"date"})
    week_date_txt = []
    for i in week_date:
        week_date_txt.append(i.get_text())
    for i in range(1,8):
        del week_date_txt[10]

    week_lowest = soup.find_all('span', attrs={'class':'lowest'})
    week_lowest_txt = []
    week_lowest_txt.append(soup.find('span', attrs={'class':'data lowest'}).get_text().replace('평균기온',''))
    for i in week_lowest:
        week_lowest_txt.append(i.get_text().replace('최저기온',''))
    del week_lowest_txt[0]
    del week_lowest_txt[0]

    week_highest = soup.find_all('span', attrs={'class':'highest'})
    week_highest_txt = []
    week_highest_txt.append(soup.find('span', attrs={'class':'data highest'}).get_text().replace('평균기온',''))
    for i in week_highest:
        week_highest_txt.append(i.get_text().replace('최고기온',''))
    del week_highest_txt[0]
    del week_highest_txt[0]

    week_rainfall = soup.find_all('span', attrs={'class':'rainfall'})
    week_rainfall_txt = []
    for i in week_rainfall:
        week_rainfall_txt.append(i.get_text().replace('강수확률',''))
    del week_rainfall_txt[0]
    del week_rainfall_txt[0]

    day_time = soup.find_all('span', attrs={'class':'time'})
    day_time_txt = []
    for i in day_time:
        day_time_txt.append(i.get_text())

    day_blind_txt = []
    day_blind_hour = soup.find_all('span', attrs={'class':'blind'})
    for i in day_blind_hour:
        day_blind_txt.append(i.get_text().replace('\n',''))
   
    matching = [s for s in day_blind_txt if "도" in s]
    day_temp_per_hour_txt = matching[5:80]
    for i in range(0,50):
        k = day_temp_per_hour_txt[i]
        k = k.replace("도",'')
        day_temp_per_hour_txt[i] = k

    pm10 = dust.find('span', attrs={'class':'value _cnPm10Value'}).get_text()
    pm10_grade = dust.find('span', attrs={'class':'grade _cnPm10Grade'}).get_text()
    pm2dot5 = dust.find('span', attrs={'class':'value _cnPm25Value'}).get_text()
    pm2dot5_grade = dust.find('span', attrs={'class':'grade _cnPm25Grade'}).get_text()

    if pm10_grade == '좋음':
        pm10_color_r = 204
        pm10_color_g = 236
        pm10_color_b = 255
        pm10_text_color_r = 50
        pm10_text_color_g = 161
        pm10_text_color_b = 255
    elif pm10_grade == '보통':
        pm10_color_r = 150
        pm10_color_g = 255
        pm10_color_b = 178
        pm10_text_color_r = 0
        pm10_text_color_g = 199
        pm10_text_color_b = 60
    elif pm10_grade == '나쁨':
        pm10_color_r = 255
        pm10_color_g = 201
        pm10_color_b = 166
        pm10_text_color_r = 253
        pm10_text_color_g = 155
        pm10_text_color_b = 90
    else:
        pm10_color_r = 252
        pm10_color_g = 164
        pm10_color_b = 164
        pm10_text_color_r = 255
        pm10_text_color_g = 89
        pm10_text_color_b = 89
    
    if pm2dot5_grade == '좋음':
        pm25_color_r = 204
        pm25_color_g = 236
        pm25_color_b = 255
        pm25_text_color_r = 50
        pm25_text_color_g = 161
        pm25_text_color_b = 255
    elif pm2dot5_grade == '보통':
        pm25_color_r = 150
        pm25_color_g = 255
        pm25_color_b = 178
        pm25_text_color_r = 0
        pm25_text_color_g = 199
        pm25_text_color_b = 60
    elif pm2dot5_grade == '나쁨':
        pm25_color_r = 255
        pm25_color_g = 201
        pm25_color_b = 166
        pm25_text_color_r = 253
        pm25_text_color_g = 155
        pm25_text_color_b = 90
    else:
        pm25_color_r = 252
        pm25_color_g = 164
        pm25_color_b = 164
        pm25_text_color_r = 255
        pm25_text_color_g = 89
        pm25_text_color_b = 89

    return render_template('index.html', cast = cast, crr_temp = crr_temp, weather_slash=weather_slash,
    week_day_txt = week_day_txt, week_date_txt= week_date_txt, week_lowest_txt = week_lowest_txt, 
    week_highest_txt = week_highest_txt , week_rainfall_txt = week_rainfall_txt, 
    day_time_txt = day_time_txt, day_temp_per_hour_txt = day_temp_per_hour_txt, 
    pm10 = pm10, pm10_grade = pm10_grade, pm2dot5 = pm2dot5, 
    pm2dot5_grade = pm2dot5_grade, pm10_color_r = pm10_color_r, 
    pm10_color_b=pm10_color_b, pm10_color_g= pm10_color_g, 
    pm10_text_color_r = pm10_text_color_r, pm10_text_color_g = pm10_text_color_g, 
    pm10_text_color_b = pm10_text_color_b, pm25_color_r = pm25_color_r, pm25_color_g = pm25_color_g,
    pm25_color_b = pm25_color_b, pm25_text_color_r = pm25_text_color_r,
    pm25_text_color_g = pm25_text_color_g, pm25_text_color_b = pm25_text_color_b)

if __name__ == "__main__":
    app.run()