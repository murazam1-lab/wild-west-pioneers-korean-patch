# Wild West Pioneers 한국어 번역 지침 (4차 전면 검수)

게임: 서부 개척 시대 마을 건설 시뮬레이션. 플레이어는 잭 모건(Jack Morgan). 주민들은 플레이어를 "Boss"라고 부름.
기존 번역은 기계번역(quickmt) + 일부 수동 수정본이라 직역투·오역·태그 위치 오류가 많다. 목표는 **한국 게임에 정식 출시된 듯한 자연스러운 한국어**.

## 1. 절대 규칙 (검사 스크립트가 오류로 잡음)
- `<sprite name="...">` 태그는 개수·이름 그대로 유지(아이콘 이미지). 이름 오타 2개만 예외 자동 허용.
- `{[Var]}`, `{Var}` 변수는 글자 그대로 유지. 변수 이름 번역 금지.
- `<br>` 개수는 원문과 동일. 원문 `\n`(줄바꿈) 개수도 가급적 동일.
- `<b>`, `<i>`, `<color=...>` 등 서식 태그는 원문과 같은 개수, 올바르게 짝을 맞추기. **강조 대상인 한국어 단어를 감싸도록** 위치 재배치. `<b><b>` 중첩·빈 `<b></b>` 금지.
  - 원문 태그가 깨져 있으면(예: `<b>Trading<b>`) 한국어에서는 올바르게 짝을 맞춰도 됨.
- `<align="justified">` 같은 태그가 문장 맨 앞이면 한국어에서도 맨 앞.
- 숫자·퍼센트·수치는 원문과 동일.
- 빈 번역 금지(원문이 빈 문자열인 항목은 이미 제외됨).

## 2. 문체
- **UI 레이블/버튼/제목**: 짧은 명사형. 예) "Send Feedback" → "의견 보내기", "Demolish" → "철거".
- **설명/툴팁/도움말(FAQ)/튜토리얼 설명**: 합니다체(~합니다/~됩니다). 지시는 "~하세요". "~하십시오"는 쓰지 않음.
- **퀘스트 목표(OBJ)·업적 설명·이정표 목표**: 명사형 종결. 예) "Gather Cattle" → "소 모으기", "Build a few Tents" → "천막 여러 채 건설", "Talk to Bill" → "빌과 대화". "~하라", "~하십시오" 금지.
- **효과 문구**: 짧은 명사형 + 마침표. 예) "건물 생산량 10% 증가."
- **대사(Dialogue, BARK, POPUP_DES 속 인물 대사, CutScenes)**: 인물 성격에 맞춘 자연스러운 구어체. 서부극 느낌 OK.
  - 주민·부하가 플레이어에게: 존댓말(~요). "Boss" → **"대장"**.
  - 도적·거친 인물: 반말/거친 말투 가능. 노인·사제: 점잖은 말투.
  - 같은 인물의 말투는 한 퀘스트 안에서 일관되게.
- **플레이어 선택지 버튼(POPUP_BUTTON)**: 플레이어(잭)의 대사로 자연스럽게. 예) "I will help you" → "도와드리죠." / "What do you mean?" → "무슨 뜻이죠?"
  - 선택지 설명(BUTTON_..._DES) "Contract accepted: ..." → "계약 수락: ...", "Contract rejected: ..." → "계약 거절: ..."
- 팝업 질문 "What do you want to do?" (플레이어 결정) → "어떻게 하시겠습니까?"
- **"당신" 최소화**. 주어 생략, "대장", "이 정착지" 등으로 자연스럽게. "당신의 정착지" → "정착지".
- 직역투 제거: "~에 의해", "~를 위한 ~", "그것은/그들은", "~하는 것이 가능합니다", "~할 수 있습니다"의 남발, 불필요한 "우리는/우리의".
- 띄어쓰기·맞춤법 정확히(예: "할 수있는" ✗ → "할 수 있는", "되었습니다." ✓, "됬" ✗). 마침표 앞 공백 금지.
- 영어 단어가 남아 있으면 안 됨(키 이름 등 고유 기술 용어 제외).
- 원문의 말장난·관용구는 의미가 통하는 한국어 표현으로.
- 원문이 개발용 문구("WIP - FULL RELEASE", "FULL RELEASE")면 "개발 중 · 정식 출시 예정" / "정식 출시 예정" 유지.

## 3. 조사 처리
- 아이콘(`<sprite>`)·변수(`{[X]}`) 바로 뒤에는 받침 따라 달라지는 조사(을/를, 이/가, 은/는, 으로/로, 과/와)를 피하도록 문장 구조를 바꿀 것.
  - 예) "Produces <sprite A> from <sprite B>." → "<sprite B>(으)로 <sprite A> 생산." ✗ → "<sprite B>에서 <sprite A> 생산." ✓ (에서/에/의/도/만/에게는 받침 무관)
  - 불가피하면 "을(를)", "이(가)" 병기.

## 4. 용어집 (반드시 통일)
### 건물
Town Hall 시청 / Big Town Hall 대형 시청 / Grand Town Hall 웅장한 시청 · Tent 천막 · Wooden Cabin 통나무집 · Brick House 벽돌집 · Warehouse 창고 · Loggers(') Cabin 벌목꾼 오두막 · Sawmill 제재소 · Hunters(') Cabin 사냥꾼 오두막 · Butcher 정육점 · Gatherers(') Hut 채집꾼 오두막 (Gatherers 단독 = 채집꾼 오두막/채집꾼) · Kitchen 주방 · Food Shop 식료품점 · Saloon 술집 · Sheriff's Office 보안관 사무소 · Well 우물 · Water Tank 물탱크 · Workers(') Camp 노동자 야영지 · Scouts(') Cabin 정찰대 오두막 · Settlers Base 이주민 기지 · Logistic(s) Center 물류 센터 · Post Office 우체국 · Brothel 유곽 · Corn Farm 옥수수 농장 · Cornfield 옥수수밭 · Grain Farm 곡물 농장 · Grainfield 곡물밭 · Potato Farm 감자 농장 · Potato Field 감자밭 · Vegetable Farm 채소 농장 · Herb Farm 약초 농장 · Herb Field 약초밭 · Cattle Ranch 소 목장 · Cattle Pasture 소 방목지 · Ranch 목장 · Barn 축사 · Slaughterhouse 도축장 · Windmill 풍차 방앗간 · Bakery 제빵소 · (Bourbon) Distillery (버번) 증류소 · Moonshiner(s)' Post / Moonshiners Outpost 밀주 제조소 · Canning Facility 통조림 공장 · Carpenter(s') Workshop / Carpenter 목공소 · Blacksmith 대장간 · Gold Mine 금광 · Gold Mine Project 금광 개발 사업 · Gold Refinery 금 제련소 · Placer Gold Miners 사금 채취장 · Stone Miners / Stone Quarry 채석장 · Mason(s) Workshop 석공 작업장 · Saltpeter Mine 초석 광산 · Dynamite Workshop 다이너마이트 작업장 · Church 교회 · Chapel 예배당 · Barbershop 이발소 · Bank 은행 · Coffeehouse 커피하우스 · Tailor's Workshop 재봉 작업장 · Tannery 무두질 작업장 · Drug Store 약국 · Hospital 병원 · Drug Workshop 의약품 작업장 · Specialists' Camp 전문가 야영지 · Newcomers Camp 새 이주민 야영지 · Base Fortification 기본 방벽 · Armored Fortification 보강 방벽 · Tower Fortification 감시탑 · Fortification 방어 시설 · Road 도로 · Main Road 주 도로 · Scaffolding 비계 · Decoration(s) 장식 · Outpost(s) (FAQ 분류) 현장 생산 건물 · Workshop(s) 작업장 · Service building 서비스 건물

### 자원
Wood 목재 · Log(s) 통나무 · Planks 판재 · Wooden Parts 목재 부품 · Gold 금 · Gold Ore 금광석 · Gold Bar(s) 금괴 · Money 돈 · Cash 현금 · Food 식량 · Raw Food 식재료 · Meat 고기 · Soup/Ration 수프 · Mushrooms 버섯 · Sausages 소시지 · Potatoes 감자 · Corn 옥수수 · Grain/Wheat 곡물 · Flour 밀가루 · Bread 빵 · Canned Food 통조림 · Bourbon 버번 · Moonshine 밀주 · Alcohol 술 · Hide 가죽 · Cattle 소 · Sheep 양 · Wool 양모 · Stone 석재 · Stone Chips 쇄석 · Stone Bricks 석재 벽돌 · Clay Lumps 점토 덩어리 · Clay Bricks 점토 벽돌 · Iron Ore 철광석 · Iron Bars 철괴 · Iron Parts 철제 부품 · Steel Bars 강철괴 · Steel Parts 강철 부품 · Coal 석탄 · Saltpeter 초석 · Dynamite 다이너마이트 · Rifles 소총 · Herb 약초 · Medicine 의약품 · Coffee Beans 커피콩 · Cotton 목화 · Linen 리넨 · Water 물 · Talent Points 재능 점수 · Journey Points 여정 점수 · Supplies 보급품

### 사람·집단
Pioneers (주민 자원/인구) 개척민 · "Pioneer" (플레이어 호칭) 개척자 · Settlers 이주민 · Residents/Citizens 주민 · Population 인구 · Workers 노동자 · Construction workers/Builders 건설 노동자 · Workforce 노동력 · Scouts 정찰대 · Expedition 원정대 · Caravan 교역단 · Trader/Merchant 상인 · Traveling(Travelling) Merchant 떠돌이 상인 · Bandit(s) 도적 / 도적단 (도둑·밴디트 ✗; Thief만 도둑) · Bandit leader/boss 도적 두목 · Natives 원주민 · Sheriff 보안관 · Officials 관리 · Specialist 전문가 · Priest 사제 · Pastor 목사 · Boss(플레이어 호칭) 대장 · Partner(호칭) 친구 · Folks 여러분/사람들

### 시스템
Idea(s) 아이디어 · Ideas Tree / Development Tree 아이디어 트리 / 발전 트리 · Talent 재능 · Trust 신뢰 · Satisfaction 만족도 · Whim(s) 요구 · Needs 필요 · Residents' Needs (건물 분류) 주민의 필요 · Contract 계약 · Quest 퀘스트 · Side Quest 부가 퀘스트 · Main Quest 메인 퀘스트 · Journey 여정 · Tier 단계 · Milestone 이정표 · World Map 세계 지도 · Settlement 정착지 (정착촌 ✗) · Range 범위/영향 범위 · Production cycle 생산 주기 · Upgrade 업그레이드 · Demolish 철거 · Journal 일지 · Guide 도움말 · Day 일차 · Gameplay Effects 게임 플레이 효과 · Soil Quality 토질 · Groundwater 지하수 · Homelessness 주거 부족 · Planning phase 배치 단계 · Level 레벨 · Lvl 2 → "2레벨" · Unlock 해금 · Reward 보상 · Deal 거래

### 지명 (StrategicMap)
Dust Creek **더스트크리크** · Sand Storm **샌드스톰**(정착지 이름. "모래 폭풍"은 실제 날씨일 때만) · Ghost Town 유령 마을 · Demolished Camp 파괴된 야영지 · Deaf Woodland 고요한 삼림 · Deaf Canyon 고요한 협곡 · Hidden Grove 숨겨진 숲 · Old Mine 오래된 광산 · Shrubby Glade 관목 숲터 · Pinewood Gulch 소나무 협곡 · Whispering Pines Camp 속삭이는 소나무 야영지 · Wolf Canyon 늑대 협곡 · Rosewood Clearing 로즈우드 공터 · Foxtrail Woodland 여우길 삼림 · Maple Hollow Junction 단풍 골짜기 갈림길 · Cedar Creek Hollow 시더크리크 골짜기 · Westwood Bar 웨스트우드 주점 · Wild Creek Cabin 와일드크리크 오두막 · Blackbark Ridge 블랙바크 능선 · Dustwind Flats 더스트윈드 평원 · Coyote Skull Mesa 코요테 해골 고원 · Rattlesnake Plain 방울뱀 평원 · Red Dune Crossing 붉은 모래언덕 교차로 · Deadman's Wash 망자의 계곡 · Lonely Vulture Peak 외로운 독수리 봉우리 · Whispering Sand Hollow 속삭이는 모래 골짜기 · Armadillo Springs 아르마딜로 스프링스 · Dust Devil Outskirts 더스트데빌 외곽 · Sunset Pass 해넘이 고개 · Scorpion's Edge 전갈 절벽 · Howling Wind Pass 울부짖는 바람 고개 · Bleakstone Desert 황량한 돌 사막 · Salt Trail Outpost 소금길 전초기지 · Hidden Laboratory 숨겨진 실험실 · Abandoned Laboratory 버려진 실험실 · Bandits' Camp 도적 야영지 · Bandits' Jail 도적 감옥 · Government Building 정부 건물 · Government Jail 정부 감옥 · the valley 계곡

### 인물
Jack Morgan 잭 모건 · Jesse (Tanner) 제시 (태너) · Glenn 글렌 · William Mercer 윌리엄 머서 · Margaret 마거릿 · Jed Holloway 제드 홀러웨이 · Gideon Pike 기디언 파이크 · June Redford 준 레드퍼드 · Lillian Hart 릴리언 하트 · Silas 사일러스 · Johnny 조니 · Hialeah 하이얼리아 · Smith (Pastor) 스미스 목사 · Stephan 스테판 · Mason (General Store Owner) 메이슨 (잡화점 주인) · Finn 핀 (식료품점 주인) · George 조지 · Jamie 제이미 · Thomas Jones / Agent Jones 토머스 존스 / 존스 요원 · Elijah 일라이자 (우체국장) · Arthur 아서 · Benjamin 벤저민 · Ben 벤 · Cornelia 코닐리아 · Wyatt 와이엇 · Texas Red 텍사스 레드 · Michael 마이클 · Bill 빌 · Dudu 두두 · Sasquatch 사스콰치 · Red Ghost 레드 고스트 · Narrator 내레이터 · Tlatoani 틀라토아니

### 퀘스트 제목 (다른 묶음에서도 참조되므로 반드시 이대로)
A Cow on the Roof 지붕 위의 소 · Band of Ghosts 유령 악단 · Beaver, Damn It! 망할 비버! · Bit Boring Here, Partner 여긴 좀 지루하군, 친구 · Blocked Passage 막힌 통로 · Breeder Problem 목장주의 고민 · Broken Business 꼬여버린 장사 · Cattle for Natives 원주민을 위한 소 · Church Holiday 교회 축일 · Debt owed 갚아야 할 빚 · End of Peace 평화의 끝 · Expensive Security 값비싼 안전 · First Contact 첫 만남 · Forever and After 영원히 함께 · Freedom 자유 · Government Orders 정부의 명령 · Government Trouble 정부와의 마찰 · Growing Family 늘어나는 식구 · Happy Residents 행복한 주민 · Haunted House 유령의 집 · Hunting for Sasquatch 사스콰치 사냥 · Lure for Customers 손님을 끄는 법 · Missing Hat 사라진 모자 · Moonshine Scandal 밀주 소동 · Mother-in-Law 장모님 · New Beginnings 새로운 시작 · On the Trail of Bandits 도적의 흔적을 따라 · Red Ghost 레드 고스트 · Retired Bandit 은퇴한 도적 · Secret Admirer 숨은 흠모자 · Spare change, boss? 대장, 잔돈 좀 있어요? · Suspicious Customer 수상한 손님 · The End of Bandits is Close 다가오는 도적의 최후 · The Lumberjack Saga 벌목꾼 이야기 · The Residents' Needs 주민의 필요 · Traveling Merchant 떠돌이 상인 · Unusual Priest 별난 사제 · Whack-a-Mole 두더지 잡기 · Where is My Father? 아버지는 어디에? · Gold Fever 황금 열풍 · Hidden Riches 숨겨진 보물 · Basic Resources 기본 자원 · Prison Break 탈옥 · Thanksgiving 추수감사절 · Halloween 핼러윈 · Alcohol License 주류 허가증 · Fortune in the Foundations 주춧돌 아래의 행운 · Settling the Frontier 변경 개척 · Settlers Expedition 이주민 원정대 · Scouting Expedition 정찰 원정 · Tough as a Rock 바위처럼 단단하게
