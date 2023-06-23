################################ 1. 환경 설정  ###################################

import pandas as pd
import numpy as np
import datetime
import streamlit as st
import datetime

##################################################################################


################################ 2. 데이터 전처리  ################################

## 2.1 환자 데이터 : CSV 파일 불러오기
data = pd.read_csv('patience_list_2.csv', encoding="cp949")

## 2.2 환자 상태에 따른 데이터 정렬
sorted_data = data.sort_values(by=['환자 상태'], key=lambda x: x.map({'응급': 0, '주시': 1, '정상': 2}), ignore_index=True)

## 2.3 스트림 릿 내 데이터프레임의 열의 특성에 맞춰, 자동으로 변환되는 datatype을 방지하기 위해 문자열로 지정

sorted_data['수술연도'] = sorted_data['수술연도'].astype(str)
sorted_data['체온'] = sorted_data['체온'].astype(str)

## 2.4 화면 비율 설정 - wide
st.set_page_config(layout="wide")

#################################################################################


######################### 3. 대시보드 구성 - tab1 , tab2 #########################

tab1, tab2 = st.tabs(['관제 시스템', '사용자 맞춤형'])

############ 3.1 tab1 : KT의 AICC 관제 시스템 구성 ################ 
with tab1:
    
    ### 3.1.1 위급 레이아웃 :  위급 상황 발생 시 이벤트 화면을 띄워줌. 위급은 기가지니 음성인식을 통한 더블 체크 후에도 환자가 반응이 없을 경우 위급이라 판단함. ###
    
    st.markdown('# [위급]')
    st.markdown('## 현재 발생한 위급환자가 없습니다.')
    
    ### 3.1.2 환자 리스트 레이아웃 : 현재 운전 중인 환자들의 데이터들을 자동으로 불러오며, 기입력된 환자 데이터를 보여줌.    ###
    ### 이는 환자 동의 하에 따른 기입력된 데이터들이며, 응급 상황 발생 시 병원에서는 이를 기반으로 신속한 의료 처치가 가능함. ###
    
    st.markdown('# 환자리스트')

    ### 3.1.2.1 '환자 상태'가 '주시'인 행 인덱스를 추출
    highlighted_indices = sorted_data[sorted_data['환자 상태'] == '주시'].index

    ### 3.1.2.2 '환자 상태'가 '응급'인 행 인덱스를 추출
    emergency_indices = sorted_data[sorted_data['환자 상태'] == '응급'].index

    ### 3.1.2.3 스타일이 적용된 환자 리스트를 화면에 출력
    st.write(
        sorted_data.style.apply(
            lambda _: ['background-color: green' if index in highlighted_indices else 'background-color: red' if index in emergency_indices else '' for index in range(len(sorted_data))],
            axis=0
        )
    )

### 환자 맞춤형 대시보드 프로토타입 구현
    
######################################################################

############ 3.2 tab2 : 환자 맞춤형 운전화면  ##########################
### 가족의 동의하에 따른 환자의 운전화면을 체크할 수 있음
### 이때 과거의 이벤트 발생 이력을 알려주며, 이는 이미 문자나 관제 시스템을 통해 알림을 제공한 상태임.
###

with tab2:

    ### 3.2.1 환자 운전화면 레이아웃 : 특정 환자의 실시간 운전 화면을 나타내는 것을 프로토타입으로 제작
    st.markdown('## 배** 운전 화면')
    st.markdown('### 2023-06-29')
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.write('')
    with col2:
        st.image('normal_resize.gif', width= 300)
    with col3:
        st.write('')

    ### 3.2.2 환자 이벤트 발생 이미지 : 환자가 운전을 하면서 발생한 이벤트에 대해 이미지/날짜/회수 등을 포함하여 시각적으로 제공 해줌.    
    st.markdown('## 최근 발생 이벤트')
    st.markdown('### 최근 발생한 이벤트가 없습니다.')

#################################################################################
