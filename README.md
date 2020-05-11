## Introduction

#### Topic 
- 온라인 유기농 식재료 마켓 클론 프로젝트

#### Team 
- 프론트앤드 3명, 백앤드 3명

#### Project Period 
- 2020.02.27 - 2020.03.06

#### Coworking 
- Trello를 스크럼방식 협업
- 주단위 백로그작성
- 일단위 스탠드업미팅
         
## 담당 개발 내역
[Modeling]
- 크게 user, product, order 로 분류
- 자기참조 : 유사상품 개념을 표현
- 하나의 상품이 시즌정보를 가지도록 설계
- 여러개의 상품을 번들로 묶어서 판매하는 프로모션 
- 장바구니와 주문 

[Django 프로젝트 초기 설계]
- my_settings.py : database 정보, secret key, jwt 알고리즘 정보 관리
- requirements.txt : 개발 환경 공유

[상품 / 레시피 데이터 크롤링]
- beautiful soup, requests
- pandas 를 통한 csv 파일 생성

[홈화면 데이터 표출] 
- 카테고리별 상품 표출
- 시즌별 상품 표출
- 세일 상품 표출

[상품 리스트 표출]
- 전체 상품 / 카테고리별 상품 표출
- 가격 / 이름 을 기준으로 받아서 정렬
- pagination : offset과 limit을 받아서 구현

[상품 상세 정보 표출]
- 상품의 상세정보(영양정보, 유사상품, 가격 등) 표출

[번들 프로모션 상품 표출]
- 상품과 번들 프로모션은 서로가 서로를 여러개 가질 수 있는 many to many 관계. 
- 하나의 번들 프로모션이 여러개의 상품을 가지고 있고 묶음으로 가격이 정해짐
- 번들 프로모션의 가격과 그에 포함된 상품들을 가져와 표출
- 프로모션 기간이 끝나면 is_in_promotion 컬럼이 False로 바뀜

[레시피 리스트 표출]
- pagination : offset과 limit을 받아서 구현

[레시피 상세 정보 표출]
- 레시피 상세정보(제조법, 레시피 설명, 저자 등) 표출

[추천 레시피 표출]
- 하나의 레시피는 여러개의 상품을 가지고 있는 one to many관계에 있음
- 추천 레시피와 레시피에 포함된 상품들을 표출
         
## Demo
Click below image to see our demo.


[![Foodly demo](https://i.ibb.co/DbfDptM/Screen-Shot-2020-03-17-at-8-46-32-PM.png=200x)](https://www.youtube.com/watch?v=1K8aV-KZMQw&feature=youtu.be)

## APIs
+ Signup and signin features(Seunghyun Ahn).
+ Display all items with the features of pagination and sorting(Heechul Yoon)
+ Show bundle items as promotion(Heechul Yoon)
+ Show similar products of a chosen product(Heechul Yoon)
+ Add, change, and delete items in a user's wishlist and cart(Sooyeon Kim).


## Technologies
+ Language           : Python 3.8.0
+ Web Framework      : Django 3.0.4
+ Database           : AWS RDS with MySQL
+ HTTP headers       : Cross-Origin Resource Sharing (CORS) headers
+ Encryption         : bcrypt
+ Web Token          : JWT
+ Web Scraping       : BeautifulSoup 4.0, Pandas
+ Version management : Git

## API Documentation
+ [signup, signin, order](https://documenter.getpostman.com/view/10398571/SzS4T8ME)
+ [products](https://documenter.getpostman.com/view/10644576/SzS8rjuD?version=latest#09377cd1-b1c6-47cc-930d-0c6e2d84c1ba)


## Database Modeling
![Foodly ERD](https://i.ibb.co/rFFmfMf/foodly-20200317-21-43.png)
