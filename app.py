import re
import streamlit as st

st.set_page_config(page_title="OLT Commands", page_icon="📡", layout="centered")

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 520px;}
    .label {font-size: 13px; color: #6b7280; margin: 14px 0 4px;}
    div[data-testid="stCodeBlock"] pre {
        background: #ffffff !important;
        border: 1px solid #eef0f3;
        border-radius: 12px;
    }
    div[data-testid="stCodeBlock"] code {color: #1f2937 !important;}
    button[data-baseweb="tab"] {font-size: 15px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### OLT Commands")

c1, c2 = st.columns(2)
pon = c1.number_input("Pon", min_value=0, value=1, step=1)
onu = c2.number_input("Onu", min_value=0, value=1, step=1)

rmac_raw = st.text_input("Router MAC (full)", placeholder="14EB-B66B-6EB3").strip()

digits = re.sub(r"[^0-9A-Fa-f]", "", rmac_raw).upper()
last4 = digits[-4:] if len(digits) >= 4 else ""
if digits:
    huawei_mac = "-".join(digits[i:i + 4] for i in range(0, len(digits), 4))
else:
    huawei_mac = ""

if last4:
    st.caption(f"Last 4 digit: {last4}")


def show(items):
    for name, cmd in items:
        st.markdown(f'<div class="label">{name}</div>', unsafe_allow_html=True)
        st.code(cmd, language="bash", wrap_lines=True)


tab1, tab2 = st.tabs(["BDCOM", "HUAWEI"])

with tab1:
    b_sn = st.text_input("ONU MAC / SN", placeholder="ECOM-9D03FF9B", key="b_sn").strip()

    show([
        ("Find Onu (ONU MAC)", f"show gpon onu-information sn {b_sn or '<ONU MAC>'}"),
        ("Find Onu (Router MAC)", f"show mac address-table | include {last4 or '<Router MAC>'}"),
        ("Onu Info", f"show gpon interface gpon 0/{pon}:{onu} onu basic-info"),
        ("Onu Power", f"show gpon interface gpon 0/{pon}:{onu} onu optical-transceiver-diagnosis"),
        ("Check Port", f"show gpon interface gpon 0/{pon}:{onu} onu port 1 state"),
        ("Reboot", f"gpon reboot onu interface gpon 0/{pon}:{onu}"),
        ("Mac Address Show", f"show mac address-table interface gpon 0/{pon}:{onu}"),
        ("Total Inactive Onu in PON", f"show gpon inactive-onu interface gpon 0/{pon}"),
        ("Total Losi in PON", f"show gpon inactive-onu interface gpon 0/{pon} | include losi"),
        ("All PON Status", "show interface brief"),
        ("PON Port Open Check", f"show interface range gpon 0/{pon}"),
    ])

with tab2:
    e1, e2 = st.columns([3, 1])
    h_raw = e1.text_input("ONU MAC ", placeholder="4577CE9A", key="h_sn").strip()
    h_sn = h_raw.split(":")[-1].strip().upper()
    slot = e2.number_input("Slot 0/_", min_value=0, value=1, step=1, key="h_slot")

    show([
        ("Find Onu (ONU MAC)", f"display ont info by-sn {h_sn or '<ONU MAC>'}"),
        ("Find Onu (Router MAC)", f"display location {huawei_mac or '<Router MAC>'}"),
        ("Onu Info", f"display ont optical-info {pon} {onu}"),
        ("Reset", f"ont reset {pon} {onu}"),
        ("Onu All Power", f"display ont optical-info history rx {pon} {onu}"),
        ("Total Inactive Onu in PON", f"display ont info summary {pon}"),
        ("Total Losi in PON", f"display ont info summary {pon} | include LOSi/LOBi"),
        ("Total Offline Onu in PON", f"display ont info summary {pon} | include offline"),
        (
            "Port Check (interface theke ber hoye)",
            f"quit\ninterface gpon 0/{slot}\ndisplay ont port state {pon} {onu} eth-port all",
        ),
    ])
