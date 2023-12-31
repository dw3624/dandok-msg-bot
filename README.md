# NAVER 단독 뉴스 알림 (telegram)
이 프로그램은 네이버 검색 API를 사용해 지정된 키워드의 단독 뉴스를 검색하고, 새 단독 뉴스를 찾으면 텔레그램으로 알림을 보내는 기능을 제공합니다.

## 기능
- 지정된 검색어로 네이버 검색 API를 호출해 단독 뉴스를 검색합니다.
- 이전에 발견된 단독 뉴스와 비교해 신규 단독 뉴스를 필터링합니다.
- 텔레그램 봇을 사용해 신규 단독 뉴스를 알림으로 전송합니다.

## 요구 사항
- Python 3.9 이상
- `aiohttp`
- `python-telegram-bot`

## 설치 및 설정
### 로컬 설치
1. 저장소를 클론하거나 압축 파일을 다운로드하여 로컬 환경에 프로젝트를 복사합니다.

2. 프로젝트 디렉토리로 이동한 다음, 필요한 종속성을 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

3. 텔레그램 봇 생성과 설정:
- 텔레그램에서 @BotFather를 검색해 봇 생성을 시작합니다.
- 봇 이름을 지정하고 사용자 이름을 받아 새로운 봇을 생성합니다.
- 생성된 봇의 토큰을 기록합니다.

4. 환경 변수 설정:
- `.env` 파일을 생성하고 아래와 같이 필요한 환경 변수를 설정합니다.

  ```
  BOT_TOKEN=봇_토큰
  CHAT_ID=채팅_ID
  NAVER_CLIENT_ID=네이버_클라이언트_ID
  NAVER_CLIENT_SECRET=네이버_클라이언트_시크릿
  ```
  > https://api.telegram.org/bot{봇  토큰}/getUpdates에 접속해 사용자의 채팅id를 확인할 수 있습니다.

5. 검색어 설정:
query_list 변수를 수정해 검색할 단독 뉴스의 키워드 목록을 지정합니다.


## 사용 방법
1. 프로그램을 실행합니다.

```bash
python dandok_news.py
```

2. 프로그램이 실행되면 검색어 목록을 텔레그램으로 전송하고, 신규 단독 뉴스를 검색해 알림으로 전송합니다.

3. 신규 단독 뉴스가 발견될 때마다 텔레그램으로 알림을 받을 수 있습니다.

## 기타 정보
- 로깅: 프로그램은 error.log 파일에 오류 로그를 기록합니다.
- 이전 단독 뉴스 목록: 이전에 발견된 단독 뉴스 목록은 old_dandok_list.json 파일에 저장되며, 프로그램 재실행 시 기존 목록을 로드합니다.
