from selenium import webdriver
import time, datetime, re, requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup



#초기 설정 및 기본 데이터
print('프로그램 제작자 : 이현록')
my_id = input('아이디 : ')
my_pw = input('비밀번호 : ')
today = datetime.datetime.now().weekday()

if(today == '1'):
    print('월요일 확인됨')
elif(today == '2'):
    print('화요일 확인됨')
elif(today == '3'):
    print('수요일 확인됨')
elif(today == '4'):
    print('목요일 확인됨')
elif(today == '5'):
    print('금요일 확인됨')
elif(today == '6'):
    print('토요일 확인됨')
elif(today == '7'):
    print('일요일 확인됨')

driver = webdriver.Chrome()
driver.get('https://poc.ebssw.kr/sso/loginView.do?loginType=onlineClass')
action = ActionChains(driver)
print('과정 진행중..(1/5)')
#로그인
time.sleep(1)
driver.find_element_by_css_selector('#j_username').send_keys(my_id)
time.sleep(0.5)
driver.find_element_by_css_selector('#j_password').send_keys(my_pw)
time.sleep(0.5)
driver.find_element_by_css_selector('.img_type').click()
time.sleep(2)

#요일별 들어야 할 과목 분류
print('과정 진행중..(2/5)')
if (today=='1'):
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=359238'
elif (today=='2'):
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=359238'
elif (today=='3'):
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=332097'
elif (today=='4'):
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=357761'
elif (today=='5'):
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=359238'
else:
    print('주말 확인됨. (테스트용)목요일로 이동합니다.')
    daylink = 'https://oc30.ebssw.kr/e913/hmpg/hmpgAlctcrListView.do?menuSn=357761'

#해당 과목으로 접속
driver.get(daylink)
time.sleep(1)

#html 소스코드에서 각 과목 이름, 과목 링크 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
links = soup.findAll('li', {'class':'clearfix'})
class_link_list = []
class_name_list = []


for i in links:
    href = i.find('a')
    class_link_list.append(href.attrs['href'])
    class_name_list.append(i.find('p', {'class':'tit bold'}).string.strip())




video_re = re.compile("javascript:showNewLrnWindow\( '([0-9]*)', '005', '1', 'LCTRE'\);")
#각 과목에 접속하고, 각 과목의 영상 링크들을 리스트에 저장
print('과정 진행중..(3/5)')
count = -1
videolinks = []
for i in class_link_list:
    count += 1
    driver.get('https://oc30.ebssw.kr'+ i)
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    novideo = soup.findAll('li', {'class':'clearfix'})
    
    print(class_name_list[count])
    for j in novideo:
        try:
            title1 = j.find('em', {'class':'border_box end'})
            title = title1.attrs['title']
        except:
            print('', end='')
        if(title == '동영상 강의'):
            print('동영상 발견')
            source1 = j.find('div',{'class':'class_tit fl'})
            source2 = source1.find('a').attrs['href']
            num = video_re.search(source2).group(1)
            videolinks.append('https://oc30.ebssw.kr/mypage/userlrn/userLrnView.do?atnlcNo=481166&stepSn=166799&lctreSn='+num+'&onlineClassYn=Y&returnUrl=')

#가져온 영상들을 하나 하나 시청함
print('과정 진행중..(4/5)')
count = -1
seconds_re = re.compile('([0-9]*):([0-9]*)')
for watching in videolinks:
    count += 1
    driver.get(watching)
    time.sleep(1)
    if(input('스킵하시겠습니까? : ') == 'y'):
        continue

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        divide = soup.find('iframe', {'id':'iframeYoutube'}).attrs['id']
        ebs = 0
        yt = 1
    except:
        ebs = 1
        yt = 0
    
    if(ebs == 1):
        print('EBS 플레이어 영상을 시청합니다.')
        time.sleep(3)
        driver.find_element_by_css_selector('.vjs-big-play-button').click()
        min_seconds = soup.find('span', {'class':'vjs-duration-display'}).text
        minuates = int(seconds_re.search(min_seconds).group(1))
        seconds = int(seconds_re.search(min_seconds).group(2))
        sum_seconds = minuates*60 + seconds
        print('{}번째 영상을 시청합니다.'.format(count+1))
        print('영상 시간 : {0}분 {1}초'.format(minuates, seconds))
        
    if(yt == 1):
        print('유튜브 영상을 시청합니다.')
        time.sleep(3)

        iframe = driver.find_element_by_tag_name('iframe')
        driver.switch_to_frame(iframe)
        driver.find_element_by_css_selector('.ytp-play-button.ytp-button').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        min_seconds = soup.find('span', {'class':'ytp-time-duration'}).text
        minuates = int(seconds_re.search(min_seconds).group(1))
        seconds = int(seconds_re.search(min_seconds).group(2))
        sum_seconds = minuates*60 + seconds
        driver.switch_to.default_content()
        print('{}번째 영상을 시청합니다.'.format(count))
        print('영상 시간 : {0}분 {1}초'.format(minuates, seconds))
        

    time.sleep(sum_seconds)

print('과정 진행중..(5/5)')
print('영상 시청이 모두 끝났습니다.')
