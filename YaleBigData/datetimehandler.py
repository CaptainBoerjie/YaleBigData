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

    # There is a common problem of commas next to Arabic words which are then not 
    # readable by dateutil.parser or convertBSdate.  These commas must be removed
    # before translation.  Next, some websites provide both Western and Islamic
    # months in the date which result in a double (ex: 23 August August 2013)
    # month which also confuses the dateutil.parser function.

    # First, remove commas
    published = ' '.join(published.split(','))
    # Second, convert any Arabic to English 
    published = convertBSdate(published)
    # Third, remove any duplicate words
    published_split = published.split()
    published = ' '.join(sorted(set(published_split), key = published_split.index))

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
                pass
                #strCleanDate = convertRSSdate(convertBSdate(published))

        except:
            today = datetime.now()
            strCleanDate = today.strftime('%Y-%m-%d %H:%M:%S')
            print("No usable date, using current date.")

        return strCleanDate


def convertBSdate(published,*args):

    eng2ar_day = {'Monday': 'الاثنين','Tuesday': 'الثلاثاء',
        'Wednesday':'الاربعاء', 'Thursday':'الخميس',
        'Friday':'الخميس','Saturday':'السبت',
        'Sunday':'الاحد'}
    ar2eng_day = {'الاثنين':'Monday','الإثنين':'Monday','الثلاثاء':'Tuesday',
        'الاربعاء':'Wednesday','الأربعاء':'Wednesday','الخميس':'Thursday',
        'الخميس':'Friday','السبت':'Saturday',
        'الاحد':'Sunday','الأحد':'Sunday'}

    ar2eng_month = {'يناير':'January','فبراير':'February',
        'مارس':'March','إبريل':'April','أبريل':'April','ابريل':'April',
        'مايو':'May','يونيو':'June',
        'يوليو':'July','أغسطس':'August','اغسطس':'August',
        'سبتمبر':'September','أكتوبر':'October',
        'نوفمبر':'November','ديسمبر':'December',
        ' كانون الثاني':'January','شباط':'February',
        'آذار':'March','نيسان':'April',
        'أيار':'May','ايار':'May','حزيران':'June',
        'تموز':'July','آب':'August',
        'أيلول':'September','تشرين الأول':'October',
        ' تشرين الثاني':'November',' كانون الأول':'December'}

    ar2eng_words = {'منذ':'ago','قبل':'ago','ساعتين':'2 hours',
        'ساعات':'hours','م':''}

    published = ' '.join(ar2eng_day.get(i,i) for i in published.split())
    published = ' '.join(ar2eng_month.get(i,i) for i in published.split())
    published = ' '.join(ar2eng_words.get(i,i) for i in published.split())
    
    return published


if __name__ == '__main__':

    test_list = ['1 يناير 2015', 'قبل ساعتين', 'منذ 5 ساعات', 
        'Fri, 5 Jun 2015 02:14:05 GMT', 'Sat, 26 Jan 2019 12:04:06 +0000',
        'الثلاثاء, 20 آب أغسطس 2013 م ','السبت - 2019-02-02-',
        '2011-08-12T19:49:56+03:00','13 اغسطس 2011','13 ابريل 2013']
        
    for i in test_list:
        print(i, " ----- ",convertRSSdate(i))