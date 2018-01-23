import requests
from datetime import datetime
from pytz import timezone
import pytz
import TVDataUnixTimeToNormal as tvn
import json

TV_program_data = []

class TVListingGetData:

    def prepare_URL(self,timv,current_time,duration):

        API_url = "http://mobilelistings.tvguide.com/Listingsweb/ws/rest/schedules/80004.null/start/1516615200/duration/" \
                  "1440?ChannelFields=Name%2CFullName%2CNumber%2CSourceId&ScheduleFields=ProgramId%2CEndTime%2CStartTime%" \
                  "2CTitle%2CAiringAttrib%2CCatId&formattype=json&disableChannels=music%2Cppv%2C24hr"

        return API_url


    def get_data(self,timevalue,timezoneforurl,duration):
        try:
            data = requests.get(tvd.prepare_URL(timevalue,timezoneforurl,duration))
        except:
            print ("No Data Recieved")

        tv_data = json.loads(data.text)
        return tv_data

    def get_individual_channel_data(self, prg_data):
        channel_program_data = []
        for data in prg_data:
            for key,value in data.items():
                program_details = {}
                if key == 'Title':
                    title = data[key]
                    #print title
                if key == 'StartTime':
                    start_time = tvn.convert_to_specified_time_zone((data[key]),'US/Pacific')
                    #print start_time
                if key == 'EndTime':
                    end_time = tvn.convert_to_specified_time_zone((data[key]),'US/Pacific')
                    #print end_time
            program_details.update({title:{'start_time':start_time,'end_time':end_time}})
            channel_program_data.append(program_details)
       # print channel_program_data
        return channel_program_data


    def get_channel_data(self,tv_data):
        for tvdata in tv_data:
            programs = {}
            for key,value in tvdata.items():
                #print key , value
                if key == 'Channel':
                    channel = tvdata[key].get('FullName')
                    print channel
                if key == 'ProgramSchedules':
                    valued = tvdata[key]
                    #print  valued
                    prg_data = tvd.get_individual_channel_data(valued)
            programs.update({channel:prg_data})
            #print programs
            TV_program_data.append(programs)
        return TV_program_data




tvd = TVListingGetData()
tvdata = tvd.get_data(80004,tvn.get_current_time(),1440)
tv_program_data = tvd.get_channel_data(tvdata)

for data in tv_program_data:
    print data


