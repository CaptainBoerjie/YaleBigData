# Handle the various datetime groups
# Examples of scraped datetime groups:

#   5 hours ago - منذ 5 ساعات
#   2 hours ago - قبل ساعتين
#   26 January 2019 - 26 يناير 2019 
#   Fri, 5 Jun 2015 02:14:05 GMT
#   Sat, 26 Jan 2019 12:04:06 +0000


import time
from datetime import datetime
from dateutil.parser import parse

def convertRSSdate(published,*args):
    try: 
        cleanDate = parse(published, fuzzy_with_tokens=True, ignoretz=True)
        strCleanDate = cleanDate[0].strftime('%Y-%m-%d %H:%M:%S')
        return strCleanDate
    except:
        try:
            if(published[-5] == '+'):
                cleanDate = parse(published[:25], fuzzy_with_tokens=True, ignoretz=True)
                strCleanDate = cleanDate[0].strftime('%Y-%m-%d %H:%M:%S')
            else:
                today = datetime.now()
                strCleanDate = today.strftime('%Y-%m-%d %H:%M:%S')
                print("No usable date, using current date.")
        except:
            today = datetime.now()
            strCleanDate = today.strftime('%Y-%m-%d %H:%M:%S')
            print("No usable date, using current date.")

        return strCleanDate


def convertBSdate(published,*args):

    eng2ar_day = {'Monday': 'الاثنين','Tuesday': 'الاثنين',
        'Wednesday':'الاثنين', 'Thursday':'الاثنين',
        'Friday':'الاثنين','Saturday':'الاثنين',
        'Sunday':'الاثنين'}
    ar2eng_day = {'الاثنين':'Monday','الاثنين':'Tuesday',
        'الاثنين':'Wednesday','الاثنين':'Thursday',
        'الاثنين':'Friday','الاثنين':'Saturday',
        'الاثنين':'Sunday'}
    # print(dict['Monday'])

    ar2eng_month = {'يناير':'January','فبراير':'February',
        'مارس':'March','إبريل':'April','أبريل':'April',
        'مايو':'May','يونيو':'June',
        'يوليو':'July','أغسطس':'August',
        'سبتمبر':'September','أكتوبر':'October',
        'نوفمبر':'November','ديسمبر':'December',
        ' كانون الثاني':'January','شباط':'February',
        'آذار':'March','نيسان':'April',
        'أيار':'May','حزيران':'June',
        'تموز':'July','آب':'August',
        'أيلول':'September','تشرين الأول':'October',
        ' تشرين الثاني':'November',' كانون الأول':'December'}

    ar2eng_words = {'منذ':'ago','قبل':'ago','ساعتين':'2 hours',
        'ساعات':'hours',}

    if string.split()[0] in ar2eng_words.keys():
        return(' '.join(ar2eng_words.get(i,i) for i in string.split()))
    elif string.split()[1] in ar2eng_month.keys():
        return(' '.join(ar2eng_month.get(i,i) for i in string.split()))