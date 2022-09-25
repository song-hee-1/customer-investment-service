# Customer Investment Service

**Batch script**를 바탕으로 주어진 고객 투자 데이터를 응답하고
**투자금**을 **입금**할 수 있는 REST API 서비스 

</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 주체](#프로젝트-주체)
      - [💭 프로젝트 설명](#-프로젝트-설명)
      - [🛠 개발 조건](#-개발-조건)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)
  * [TIL](#til)


</br>

## 개발 기간
**2022.09.16 ~ 2022.09.21** 

</br>
</br>
  
## 프로젝트 개요


#### 프로젝트 주체 

![image](https://user-images.githubusercontent.com/83492367/192143582-116be357-c347-4bbc-9d32-a58b3185f5cd.png)



[디셈버앤컴퍼니(핀트)](https://www.dco.com/)

</br>

#### 💭 프로젝트 설명

주어진 **고객 투자 데이터**를 응답하는 REST API 개발

</br>

#### 🛠 개발 조건



> * **데이터**
> 	* 개발에 필요한 기본 데이터 셋 제공
> 	* 주어진 데이터셋이 효과적으로 이용될 수 있게 자유롭게 모델링하여 구현 


> * **Batch**
> 	* 제공된 테스트 데이터 셋을 API에서 사용할 수 있게 정제하여 로딩하는 batch script 작성
> 	* 데이터 셋은 그날의 데이터가 매일 새로 제공되는 것 가정
> 	* 제공되는 테스트 데이터에는 오류 데이터가 포함될 수 있으며, 그 외 정상 데이터들은 모두 로딩되어야 함

> * **API**
> 	* 위에서 설계하고 로딩한 데이터를 고객에게 제공하는 API 개발
> *  **데이터 조회**
> 		* 데이터 셋에 포함된 특정 고객의 자산 정보를 조회하는 API 개발
> 		* 개발할 API의 화면과 응답에 필요한 데이터는 아래와 같음
> 			* 투자 화면 API
> 				* 계좌명
> 				* 증권사
> 				* 계좌번호
> 				* 계좌 총 자산
> 			* 투자상세 화면 API
> 				* 계좌명
> 				* 증권사
> 				* 계좌번호
> 				* 계좌 총 자산
> 				* 투자 원금
> 				* 총 수익금 ( 총 자산 - 투자 원금 )
> 				* 수익률 ( 총 수익금 / 투자 원금 * 100) 
> 			* 보유종목 화면 API
> 				* 보유 종목명
> 				* 보유 종목의 자산군
> 				* 보유 종목의 평가 금액 ( 종목 보유 수량 * 종목 현재가 )
> 				* 보유 종목 ISIN
> * **투자금 입금**
> 		* 투자금 입금은 2 phase로 이루어짐
> 
> 		**Phase1 API**
> 		* 입금 거래 정보들을 서버에 등록
> 			* 요청 데이터
> 				* 계좌번호
> 				* 고객명
> 				* 거래 금액
> 
> 			* 응답 데이터
> 				* 거래정보 식별자 - 요청 데이터 묶음을 식별할 수 있는 key 값

> 		**Phase2 API**
> 		* phase1에서 등록한 거래정보 검증 후 실제 고객의 자산 업데이트
> 		* 거래 정보를 hashing하여 서버에 phase2 요청을 하면 서버에서는 phase1에서 등록하여 저장된 데이터를 hashing하여 동일한 데이터에 대한 요청인지 검증
> 		* 검증에 성공하면 고객의 총 자산을 업데이트하고 성공 응답, 검증 실패시 자산 업데이트 없이 실패 응답
> 			* 요청 데이터
> 				* phase1 요청 데이터 계좌번호, 고객명, 거래 금액 순서로 연결한 string을 hash한 string
> 				* phase1에서 응답받은 거래정보 식별자
> 
> 			* 응답 데이터
> 				* 입금 거래 결과



</br>

#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST Framework, Crontab
- **Database** : SQLite, PostgreSQL
- **ETC** : Git, Github, Azure

</br>



#### 📰 모델링

![Untitled (4)](https://user-images.githubusercontent.com/83492367/192148805-4b900696-b99c-48c3-ba63-9d87e716c505.png)



- 주어진 데이터 외 서비스 흐름을 고려하여 `User(사용자)`, `Account(계좌)`, `Stock Securities(증권사)`, `Stock(증권)`, `Assget Group(자산군)`, )`Transfer(입금)`의 테이블로 모델링

	- 한`User(사용자)`는 **여러 개**의 `Account(증권계좌)`를 가질 수 있음 (실제 서비스에서 이를 확인하여 적용)
	- `Stock Securities(증권사)`와 `Assget Group((자산군)`은 데이터의 추가 및 수정이 용이하도록 **외래키**를 이용하여 참조
	- 가격 변동이 많은 `Stock(증권)`의 가격의 특성을 고려하여 stock에 current_price를 이용하여 값들 계산하도록 정의
	- `Stock(증권)`의 **기본키(PK)**는 **국제 증권 식별 번호**인 **isin**를 이용

	- `Account`와 `Stock`는 **다대다(M:N)관계**이며,  수량과 투자 시간, 투자 원금에 대한 **정보**를 **추가**로 나타내기 위하여 `investment`라는 **중간 테이블** 정의

- 각 데이터의 특성을 고려하여 `IntegerField `, `PositiveIntegerField `,  `PositiveBigIntegerField `를 나누어 사용

</br>

#### 🛠 API Test

- 특정 고객의 자산 정보가 제대로 조회되는지 확인하기 위한 테스트 코드 작성

- 투자금 입금 단계에 따른 유효성 검증이 제대로 작동하는지 확인하기 위한 테스트 코드 작성

![image](https://user-images.githubusercontent.com/83492367/192147535-81439276-deb6-4fe4-99f4-f351926e973d.png)





</br>

## 프로젝트 분석
- 개발 조건과 확장성을 고려하여 `accounts`, `investments`, `stocks`, `transfers`의 4개의 앱으로 분리
- 모델링 내용을 바탕으로 기업에서 제공해 준 초기 데이터 가공 
	- 가공한 각 데이터는 각 앱의 `data` 폴더에 테이블별로 존재
	-  초기 데이터`account_asset_info_set`에 같은 증권(=isin이 같음)임에도 `현재가`가 다른 문제를 확임
		- `현재가`를 `구매단가`라 생각해도 `account_basic_info_set`의 `계좌별 투자원금`과 값이 상이하여 오류로 판단
		- `현재가`를 임의로 설정하여 진행 

- Batch
	- `Crontab`을 이용하여 매일 오전 9시 00분 ~ 15분 사이에 새로운 데이터로 갱신되도록 처리
		- 초기 데이터가 많지 않아 15분 소요
		- 데이터가 많아진다면 다른 시간대 설정 및 각 작업 소요시간을 예측할 필요

- 데이터 조회 API
	- `Serializer`에서 `반복되는 계산(method field)`를 줄이기 위하여 `투자화면 Serializer`는 `투자상세 화면 serializer`를 상속 
	- `투자화면`과 `투자상세화면`이 하나의 url에서 처리될 수 있도록,  `is_simple`이라는 parameter를 이용하여 화면 전환 가능하도록 처리 
	- 계좌별 `total asset(총 자산)`을 계산하기 위해 Django ORM의 `annotate`와 `F 객체` 이용
	- 외래 테이블의 필드인 `Stock(증권)`의 `current price(현재가)`를 이용하여 `계좌 총 자산`을 계산하므로, 각 증권의 현재가 값만 업데이트하면 이에 따라 각 값들이 자동으로 계산되도록 설계

	
- 투자금 입금 API
	- phase 1
		- 입력받은 `계좌번호`가 실제 존재하는 정보인지 유효성 검증
		- 입력받은 `사용자 이름`이 실제 존재하는 정보인지 유효성 검증
		- 입력받은 `계좌번호의 명의`가 입력받은 사용자 이름과 일치하는지 검증
		- 유효성 검증을 통과한다면,  `bcrypt`를 이용한 hashing값을 DB 저장
		- 요청 데이터와 응답 데이터 처리를 위하여 다른 serializer를 이용
	- phase 2 
		- phase1에서 DB에 저장한 hashing(signature)값과 각 필드의 값을 연결한 string이 같은지 확인
		-  값이 틀린다면 자산 업데이트 없이 실패 응답
		- 값이 일치한다면 계좌의 투자원금값을 더하고, 투자 테이블에 현금자산(asset_group_id=7) 내역 추가
</br>

## API ENDPOINT

### investments
URL|Method|Description|
|------|---|---|---|
|"api/investments"|GET|로그인 한 고객의 투자상세 화면 |
|"api/investments?is_simple=true"|GET|로그인 한 고객의 투자 화면(is_simple parameter 이용) |
|"api/investments/holdings"|GET|로그인 한 고객의 보유종목 화면


### transfers

URL|Method|Description|
|------|---|---|---|
|"api/transfers-verifications"|POST|phase1 : 입금 거래 정보를 서버에 등록 |
|"api/transfers"|POST|phase2: phase1에서 등록한 거래정보를 토대로 고객 자산 업데이트 |
- 단, phase2에서는 자산 업데이트 성공시 status 및 관련 테이블 값만 업데이트


</br>



## TIL

- [[TIL] ModuleNotFoundError: No module named ‘django’ 에러 해결하기](https://medium.com/@heeee/til-modulenotfounderror-no-module-named-django-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0-c00bb1a96682)
- [[TIL] DRF serializer에서 외래키 테이블의 필드 가져오기](https://medium.com/@heeee/til-drf-serializer%EC%97%90%EC%84%9C-%EC%99%B8%EB%9E%98%ED%82%A4-%ED%85%8C%EC%9D%B4%EB%B8%94%EC%9D%98-%ED%95%84%EB%93%9C-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0-242c06b25dc2)





