import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang.parser import global_idmap
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from typing import Any
import time
import TTC_times_API

Window.clearcolor = (0,0.6,1,1)

def picture(input: Any)-> str:
    """
    searchs in the directory for picture with the name input
    """
    if input in ['clear','mostly_clear']:
        return 'sun.png'
    elif input in ['partly_cloudy']:
        return 'partly_cloudy.png'
    elif input in ['cloudy', 'mostly_cloudy','fog_light', 'fog']:
        return 'cloudy.png'
    elif input in ['rain_light', 'drizzle']:
        return 'light rainy.png'
    elif input in ['rain']:
        return 'moderately rainy.png'
    elif input in ['heavy_rain']:
        return 'heavy rain.png'
    elif input in ['tstorm']:
        return 'thunder storm.png'
    elif input in ['flurries']:
        return 'flurries.png'
    elif input in ['snow_heavy', 'snow', 'snow_light']:
        return 'snow.png'
    elif input in ['ice_pellets_heavy', 'ice_pellets', 'ice_pellets_light']:
        return 'hail.png'
    else:
        return 'not_found.png'



class LayerOne(Widget):
    image_source = StringProperty('cloudy.png')
    hour_1_pic = StringProperty('sun.png')
    hour_2_pic = StringProperty('sun.png')
    hour_3_pic = StringProperty('sun.png')
    hour_4_pic = StringProperty('sun.png')
    hour_5_pic = StringProperty('sun.png')
    hour_6_pic = StringProperty('sun.png')
    hour_7_pic = StringProperty('sun.png')
    hour_8_pic = StringProperty('sun.png')
    def updateTime(self, *args):
        """
        Updates the text of the labels every second to the correct time
        """
        label_hr_min = self.ids['hr_min']
        label_sec = self.ids['seconds']
        label_date = self.ids['date']
        hr_min = time.strftime('%I:%M')
        label_sec.text = time.strftime('%S')
        if len(time.strftime('%A')) == 9:
            label_date.pos_hint = {'right': 0.306, 'top': 0.89}
        elif len(time.strftime('%A')) == 6:
            label_date.pos_hint = {'right': 0.284, 'top': 0.89}
        else:
            label_date.pos_hint = {'right': 0.292, 'top': 0.89}
        label_date.text = time.strftime('%A, %B %d, %Y')
        if hr_min[0]=='0':
            label_hr_min.text = hr_min[1:]
            label_hr_min.pos_hint = {'right':0.209, 'top': 0.975}
            label_sec.pos_hint = {'right':0.286, 'top': 0.956}      #
        else:
            label_hr_min.text = hr_min
            label_sec.pos_hint = {'right':0.327, 'top': 0.956}      #
            label_hr_min.pos_hint = {'right':0.232, 'top': 0.975}

    def updateMarket(self, *args): # every 15 sec
        dow = self.ids["dow_value"]
        dow_change = self.ids["dow_change"]
        tsx = self.ids["tsx_value"]
        tsx_change = self.ids['tsx_change']
        dollar = self.ids['dollar_value']
        dollar_change = self.ids['dollar_change']
        data = TTC_times_API.retrieve_market_data()
        dow.text = data['Dow']['price']
        dow_change.text = data['Dow']['change'] + '  % ' + data['Dow']['%change']
        tsx.text = data['TSX']['price']
        tsx_change.text = data['TSX']['change'] + '  % ' + data['TSX']['%change']
        dollar.text = data['Dollar']['exchange']
        dollar_change.text = data['Dollar']['change']
        self.red_or_green(dow_change, dow_change.text)
        self.red_or_green(tsx_change, tsx_change.text)
        if dollar_change.text[0] == '-':
            dollar_change.color = (0,1,0,1)
        else:
            dollar_change.color = (1,0,0,1)
        #print("refresh of market data")

    def updateHourly(self):
        data = TTC_times_API.retrieve_hourly()
        print(data)
        self.hour_1_pic = picture(data[0][2])
        self.hour_2_pic = picture(data[1][2])
        self.hour_3_pic = picture(data[2][2])
        self.hour_4_pic = picture(data[3][2])
        self.hour_5_pic = picture(data[4][2])
        self.hour_6_pic = picture(data[5][2])
        self.hour_7_pic = picture(data[6][2])
        self.hour_8_pic = picture(data[7][2])
        hour_1_temp = self.ids['hour_1_temp']
        hour_1_temp.text = str(data[0][1])[:len(str(data[0][1]))-3] + '°' + 'C'
        hour_2_temp = self.ids['hour_2_temp']
        hour_2_temp.text = str(data[1][1])[:len(str(data[1][1]))-3] + '°' + 'C'
        hour_3_temp = self.ids['hour_3_temp']
        hour_3_temp.text = str(data[2][1])[:len(str(data[2][1]))-3] + '°' + 'C'
        hour_4_temp = self.ids['hour_4_temp']
        hour_4_temp.text = str(data[3][1])[:len(str(data[3][1]))-3] + '°' + 'C'
        hour_5_temp = self.ids['hour_5_temp']
        hour_5_temp.text = str(data[4][1])[:len(str(data[4][1]))-3] + '°' + 'C'
        hour_6_temp = self.ids['hour_6_temp']
        hour_6_temp.text = str(data[5][1])[:len(str(data[5][1]))-3] + '°' + 'C'
        hour_7_temp = self.ids['hour_7_temp']
        hour_7_temp.text = str(data[6][1])[:len(str(data[6][1]))-3] + '°' + 'C'
        hour_8_temp = self.ids['hour_8_temp']
        hour_8_temp.text = str(data[7][1])[:len(str(data[7][1]))-3] + '°' + 'C'
        for ind in range(8):
            hour_time = self.ids['hour_{}_time'.format(ind+1)]
            hour_time.text = data[ind][0]

    def red_or_green(self, layout: Any, change: str):
        """
        if value's first character is -, meaning a negative change, then turn
        the text of the color red, otherwise turn green

        """
        if change[0] == '-':
            layout.color = (1,0,0,1)
        else:
            layout.color = (0,1,0,1)


    def updateCurrentWeather(self, *args): # every hour
        data = TTC_times_API.retrieve_current()
        current_temp = self.ids['current_temp']
        input = data['weather_code']["value"]
        current_temp.text = str(data["temp"]["value"])[:2]
        x = picture(input)
        #print('refresh of Current weather: {}'.format(x))
        current_feels = self.ids['current_feels_like']
        feels = str(data['feels_like']['value'])
        current_feels.text = 'Feels like:' + '\n{}'.format(feels[:len(feels)-3])
        self.image_source = x

    def redraw_canvas(self,layout: Any, pic:str):
        layout.canvas.clear()
        with layout.canvas:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size, source=pic)

    def updateTTC(self, *args): #every min
        earliest_504 = self.ids['504_earliest']
        next_504 = self.ids['504_next']
        earliest_29 = self.ids['29_earliest']
        next_29 = self.ids['29_next']
        data_29 = TTC_times_API.retrieve_data_N()['Northbound_Liberty']
        data_504 = TTC_times_API.retrieve_data_E()['Eastbound']
        earliest_29.text = '[b]'+data_29[0][:len(data_29[0])-1]+ '[/b]'
        next_29.text = '[b]'+data_29[1][:len(data_29[1])-1]+ '[/b]'
        earliest_504.text = '[b]'+data_504[0][:len(data_504[0])-1]+ '[/b]'
        next_504.text = '[b]'+data_504[1][:len(data_504[1])-1]+ '[/b]'
        #print('refresh of TTC data')

class Ttc_displayApp(App):
    def build(self):
        layer = LayerOne()
        Clock.schedule_interval(layer.updateTime, 1)
        layer.updateTTC()
        Clock.schedule_interval(layer.updateTTC, 30)
        layer.updateCurrentWeather()
        Clock.schedule_interval(layer.updateCurrentWeather, 720)
        layer.updateCurrentWeather()
        #layer.updateMarket()
        #Clock.schedule_interval(layer.updateMarket, 5)
        layer.updateHourly()
        Clock.schedule_interval(layer.updateHourly, 1800)
        return layer



if __name__== "__main__":
    Ttc_displayApp().run()
