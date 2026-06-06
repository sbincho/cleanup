<div align="center">

# 생성 AI 기반 야구 채팅 메시지 순화 솔루션

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/FastAPI-%2334D058.svg)](https://fastapi.tiangolo.com/ko/)

</div>

## 한눈에 보기
- 무엇을 만들었나 :  채팅 메세지 유해 유형 분류 모델, 표현 순화를 위한 프롬프트 엔지니어링, 서비스 웹 화면, 채팅 서비스
- 핵심 성과 : 채팅 메세지 유해 유형 분류 모델 성능 **Acc = 0.6078 → 0.8955** 로 개선
- 내 역할 : 야구 채팅 데이터 크롤링, 채팅 메세지 유해 유형 분류 모델 개발, 서비스 웹 화면 개발, 채팅 기능 구현

---
## 핵심 성과
- 채팅 메세지 유해 유형 분류 모델 성능 **Acc = 0.6078 → 0.8955** 로 개선
- 모델 성능 검증 단계에서 타종목 및 타분야 데이터를 추가로 활용하여 개발한 모델이 야구 데이터에만 과도하게 특화되지 않았는지 검증하고 일반화 성능을 확인
<img width="1275" height="455" alt="Image" src="https://github.com/user-attachments/assets/667b100f-f546-4fa3-aa1b-790a95baae74" />



---
## 프로젝트 개요
야구는 최근 온‧오프라인 모두 높은 인기를 끄는 스포츠로 온라인에서도 ‘채팅’참여를 통해 다수와 함께 응원하며 경기의 즐거움을 증대할 수 있으나, 경기와 상관 없는 메시지가 이용자의 즐거움 반감 및 불쾌감 초래하고 있습니다. 따라서 사용자의 표현의 자유를 존중하면서 쾌적한 서비스 환경을 제공하고자 합니다.

### 프로젝트 정보
- **기간**:  2024.07.05~2024.08.20 
- **팀 구성**: 5명
- **역할**:  야구 채팅 데이터 크롤링, 채팅 데이터 유해 유형 분류 모델 개발, 서비스 웹 화면 개발, 채팅 기능 구현
- **성과**: K-디지털 트레이닝 훈련 Demo-day **대상(1위)**

---
### 클린업 알고리즘 프로세스
<img width="1287" height="585" alt="Image" src="https://github.com/user-attachments/assets/5f24671c-3d09-4fc9-8af9-eefb7b24abe9" />


### 채팅 데이터 유해 유형 및 솔루션

#### 비하/비난, 조롱/비꼬기 ▶ OpenAI API ‘GPT-4o-mini’모델 활용, 프롬프트 엔지니어링
<img width="1282" height="510" alt="Image" src="https://github.com/user-attachments/assets/a01e9b71-0f01-48c0-a580-014d3681f1c7" />

#### 분위기 조장 ▶ 권고문 출력
<img width="1286" height="408" alt="Image" src="https://github.com/user-attachments/assets/716d610f-de32-45d5-bf5a-1df4922469b3" />

#### 욕설/비속어, 멸칭 ▶ re모듈 & 정규표현식 활용, 비공식 언어 표현 마스킹 및 대체어 출력
<img width="1285" height="466" alt="Image" src="https://github.com/user-attachments/assets/02acde01-554d-4408-8744-816261d590a8" />

## 클린업 솔루션 특장점
### "야구 채팅 언어 특화 솔루션"

**1. 표현 순화&긍정화**
- 단어를 넘어, 문장을 읽어 표현을 순화 및 긍정화

**2. 자연스러운 권유문**
- 자연스러운 권유문 노출로 필터링과 동시에 유저 윤리 의식 제고

**3. 빠른 신조어 대응 가능**
- 야구 특화 사전, 유해 말뭉치 사전기반 제작 GUI 제공
- 명사형 단어 검색 및 추가 기능으로 신조어 대응 빠른 필터링 가능
---
## 알고리즘 설계 및 개발
### 모델 선정 과정
<img width="1296" height="481" alt="Image" src="https://github.com/user-attachments/assets/ee704754-f3ee-408e-890a-5672e6039868" />

```text
kcelectra | Acc = 0.4216
kcbert | Acc = 0.6078
```
온라인 뉴스에서 댓글과 대댓글을 수집해 학습한 딥러닝 모델 KcELECTRA와 KcBERT 중 프로젝트 데이터에 더 좋은 성능을 내는 KcBERT 모델을 채팅 메세지 유해 유형 분류 모델로 채택하였습니다.

### 모델 성능 개선 과정

<img width="1158" height="427" alt="Image" src="https://github.com/user-attachments/assets/1334375c-6767-402f-ab0c-08c71dfc6645" />

| label | count | 
|------|-----------|
| **무해** | **48,927** |
| 비하/비난 | 749 |
| 조롱/비꼬기  | 294 |
| 분위기 조장 | 432 | 


#### 1. 무해 데이터 유사 표현 절감
압도적인 무해 데이터의 양을 다운 샘플링 하기 전 보다 다양한 표현을 학습하기 위해 코사인 유사도 60을 기준으로 그룹화하여 각 그룹당 1개의 데이터만 남기고 나머지는 제거하였습니다.

#### 2. 무해 데이터 다운 샘플링
모델이 무해 데이터에 과적합 되는 것을 막기 위해 무해 데이터와 유해 데이터의 비율을 6:4로 맞추어 파인 튜닝을 진행하였습니다.

#### 3. 하이퍼 파라미터 튜닝
Grid Search를 통해 가장 높은 Validation Accuracy 값을 갖는 조합을 선정하여 Validation Accuracy를 0.6078 -> 0.8955로 개선

## 시스템 구현
<img width="1100" height="693" alt="image" src="https://github.com/user-attachments/assets/ea3e7a5e-303c-4a80-b20b-690303207a9b" />

FastAPI와 WebSocket을 이용하여 채팅 시스템을 구현하였습니다.



