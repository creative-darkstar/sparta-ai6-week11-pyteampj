# sparta-ai6-week11-pyteampj
팀 스파르타 AI 6기 11주차 팀 프로젝트 (2024-05-10 제출)

## 프로젝트 명: Sparta NEWS
Sparta NEWS에서 최신 정보를 확인하세요 (reference: [GeekNews](https://news.hada.io/))


## 개요

☆ 포인트 기능

날짜가 하루 지날때 마다 -5 Point, 댓글 하나당 +3 Point, 좋아요 하나당 +1 Point

### 글 전체 페이지(`api/content/`)

[API] News 리스트 보여주기 1 (포인트 많은 순으로 정렬 + 날짜 최신순으로 정렬)

- 쿼리 스트링으로 order-by=new 들어오면 최신순
- 쿼리 스트링으로 user=A 들어오면 A id를 가진 유저가 작성한 글 목록
- 쿼리 스트링으로 liked-by=A 들어오면 A id를 가진 유저가 좋아요를 누른 글 목록
- 쿼리 스트링으로 favorite-by=A 들어오면 A id를 가진 유저가 즐겨찾기를 누른 글 목록

★ 전체 리스트에서 뿌려줄 데이터

- 제목
- URL
- 글 내용(요약본 <- 선택사항)
- 포인트
- 작성자
- 댓글 개수
- 작성일시
- 수정일시

### 글 작성 페이지 (`api/content/`)

[API] News 작성하기

★ 글 작성 시 필요한 데이터
- 타입 (뉴스, Ask, Show)
- 제목
- URL
- 내용

### 글 상세 페이지 ( `/content/<int:content_id>/` )

[API] News 디테일 페이지 보여주기

★ 상세 페이지에서 뿌려줄 데이터
- 제목
- 글 내용
- URL
- 포인트
- 작성자
- 댓글 개수
- 작성일시
- 수정일시

### ★ 글 즐겨찾기 기능 (`/content/<int:content_id>/favorite/`)

[API] News 찜하기

즐겨찾기 한 상태면 취소, 즐겨찾기 안 한 상태면 등록

### ★ 글 좋아요 기능(`/content/<int:content_id>/like/`)

[API] News 에 좋아요 누르기

좋아요 한 상태면 취소, 좋아요 안 한 상태면 등록

### ★ 댓글 조회/작성 기능(`content/<int:content_id>/comment/`)

[API] News 댓글 보여주기

[API] News 댓글 작성하기

★ 댓글 데이터
- 작성자
- 내용
- 작성일시
- 수정일시

[API] News 댓글 수정하기(`content/comment/<int:comment_id>/`)

[API] News 댓글 삭제하기(`content/comment/<int:comment_id>/`)

### ★ 댓글 좋아요 기능(`content/comment/<int:comment_id>/like/`)

[API] News 댓글에 좋아요 누르기

좋아요 되어 있으면 취소, 좋아요 안되어있으면 등록


### Auth

#### 회원가입 ( `/user/signup/` )

[API] 회원가입

★ 회원가입 데이터

- 아이디
- 비밀번호 (비밀번호 확인)


[API] 로그인 / 로그인 갱신 / 로그아웃

- 로그인 갱신 ( `/user/token/refresh/` )
- 로그인/로그아웃 ( `/user/login/` , `/user/logout/` )

#### Profile (`/user/<str:username>/`)

★ 유저 페이지 데이터
- username
- 가입일 (date_joined)
- 소개 (introduction)
- 작성한 글 페이지( `/content?user=<user_id>` )
- 작성한 댓글 페이지( `/content/comment?user=<user_id>` )
- 즐겨찾기한 글 페이지( `/content?favorite-by=<user_id>` )

  [API] 즐겨찾기 한 News 목록 보여주기

→ 로그인 후 본인 프로필 페이지에 접근한 경우

- 좋아요 한 페이지( `/content?liked-by=<user_id>` )
    
    [API] 좋아요 한 News 목록 보여주기
    
- 좋아요 한 댓글( `/content/comment?liked-by=<user_id>` )
    
    [API] 좋아요 한 News 댓글 목록 보여주기


## ERD

![ERD](https://github.com/creative-darkstar/sparta-ai6-week11-pyteampj/assets/159861706/8a88d3a7-cc4c-4d84-9231-b203551a62ef)


## API 명세

- Articles

| Method                                 | Authorization | endpoint                     | Description                                                                                                                                                                                                                                     |
|----------------------------------------|---------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <span style="color:green">GET</span>   | `Anonymous`   | `/api/content/`             | 전체 페이지 (정렬기준: ① 날짜 최신순 ② 포인트 많은 순) <br> - 쿼리 스트링으로 order=new 들어오면 최신순 <br> - 쿼리 스트링으로 user=A 들어오면 A id를 가진 유저가 작성한 글 목록 <br> - 쿼리 스트링으로 liked_by=A 들어오면 A id를 가진 유저가 좋아요를 누른 글 목록 <br> - 쿼리 스트링으로 favorited_by=A 들어오면 A id를 가진 유저가 즐겨찾기를 누른 글 목록 |
| <span style="color:yellow">POST</span> | `User`        | `/api/content/`        | 글 작성                                                                                                                                                                                                                                            |
| <span style="color:green">GET</span>   | `Anonymous`        | `/api/content/<int:content_id>` | 상세 페이지 (게시글 해당)                                                                                                                                                                                                                                 |
| <span style="color:skyblue">PUT</span> | `User`     | `/api/content/<int:content_id>` | 글 수정 (로그인한 사용자이면서 해당 글 작성자여야 가능)                                                                                                                                                                                                                |
| <span style="color:red">DELETE</span>  | `User`     | `/api/content/<int:content_id>` | 글 삭제 (로그인한 사용자이면서 해당 글 작성자여야 가능)                                                                                                                                                                                                                |
| <span style="color:yellow">POST</span> | `User`     | `/api/content/<int:content_id>/favorite` | 글 즐겨찾기                                                                                                                                                                                                                                          |
| <span style="color:yellow">POST</span> | `User`     | `/api/content/<int:content_id>/like` | 글 좋아요                                                                                                                                                                                                                                           |
| <span style="color:green">GET</span>   | `Anonymous`     | `/api/content/<int:content_id>/comment` | 상세 페이지의 댓글 데이터 (정렬기준: 날짜 최신순)                                                                                                                                                                                                                   |
| <span style="color:yellow">POST</span> | `User`     | `/api/content/<int:content_id>/comment` | 댓글 작성                                                                                                                                                                                                                                           |
| <span style="color:green">GET</span>   | `Anonymous`     | `/api/content/comment` | 댓글 페이지 <br> - 쿼리 스트링으로 user=A 로 하면 A id를 가진 유저가 작성한 댓글 목록 <br> - 쿼리 스트링으로 liked_by=A 들어오면 A id를 가진 유저가 좋아요를 누른 댓글 목록                                                                                                                                |
| <span style="color:skyblue">PUT</span> | `User`     | `/api/content/comment/<int:comment_id>` | 댓글 수정                                                                                                                                                                                                                            |
| <span style="color:red">DELETE</span>   | `User`     | `/api/content/comment/<int:comment_id>` | 댓글 삭제                                                                                                                                                                                                                           |
| <span style="color:yellow">POST</span>   | `User`     | `/api/content/comment/<int:comment_id>/like` | 댓글 좋아요                                                                                                                                                                                                                            |

- Accounts

| Method                                 | Authorization | endpoint                      | Description                                                                                                          |
|----------------------------------------|---------------|-------------------------------|----------------------------------------------------------------------------------------------------------------------|
| <span style="color:yellow">POST</span>   | `Anonymous`      | `/api/user/signup/`              | 회원가입 - JWT                                                                                                           |
| <span style="color:yellow">POST</span>   | `User`      | `/api/user/login/`          | 로그인 - JWT                                                                                                            |
| <span style="color:yellow">POST</span> | `User`         | `/api/user/logout/` | 로그아웃 - JWT                                                                                                           |
| <span style="color:green">GET</span> | `Anonymous`      | `/api/user/<str:username>/` | 유저 페이지 (로그인 상태 / user의 페이지로 들어왔을 때 더 많은 정보가 DP) <br> - 다른 유저 볼 때는 username, 가입일, 소개 DP / 작성글, 작성댓글, 즐겨찾기글 <br> - 내꺼 볼 때는 username, 가입일, 소개 DP / 소개 수정 가능 / PW 수정 가능 / 작성글, 작성댓글, 즐겨찾기글, 추천글, 추천댓글 |
| <span style="color:skyblue">PUT</span>  | `User`      | `/api/user/<str:username>/` | 유저 페이지 수정 (내 꺼만 가능. 수정 가능 필드: 소개, PW)                                                                               |


## 역할 분담
    
- 권진우: 글 CUD, 글 즐겨찻기, 글 좋아요

- 박지현: Accounts API 전체

- 정해진: 프로젝트 총 책임
  - 프로젝트 생성
  - model 정의(초기 앱 구조 및 `models.py` 작성)
  - 브랜치(dev, main, 기능 브랜치) 관리
  - 글 전체 조회/Filtering/Ordering
  - 댓글 전체 조회/Filtering/Ordering
  - 댓글 CUD, 댓글 즐겨찾기, 댓글 좋아요
  - 담당 외 코드 수정

- 진성길: -
    

## 사용하는 기술
- Python
- Python Django
- Python Django Rest Framework
- DB: SQLite3
- Server: Django


## 설치 필요 패키지
- requirements.txt에 명시
- `pip install -r requirements.txt` 로 설치