# Test the get() function to access text within a tag

from bs4 import BeautifulSoup

code = """
<div id="article_wrapper" class="stuff_container">
<h2 id="article_title">محمد لمين يناشد المحسنين مساعدته لاستكمال العلاج</h2>
<div id="article_info">
<a href="/press/category/27/مجتمع-1/" id="article_category">مجتمع</a>
<div class="subinfo">10 فبراير 2015 (<time class="relative_time" datetime="2015-2-10T23:00:0Z+1"></time>) - <b>البليدة: ب. رحيم</b></div>
</div>
<div id="article_img">
<img src="">
</div>
"""
soup = BeautifulSoup(code, 'lxml')

print(soup.find('div').get('class'))