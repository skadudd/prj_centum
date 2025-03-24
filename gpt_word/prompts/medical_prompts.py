# prompts/medical_prompts.py
"""
의학 텍스트 분류를 위한 프롬프트 모음
"""

class CCPrompts:
    """Chief Complaint 관련 프롬프트"""
    
    @staticmethod
    def cc_analysis_prompt(texts):
        """CC 분석 프롬프트"""
        return f"""
            환자의 증상을 설문한 정보입니다. 당신은 구강내과 전문의이며, CC 설문 조사를 통해 결과적으로 입이 안벌어지거나, 나쁜 소리, 통증 등을 파악하여 환자를 분류하길 원합니다.
            다음 주요 증상(CC) 텍스트들을 분석하여 JSON 형식으로 분류해주세요.
            
            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. location: 통증/증상 위치 (문자열)
            2. pain_type: 통증/증상 종류 (문자열)
            3. painUncomp_desc_jaw: 턱 통증/불편감 턱 관절의 통증, 소리, 움직임 제한 등과 관련된 증상을 포함하는 카테고리 (문자열)
            4. disable_desc_jaw: 턱 관절의 비정상적인 움직임, 소리, 제한된 개구 등의 증상을 다루는 카테고리 (문자열)
            5. muscle_joint_desc_stress: 스트레스로 인한 턱 근육의 긴장, 통증, 이갈이 등의 증상을 포함하는 카테고리 (문자열)
            
            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "location": "위치",
                "pain_type": "통증 종류",
                "painUncomp_desc_jaw": "환자의 턱 통증/불편감",
                "disable_desc_jaw": "환자의 턱 관절 비정상적 움직임",
                "muscle_joint_desc_stress": "환자의 스트레스로 인한 턱 근육 긴장"
            }}]"""
    
    @staticmethod
    def cc_history_prompt(texts):
        """CC 병력 및 습관 관련 프롬프트"""
        return f"""
            환자의 턱관절 병력 및 습관 정보입니다. 다음 텍스트를 분석하여 JSON 형식으로 분류해주세요.
            텍스트에 없는 내용은 지어내지 마세요.
            
            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. dentalHistory_desc: 교정 치료, 보톡스, 물리치료 등 치과적 개입과 관련된 증상 및 경과를 다루는 카테고리 (문자열)
            2. clinic_history_desc: 턱관절장애 관련 과거 병력, 치료 이력, 발병 시기 및 계기 등을 포함합니다. 교정 치료, 외상, 수술 등이 언급되는 카테고리 (문자열)
            3. factor_habbit: 음식 섭취 습관, 수면 자세, 이 악물기 등 일상생활과 연관된 턱 관절 증상을 포함하는 카테고리 (문자열)
            4. treat_plan: 물리치료, 약물요법, 장치치료, 보톡스 주사 등 계획된 치료 방법과 치료 경과 및 반응을 포함합니다. 치료 계획 변경, 추가 검사 등 카테고리 (문자열)
            
            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "dentalHistory_desc": "환자의 교정 치료, 보톡스, 물리치료 등",
                "clinic_history_desc": "환자의 턱관절장애 관련 과거 병력, 치료 이력, 발병 시기 및 계기 등",
                "factor_habbit": "환자의 음식 섭취 습관, 수면 자세, 이 악물기 등",
                "treat_plan": "물리치료, 약물요법, 장치치료, 보톡스 주사 등"
            }}]"""
    
    @staticmethod
    def cc_severity_prompt(texts):
        """CC 심각도 관련 프롬프트"""
        return f"""
            환자의 턱관절 통증 정도 정보입니다. 다음 텍스트를 분석하여 JSON 형식으로 분류해주세요.
            
            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. severity: 통증/증상 강도 (1-5, 없으면 null)
            2. vas: vas로 기재되어 있는 통증 점수. (int, 없으면 null)
            3. duration: 지속 기간 (명시된 경우만, 문자열)
            
            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "severity": "숫자 또는 null",
                "vas": "숫자 또는 null",
                "duration": "기간 또는 null"
            }}]"""


class TreatmentPrompts:
    """치료 관련 프롬프트"""
    
    @staticmethod
    def medication_prompt(texts):
        """약물 복용 분류 프롬프트"""
        return f"""다음 약물 복용 관련 텍스트들을 분석하여 JSON 형식으로 분류해주세요.

            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. medication_type: 약물 종류 (진통제/소염제/근이완제 등)
            2. frequency: 복용 빈도 ('regular': 정기적, 'occasional': 간헐적, 'none': 미복용)
            3. duration: 복용 기간 (명시된 경우만)
            4. compliance: 복약 순응도 ('good': 양호, 'fair': 보통, 'poor': 불량)

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "medication_type": "약물 종류",
                "frequency": "복용 빈도",
                "duration": "기간 또는 null",
                "compliance": "순응도"
            }}]"""

    @staticmethod
    def device_prompt(texts):
        """장치 사용 분류 프롬프트"""
        return f"""다음 장치 사용 관련 텍스트들을 분석하여 JSON 형식으로 분류해주세요.

            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. device_type: 장치 종류
            2. usage_pattern: 사용 패턴 ('constant': 상시착용, 'partial': 부분착용, 'rare': 거의미착용)
            3. duration: 사용 기간
            4. compliance: 착용 순응도 ('good': 양호, 'fair': 보통, 'poor': 불량)

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "device_type": "장치 종류",
                "usage_pattern": "사용 패턴",
                "duration": "기간 또는 null",
                "compliance": "순응도"
            }}]"""
    
    @staticmethod
    def habit_prompt(texts):
        """습관 분류 프롬프트"""
        return f"""다음 습관 관련 텍스트들을 분석하여 JSON 형식으로 분류해주세요.

            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. habit_type: 습관 종류 (이갈이/편측성저작 등)
            2. frequency: 빈도 ('high': 매일/자주, 'medium': 가끔, 'low': 거의없음)
            3. awareness: 인지여부 ('aware': 인지, 'unaware': 미인지)
            4. improvement: 개선여부 ('improved': 개선, 'unchanged': 유지, 'worsened': 악화)

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "habit_type": "습관 종류",
                "frequency": "빈도",
                "awareness": "인지여부",
                "improvement": "개선여부"
            }}]"""


class TherapyPrompts:
    """물리치료 관련 프롬프트"""
    
    @staticmethod
    def hot_pack_prompt(texts):
        """찜질 분류 프롬프트"""
        return f"""다음 찜질 관련 텍스트들을 분석하여 JSON 형식으로 분류해주세요.

            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. status: 찜질 시행 여부 (0: 미시행, 1: 시행)
            2. frequency: 시행 빈도 ('high': 매일/자주, 'medium': 주 2-3회, 'low': 주 1회 이하)
            3. duration: 시행 시간 (분 단위 정수, 명시되지 않은 경우 null)
            4. method: 찜질 방법 ('hot': 온찜질, 'cold': 냉찜질, 'both': 둘 다, null: 불명확)

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "status": 0 또는 1,
                "frequency": "빈도",
                "duration": 숫자 또는 null,
                "method": "방법"
            }}]"""

    @staticmethod
    def massage_prompt(texts):
        """마사지/스트레칭 분류 프롬프트"""
        return f"""다음 마사지/스트레칭 관련 텍스트들을 분석하여 JSON 형식으로 분류해주세요.

            각 텍스트에 대해 다음 정보를 추출해주세요:
            1. type: 종류 ('massage': 마사지, 'stretching': 스트레칭, 'both': 둘다)
            2. frequency: 시행 빈도 ('high': 매일/자주, 'medium': 주 2-3회, 'low': 주 1회 이하)
            3. duration: 시행 시간 (분 단위 정수, 명시되지 않은 경우 null)
            4. method: 방법 ('self': 자가, 'professional': 전문가, 'both': 둘다)

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "type": "종류",
                "frequency": "빈도",
                "duration": 숫자 또는 null,
                "method": "방법"
            }}]"""


class PresentIllnessPrompts:
    """현재 질환(PI) 관련 프롬프트"""
    
    @staticmethod
    def pi_basic_info_prompt(texts):
        """PI 기본 정보 분류 프롬프트"""
        return f"""
            다음은 턱관절장애(TMJ) 및 저작근 장애에 대한 진료 기록(PI 텍스트)입니다.
            문서에는 K07.65(퇴행성 관절염), K07.66(저작근의 장애), K07.63(턱관절 통증) 등의 진단 코드가 포함될 수 있습니다.

            아래 텍스트를 분석하여, 다음 필드를 JSON 형식으로 추출해주세요:

            1. onset (발현 시기)  
            - 예: "3개월 전", "2023년 1월", "발병 시기 미상"  
            - 텍스트에서 구체적으로 언급된 경우만 추출하고, 없으면 `""`(빈 문자열)

            2. pattern (증상 양상)  
            - "constant" (지속성), "intermittent" (간헐성), "progressive" (점진적 악화)  
            - 명확히 언급된 경우에만 지정. 없으면 `""`

            3. aggravating_factors (악화 요인 목록, 배열)  
            - 예: ["딱딱한 음식", "스트레스", "이 악물기"]  
            - 여러 개라면 배열에 순서대로 담고, 없으면 `[]`

            4. status (현재 상태)  
            - "improving" (호전), "unchanged" (변화 없음), "worsening" (악화)  
            - 명시되지 않으면 `""`

            5. PI_diagnosis_jojint (턱관절 진단 내용, 문자열)  
            - K07.65 퇴행성 관절염, K07.63 턱관절 통증, K07.66 저작근 장애 등 진단명  
            - 예: "퇴행성 관절염 (K07.65)"

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "onset": "",
                "pattern": "",
                "aggravating_factors": [],
                "status": "",
                "PI_diagnosis_jojint": ""
            }}]
            """
    
    @staticmethod
    def pi_examination_prompt(texts):
        """PI 검사 및 치료 정보 프롬프트"""
        return f"""
            다음은 턱관절장애(TMJ) 및 저작근 장애에 대한 진료 기록(PI 텍스트)입니다.
            아래 텍스트를 분석하여, 다음 필드를 JSON 형식으로 추출해주세요:

            1. TMJ_PI_desc (진단/검사 항목, 배열)  
            - 파노라마, CT, 측두하악장애분석검사, 초음파, T-scan 등 실시된 검사 이름을 배열로 적습니다.  
            - 예: ["파노라마", "Cone Beam CT"]

            2. TMJ_PI_treatment (물리치료 항목, 배열)  
            - 분사신장치료, 전기자극치료, 복합자극치료, 물리치료 등  
            - 예: ["측두하악관절자극요법-단순", "분사신장치료"]

            3. drug_treatment (약물치료 항목, 배열)  
            - 예: ["소론도정(프레드니솔론)", "페리슨정(에페리손염산염)"]  
            - 복용 방법, 용량, 횟수 등은 이 필드가 아닌 별도 필드에 기입

            4. closing_dentalgear_desc (교합치료 항목, 배열)  
            - 교합안정장치(Splint), 교합조정, 보톡스(교합개선 목적) 등 교합 관련 치료가 있으면 적습니다.  
            - 없으면 `[]`

            5. PI_check (경과관찰 항목, 배열)  
            - "증상 체크 [2주후]", "1개월 후 재내원", "재평가 예정" 등 주기적 검진/재평가 계획  
            - 예: ["증상 ck [2주후]"]

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "TMJ_PI_desc": [],
                "TMJ_PI_treatment": [],
                "drug_treatment": [],
                "closing_dentalgear_desc": [],
                "PI_check": []
            }}]
            """
    
    @staticmethod
    def pi_treatment_details_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 턱관절장애(TMJ) 및 저작근 장애에 대한 진료 기록(PI 텍스트)입니다.
            아래 텍스트를 분석하여, 다음 필드를 JSON 형식으로 추출해주세요:

            1. physical_therapy (저작근 장애(K07.66) 물리치료 등, 문자열)  
            - 저작근 장애를 치료하기 위해 시행된 물리치료나 자극요법(단순/전기/복합), 분사신장치료 등의 종합 요약  
            - 예: "측두하악관절 단순/전기/복합 자극, 분사신장치료"

            2. occlusal_treatment (교합안정장치(Splint) 등 장치치료, 문자열)  
            - 예: "APS, SS 장치 장착 및 조정"  
            - 교합 조정, 장치 제작 등

            3. medication_prescription (약물 처방 상세, 문자열)  
            - "페리슨정(에페리손염산염) 1/1회/14일 :: 취침 직전 복용" 처럼, 복용 용법/횟수/기간 등을 구체적으로 적습니다.  
            - 여러 개라면 문장으로 나열  
            - 예: "페리슨정(에페리손염산염) - 1/1회/14일, 소론도정(프레드니솔론) - 1/1회/14일"

            4. other_treatment (그 외 보톡스 시술, 악관절 강세척술, 교합조정, 발치 등, 문자열)  
            - "보톡스 시술", "악관절 세척술" 등  
            - 텍스트에서 확인되면 구체적으로 작성, 없으면 `""`

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "physical_therapy": "",
                "occlusal_treatment": "",
                "medication_prescription": "",
                "other_treatment": ""
            }}]
            """
    
    @staticmethod
    def pi_drug_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 약물의 종류입니다.
            - 페리슨정(에페리손염산염),소론도정(프레드니솔론),리보트릴정(클로나제팜),세크로정(아세클로페낙),휴모리드정5mg(모사프리드시트르산염수화물),뉴론틴캡슐300밀리그램(가바펜틴),알마겔정,휴모리드정,디푸루칸건조시럽(플루코나졸),리보트릴정,뉴론틴캡슐,세크로정,페리슨정,소론도정,디푸루칸건조시럽,영진멜라토닌서방정,쎄레브렉스캡슐100밀리그램(세레콕시브),아목클정,테그레톨정200밀리그램,뉴론틴캡슐300밀리그램,아목클정625밀리그램,아목클정625밀리그램(아목시실린·클라불란산칼륨),휴온스아목시크라정625밀리그램,알마겔정(알마게이트),살라겐정(필로카르핀염산염),뉴론틴정600밀리그램(가바펜틴),아목사정625밀리그램(아목시실린수화물-클라불란산칼륨),휴모리드정(모사프리드시트르산염수화물),타이레놀8시간이알서방정(아세트아미노펜)
            
            아래 텍스트를 분석하여, 다음 필드를 JSON 형식으로 추출해주세요:

            1. pi_drug_specise (약 이름 유사할 시 전달한 예시로 대체 , 문자열)  
            아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            유사한 단어가 없다면 빈 문자열로 추출합니다.
            여러가지가 등장한다면 콤마로 구분합니다.
            - 약 종류 기재
            - 예: "소론도정(프레드니솔론)"

            2. pi_drug_term (복용 주기. 주 단위 n회 기재, 정수형)
            - 복용 주기 기재
            - 예: 3

            3. pi_drug_total_time (복용 기간 기재. 범위일 시, 최장 기간 기재, 정수형)
            - 복용 기간 기재
            - 예: 30

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_drug_specise": "",
                "pi_drug_term": "",
                "pi_drug_total_time": "",
            }}]
            """
    
    @staticmethod
    def pi_occulusal_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 교합 치료 장치 종류입니다.
            - APS,SS Splint,APS Splint,이갈이장치,코골이장치
            아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            유사한 단어가 없다면 빈 문자열로 추출합니다.
            여러가지가 등장한다면 콤마로 구분합니다.
            다음 필드를 JSON 형식으로 추출해주세요:

            1. pi_occ_specise (약 이름 유사할 시 전달한 예시로 대체 , 문자열)  
            - 장치 및 처치 종류 기재
            - 예: "Splint"

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_occ_specise": ""
            }}]
            """
    
    @staticmethod
    def pi_physical_therapy_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 물리 치료 종류입니다.
            - 두하악관절 단순,전기,분사신장치료,복합자극,복합자극요법,악관절고착해소술,악관절 고착 해소술,물리치료,초음파치료	

            아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            유사한 단어가 없다면 빈 문자열로 추출합니다.
            여러가지가 등장한다면 콤마로 구분합니다.
            다음 필드를 JSON 형식으로 추출해주세요:

            1. pi_physical_therapy (약 이름 유사할 시 전달한 예시로 대체 , 문자열)  
            - 장치 및 처치 종류 기재
            - 예: "Splint"

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_physical_therapy": ""
            }}]
            """
    
    @staticmethod
    def pi_next_schedule_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 다음 내원 주기 및 증상 체크 내용입니다.
            - 증상 체크 : 증상 ck, 장치 ck, 근육두께 ck, 물리치료, x-ray, 재평가
            - 내원 예정 : 1개월 후, 2주 후, 1주 후
            다음 필드를 JSON 형식으로 추출해주세요:

            1. pi_next_schedule (다음 내원 예정일, 정수형)  
            - 텍스트 내 내원 예정 내용을 추출하여 days 단위로 변환해 기재해 주세요
            - 예: 7

            2. pi_next_ck (다음 내원시 증상 체크, 문자형)  
            - 아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            - 예: 근육두께ck

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_next_schedule": "",
                "pi_next_ck": "",
            }}]
            """
    
    @staticmethod
    def pi_next_schedule_prompt(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 다음 내원 주기 및 증상 체크 내용입니다.
            - 증상 체크 : 증상 ck, 장치 ck, 근육두께 ck, 물리치료, x-ray, 재평가
            - 내원 예정 : 1개월 후, 2주 후, 1주 후
            다음 필드를 JSON 형식으로 추출해주세요:

            1. pi_next_schedule (다음 내원 예정일, 정수형)  
            - 텍스트 내 내원 예정 내용을 추출하여 days 단위로 변환해 기재해 주세요
            - 예: 7

            2. pi_next_ck (다음 내원시 증상 체크, 문자형)  
            - 아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            - 예: 근육두께ck

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_next_schedule": "",
                "pi_next_ck": "",
            }}]
            """
    
    @staticmethod
    def pi_aggravating_factors(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 악화 요인에 대한 내용입니다. 악화 요인에는 아래의 요소가 존재합니다.
            - 딱딱한 음식,이 악물기,스트레스,찬 음식,단 음식
            
            아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            유사한 단어가 없다면 빈 문자열로 추출합니다.
            여러가지가 등장한다면 콤마로 구분합니다.
            다음 필드를 JSON 형식으로 추출해주세요:
            

            1. pi_aggravating_factors (악화 요인, 문자열)  
            - 예: 딱딱한 음식

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_aggravating_factors": ""
            }}]
            """
    
    @staticmethod
    def pi_TMJ_PI_desc(texts):
        """PI 치료 상세 정보 프롬프트"""
        return f"""
            다음은 본 문서에 등장하는 악화 요인에 대한 내용입니다. 악화 요인에는 아래의 요소가 존재합니다.
            - 딱딱한 음식,이 악물기,스트레스,찬 음식,단 음식
            
            아래 텍스트를 분석하여 위의 용어가 등장한다면 추출해주세요. 유사한 단어가 있다면 위 예시로 대체합니다.
            유사한 단어가 없다면 빈 문자열로 추출합니다.
            여러가지가 등장한다면 콤마로 구분합니다.
            다음 필드를 JSON 형식으로 추출해주세요:
            

            1. pi_aggravating_factors (악화 요인, 문자열)  
            - 예: 딱딱한 음식

            텍스트 목록:
            {texts}

            다음 JSON 형식으로 응답해주세요:
            [{{
                "pi_aggravating_factors": ""
            }}]
            """
            
class NumericPrompts:
    """교합 관련 데이터 추출 프롬프트"""
    
    @staticmethod
    def extract_occlusion_data(texts):
        """교합 데이터 추출 프롬프트"""
        return f"""다음 구강 교합 관련 텍스트들을 분석하여 각 케이스별로 교합 정보를 JSON 형식으로 추출해주세요.

        각 텍스트에 대해 다음 정보를 추출해주세요:
        1. occlusion_rt_number: 오른쪽(Rt) 교합 시 닿는 이빨 갯수 (0-4 사이의 정수)
        - 4,5,6,7번 치아가 교합에 참여하는지 확인
        - "4567"과 같이 표시된 경우 4개
        - "567"과 같이 표시된 경우 3개
        - "67"과 같이 표시된 경우 2개
        - 치아가 없거나 완전히 안 닿는 경우 0

        2. occlusion_lt_number: 왼쪽(Lt) 교합 시 닿는 이빨 갯수 (0-4 사이의 정수)
        - 위와 동일한 규칙 적용

        3. occlusion_rt_intensity: 오른쪽 교합 강도 (0-2 사이의 정수)
        - 0: "안닿음", "뜸", "open bite" 등 교합이 없는 경우
        - 1: "살짝 닿음", "약하게", "약함", "덜 닿음" 등 교합이 약한 경우
        - 2: 정상 교합 또는 강도에 대한 언급이 없는 경우

        4. occlusion_lt_intensity: 왼쪽 교합 강도 (0-2 사이의 정수)
        - 위와 동일한 규칙 적용

        텍스트 분석 시 주의사항:
        - "Both", "both"는 양쪽 모두를 의미합니다.
        - "Lt", "LT", "lt", "왼쪽", "좌측"은 왼쪽을 의미합니다.
        - "Rt", "RT", "rt", "오른쪽", "우측"은 오른쪽을 의미합니다.
        - 괄호 안의 내용(예: "(Lt 45덜닿음>더 닿음)")도 고려하세요.
        - 특정 치아가 언급되지 않은 경우, 해당 방향의 전체 교합 상태를 고려하세요.
        - 텍스트에 치아 번호만 언급되고 강도가 명시되지 않은 경우 강도는 2로 간주합니다.
        - 빈 문자열이나 "n/s", "nan", "-" 등의 경우 모든 값을 null로 처리합니다.

        예시 분석:
        1. "4567/4567 (우측 6,7 긴밀하진 않음)" -> {{
        "occlusion_rt_number": 4, 
        "occlusion_lt_number": 4, 
        "occlusion_rt_intensity": 1, 
        "occlusion_lt_intensity": 2
        }}

        2. "오른쪽 4,5 안닿음" -> {{
        "occlusion_rt_number": 2, 
        "occlusion_lt_number": 4, 
        "occlusion_rt_intensity": 0, 
        "occlusion_lt_intensity": 2
        }}

        3. "Lt) 45 안 닿음/ Rt 3번 약하게 닿음" -> {{
        "occlusion_rt_number": 4, 
        "occlusion_lt_number": 2, 
        "occlusion_rt_intensity": 1, 
        "occlusion_lt_intensity": 0
        }}

        4. "왼쪽 4,5 안 닿음 -> 교합지 상에서" -> {{
        "occlusion_rt_number": 4, 
        "occlusion_lt_number": 2, 
        "occlusion_rt_intensity": 2, 
        "occlusion_lt_intensity": 0
        }}

        5. "both 4567" -> {{
        "occlusion_rt_number": 4, 
        "occlusion_lt_number": 4, 
        "occlusion_rt_intensity": 2, 
        "occlusion_lt_intensity": 2
        }}

        6. "BOTH 4567 OPEN BITE 경향" -> {{
        "occlusion_rt_number": 4, 
        "occlusion_lt_number": 4, 
        "occlusion_rt_intensity": 1, 
        "occlusion_lt_intensity": 1
        }}

        다음 텍스트들에 대해 분석해주세요:
        {texts}

        다음 JSON 형식으로 응답해주세요:
        [{{
            "occlusion_rt_number": 숫자 또는 null,
            "occlusion_lt_number": 숫자 또는 null,
            "occlusion_rt_intensity": 숫자 또는 null,
            "occlusion_lt_intensity": 숫자 또는 null
        }}]"""