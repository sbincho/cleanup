<div align="center">

# 생성 AI 기반 야구 채팅 메시지 순화 솔루션

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/FastAPI-%2334D058.svg)](https://fastapi.tiangolo.com/ko/)

</div>

## 한눈에 보기
- 무엇을 만들었나 :  채팅 메세지 유해 유형 분류 모델, 표현 순화를 위한 프롬프트 엔지니어링, 서비스 웹 화면, 채팅 서비스
- 핵심 성과 : 채팅 메시지 유해 유형 성능 
- 내 역할 : 야구 채팅 데이터 크롤링, 채팅 메세지 유해 유형 분류 모델 개발, 서비스 웹 화면 개발, 채팅 기능 구현

---
## 핵심 성과
<img width="1275" height="455" alt="Image" src="https://github.com/user-attachments/assets/667b100f-f546-4fa3-aa1b-790a95baae74" />

```text
[val data] Macro F1 = 0.9580 | Acc = 0.9675
[unseen data] Macro F1 = 0.8227 | Acc = 0.8776
```

---
## 프로젝트 개요
야구는 최근 온‧오프라인 모두 높은 인기를 끄는 스포츠로 온라인에서도 ‘채팅’참여를 통해 다수와 함께 응원하며 경기의 즐거움을 증대할 수 있으나, 경기와 상관 없는 메시지가 이용자의 즐거움 반감 및 불쾌감 초래하고 있습니다. 따라서 사용자의 표현의 자유를 존중하면서 쾌적한 서비스 환경을 제공하고자 합니다.

### 프로젝트 정보
- **기간**:  2024.07.05~2024.08.20 
- **팀 구성**: 5명
- **역할**:  야구 채팅 데이터 크롤링, 채팅 데이터 유해 유형 분류 모델 개발, 서비스 웹 화면 개발, 채팅 기능 구현
- **성과**: 교육 과정 **최우수상 수상**

- ### 파일 설명

- **code.ipynb** 분석을 위해 작성한 전체 코드
- **presentation.pdf** 프레젠테이션을 위해 제작한 ppt의 pdf 버전

---
### 클린업 알고리즘 프로세스
<img width="1287" height="585" alt="Image" src="https://github.com/user-attachments/assets/5f24671c-3d09-4fc9-8af9-eefb7b24abe9" />


### 채팅 데이터 유해 유형 및 솔루션
<img width="1282" height="510" alt="Image" src="https://github.com/user-attachments/assets/a01e9b71-0f01-48c0-a580-014d3681f1c7" />
<img width="1286" height="408" alt="Image" src="https://github.com/user-attachments/assets/716d610f-de32-45d5-bf5a-1df4922469b3" />
<img width="1285" height="466" alt="Image" src="https://github.com/user-attachments/assets/02acde01-554d-4408-8744-816261d590a8" />

---
## 알고리즘 설계 및 개발
### 모델 선정 과정
<img width="1296" height="481" alt="Image" src="https://github.com/user-attachments/assets/ee704754-f3ee-408e-890a-5672e6039868" />



### 모델 성능 개선 과정

<img width="1158" height="427" alt="Image" src="https://github.com/user-attachments/assets/1334375c-6767-402f-ab0c-08c71dfc6645" />

### 모델 평가

<img width="1275" height="455" alt="Image" src="https://github.com/user-attachments/assets/667b100f-f546-4fa3-aa1b-790a95baae74" />


### 데이터 세트의 특징

- 출처: kaggle, aihub, 공공데이터포털 등등

데이터 세트 선택 근거: (왜 이 데이터 세트인지)

- 구성: feature의 종류, 데이터 개수, 각 feature의 자료형 등 dataset을 설명할 수 있는 모든 것 (←kaggle에 올라오는 notes를 참고해보아도 좋을 듯)

### 결과 요약

- 가설: 검증되었는지?
- 목표: 달성되었는지?
- 그 밖에 기획단계에서는 기대하지 않았던 인사이트가 있다면?

### 한계점과 보완 방안

- 한계: 데이터상의 한계, 모델 구축상의 한계, HW상의 한계 등
- 보완 방안: 내가 해결할 수 있는 것 위주로 쓰기
