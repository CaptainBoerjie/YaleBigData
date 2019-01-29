#   5 hours ago - منذ 5 ساعات
#   2 hours ago - قبل ساعتين
#   26 January 2019 - 26 يناير 2019 

def translate_date(string):
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
    elif string.split()[2] in ar2eng_month.keys():
        return(' '.join(ar2eng_month.get(i,i) for i in string.split()))
    else:
        return("Nope")

test_string = ' 26 يناير 2019 '
print(translate_date(test_string))