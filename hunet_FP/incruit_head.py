# %%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, math, os, random, urllib, urllib.request, getpass, re, datetime

# %%
Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
driver = webdriver.Chrome(service=Services)
today = datetime.datetime.today()

name = 'incruit_head'  # 저장할 폴더명
time_local = time.localtime()
time_name = ('%d.%d.%d_' % (time_local.tm_year,
             time_local.tm_mon, time_local.tm_mday))

username = getpass.getuser()    # getpass 모듈로 username 불러오기
username = 'yzz07'
save_location = 'C:\\Users\\' + username + '\\Desktop'
save_name = save_location + '\\' + name

if os.path.exists(save_name) == False:
    os.mkdir(save_name)
    os.chdir(save_name)
else:
    os.chdir(save_name)

dic_category = {100: '경영·인사·총무·사무', 101: '재무·회계·경리', 102: '마케팅·광고·홍보·조사', 103: '교육·교사·강사·교직원', 104: '디자인', 106: '고객상담·TM ', 107: '건설·건축·토목·환경', 110: '유통·물류·운송·운전', 120: '전자·기계·기술·화학·연구개발', 210: '금융·보험·증권', 190: '의료·간호·보건·복지', 130: '전문직·법률·인문사회·임원', 140: '생산·정비·기능·노무', 170: '서비스·여행·숙박·음식·미용·보안', 150: '무역·영업·판매·매장관리', 160: '인터넷·IT·통신·모바일·게임'}

data_url = []
data_main = []  # 대분류
data_middle = []  # 중분류

for key, value in dic_category.items():
    page = 1
    try :
        while True :
            url = 'https://chief.incruit.com/jobdb_list/searchjob.asp?occ1=%s&page=%s'%(key, page)
            driver.get(url)
            time.sleep(random.uniform(1, 6)) 

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', 'cPrdlists_wrap cPrdlists_wrap_respon')
            contents = content.find_all('li', 'c_col')

            for i in contents : 
                data_url_ = i.find('div', 'cell_mid').find('div', 'cl_top').find('a')['href']
                data_url.append(data_url_)

                data_main_ = value
                data_middle_ = i.find('div', 'cell_mid').find('div', 'cl_btm').text
                data_main.append(data_main_)
                data_middle.append(data_middle_)

            page += 1
    except :
        print('%s' %value)


# %%
df = pd.DataFrame()
df['data_url'] = pd.Series(data_url)
df['data_main'] = pd.Series(data_main)
df['data_middle'] = pd.Series(data_middle)

# %%
fc_name = (time_name + name + '.csv')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")

# %%
data_type = []  # 고용형태
data_career = []  # 경력
data_education = []  # 학력
data_region = []  # 지역
data_title = []  # 제목
data_company = []  # 기업 이름
data_deadline = []  # 마감일
data_notice = []  # 공고일
data_size = []
data_field = []

for i in data_url :
    url = i
    Services = Service("C:/Users/yzz07/Desktop/PROGRAMMING/chromedriver.exe")
    driver = webdriver.Chrome(service=Services)
    driver.get(url)
    time.sleep(random.uniform(1, 3)) 

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find('div', 'section_view_layout')

    data_type_ = content.find_all('em', class_="bb")[-3].get_text()
    data_career_ = content.find_all('em', class_="bb")[-2].get_text()
    data_education_ = content.find_all('em', class_="bb")[-1].get_text()
    data_region_ = content.find_all('em')[-5].get_text()
    data_title_ = content.find('div', 'job_info_detail').find('h2').find("strong").get_text()
    data_company_ = content.find('div', 'job_info_detail').find('h3').find("a").get_text()

    try :
        data_deadline_ = soup.find_all('div', 'day')[1].find('em').text
    except :
        data_deadline_ = '채용시'

    try :
        data_notice_ = soup.find_all('div', 'day')[0].text
    except :
        data_notice_ = '-'

    data_size_ = content.find('div', 'job_info_detail').find_all('dd')[-1].get_text()
    data_field_ = content.find('div', 'job_info_detail').find_all('dd')[-2].get_text()

    data_type.append(data_type_)
    data_career.append(data_career_)
    data_education.append(data_education_)
    data_region.append(data_region_)
    data_title.append(data_title_)
    data_company.append(data_company_)
    data_deadline.append(data_deadline_)
    data_notice.append(data_notice_)
    data_size.append(data_size_)
    driver.close()


# %%
df['data_type'] = pd.Series(data_type)
df['data_career'] = pd.Series(data_career)
df['data_education'] = pd.Series(data_education)
df['data_region'] = pd.Series(data_region)
df['data_title'] = pd.Series(data_title)
df['data_company'] = pd.Series(data_company)
df['data_deadline'] = pd.Series(data_deadline)
df['data_notice'] = pd.Series(data_notice)
df['data_size'] = pd.Series(data_size)
# %%
fc_name = (time_name + name + '2.csv')
df.to_csv(fc_name, index=False, encoding="utf-8-sig")
# %%
