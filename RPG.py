import streamlit as st
import random

# --- ページ構成の蹂躙 ---
st.set_page_config(page_title="星霜の継承", page_icon="⏳")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d !important; }
    h1, h2, h3, p, div { color: #e0e0e0 !important; }
    div[data-testid="stAudio"], audio { display: none !important; visibility: hidden !important; }
    
    div.stButton > button {
        background-color: #1a1a2e !important; color: #ff4d4d !important;
        border: 2px solid #ff4d4d !important; border-radius: 0px !important;
        font-family: 'Courier New', Courier, monospace;
    }
    div.stButton > button:hover { background-color: #ff4d4d !important; color: #1a1a2e !important; cursor: crosshair; }
    </style>
    """, unsafe_allow_html=True)

# --- 音楽---
st.components.v1.html("""
    <script>
        var audio = new Audio('/app/static/Terminal_Equilibrium.mp3');
        audio.loop = true;
        window.parent.document.body.addEventListener('click', function() {
            audio.play().then(() => { console.log("旋律解禁"); });
        }, { once: true });
    </script>
""", height=0)

# --- 初期状態 ---
if 'page' not in st.session_state: st.session_state.page = "title"
if 'magic_stone' not in st.session_state: st.session_state.magic_stone = 200
if 'skill_cooldown' not in st.session_state: st.session_state.skill_cooldown = 0
if 'weapon' not in st.session_state:
    st.session_state.weapon = "素手"
    st.session_state.atk = 5
    st.session_state.enemy_hp = 100
    st.session_state.log = ["面接官が虚空を見つめている..."]
    st.session_state.character = "なし"

# --- データ定義 ---
ARMORY = {
    "素手": {"atk": 5}, "機械の手": {"atk": 30}, "刀": {"atk": 45},
    "星霜の双剣": {"atk": 60}, "錬金の瓶": {"atk": 20}, "暗黒の杖": {"atk": 35},
    "ゴミの棒": {"atk": 10}, "時間の短剣": {"atk": 25}, "聖なる杖": {"atk": 40},
    "終焉の知識": {"atk": 5}, "聖剣": {"atk": 500}, "バグ": {"atk": 666}
}

CHARACTERS = {
    "始まりの旅人": {"icon": "🚶", "cost": 0, "weapon": "素手", "atk_bonus": 0, "skill": "本気の攻撃", "dmg": 30},
    "星霜の旅人": {"icon": "⏳", "cost": 100, "weapon": "星霜の双剣", "atk_bonus": 35, "skill": "双剣乱舞", "dmg": 85},
    "samurai": {"icon": "🗡️", "cost": 75, "weapon": "刀", "atk_bonus": 20, "skill": "精神統一", "dmg": "BUFF_ATK_2x"},
    "狂気の錬金術師": {"icon": "⚗️", "cost": 400, "weapon": "錬金の瓶", "atk_bonus": 5, "skill": "理性の回復", "dmg": "HEAL_HP"},
    "時間の盗賊": {"icon": "⏰", "cost": 3000, "weapon": "時間の短剣", "atk_bonus": 10, "skill": "時止め", "dmg": "STUN_3T"},
    "聖者": {"icon": "👼", "cost": 5000, "weapon": "聖なる杖", "atk_bonus": 25, "skill": "神の慈悲", "dmg": "REFLECT_50"},
    "暗黒の魔法使い": {"icon": "🧙‍♂️", "cost": 700, "weapon": "暗黒の杖", "atk_bonus": 10, "skill": "煉獄", "dmg": 2256},
    "終焉の支配者": {"icon": "👑", "cost": 7000, "weapon": "終焉の知識", "atk_bonus": 10, "skill": "終焉の宣告", "dmg": 989001},
    "聖剣の勇者": {"icon": "⚔️", "cost": 10000, "weapon": "聖剣", "atk_bonus": 1000, "skill": "世界消滅", "dmg": 9999999999999},
    "バグの亡霊": {"icon": "👻", "cost": 6666, "weapon": "バグ", "atk_bonus": 666, "skill": "スタックオーバーフロー", "dmg": "RANDOM_KILL"},
}

# --- 画面遷移 ---
if st.session_state.page == "title":
    st.title("⏳ 星霜の継承：異世界に生きる")
    if st.button("Embrace the Chaos"):
        st.session_state.page = "character_select"
        st.rerun()

elif st.session_state.page == "character_select":
    st.title("キャラ選択")
    cols = st.columns(3)
    for i, (name, data) in enumerate(CHARACTERS.items()):
        with cols[i % 3]:
            if st.session_state.magic_stone >= data["cost"]:
                if st.button(f"{data['icon']}\n{name}"):
                    st.session_state.character = name
                    st.session_state.weapon = data["weapon"]
                    st.session_state.atk = ARMORY[data["weapon"]]["atk"] + data["atk_bonus"]
                    st.session_state.page = "game"
                    st.rerun()
            else:
                st.button(f"🔒 {name}", disabled=True)

elif st.session_state.page == "game":
    st.title("⚔️ 蹂躙の戦場")
    char = CHARACTERS[st.session_state.character]
    st.subheader(f"面接官の理性(HP): {st.session_state.enemy_hp}")
    st.write(f"キャラ: {st.session_state.character} / 威力: {st.session_state.atk}")

    if st.session_state.skill_cooldown > 0:
        st.sidebar.warning(f"必殺技チャージ中: あと {st.session_state.skill_cooldown} ターン")

    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("蹂躙攻撃を開始する！"):
            dmg = st.session_state.atk + random.randint(1, 10)
            st.session_state.enemy_hp -= dmg
            st.session_state.log.append(f"攻撃！{dmg} のダメージを与えた！")
            
            if 'skill_cooldown' in st.session_state and st.session_state.skill_cooldown > 0:
                st.session_state.skill_cooldown -= 1
            st.rerun()
                
    with c2:
        cd = st.session_state.get('skill_cooldown', 0)
        can_use = (cd == 0)
        btn_label = f"⚡ 必殺！{char['skill']}" if can_use else f"⚡ チャージ中({cd})"
        
        if st.button(btn_label, disabled=not can_use):
            dmg = char['dmg']
            if dmg == "BUFF_ATK_2x":
                st.session_state.atk *= 1.7
                st.session_state.log.append("精神統一完了！攻撃力が1.7倍に増幅された！")
            elif dmg == "STUN_3T":
                st.session_state.enemy_stunned = 3
                st.session_state.log.append("時が止まった...！相手は無防備だ！！")
            elif dmg == "RANDOM_KILL":
                if random.random() < 0.3:
                    st.session_state.enemy_hp = 0
                    st.session_state.log.append("バグが爆発！面接官が強制終了させられた！")
                else:
                    st.session_state.log.append("バグは不発だった...無情だ...")
            elif isinstance(dmg, int):
                st.session_state.enemy_hp -= dmg
                st.session_state.log.append(f"『{char['skill']}』発動！！ {dmg} の確定ダメージ！")
            
            st.session_state.skill_cooldown = 10
            st.rerun()

    if st.session_state.enemy_hp <= 0:
        st.balloons()
        st.session_state.enemy_hp = 100
        st.session_state.skill_cooldown = 0
        st.session_state.log.append("！！！蹂躙完了！！！面接官は再起動した...")
        st.rerun()
          
    for entry in reversed(st.session_state.log):
        st.write(entry)