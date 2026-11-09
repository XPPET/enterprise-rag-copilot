import os
import streamlit as st
from rag_engine import query_copilot, index_uploaded_pdf, collection

st.set_page_config(
    page_title="EY Enterprise AI Copilot",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #FFE600; margin-bottom: 0px; }
    .subtitle { font-size: 1.05rem; color: #8F9CA3; margin-bottom: 1.5rem; }
    .risk-high { background-color: rgba(255, 75, 75, 0.15); border-left: 5px solid #FF4B4B; padding: 10px; border-radius: 4px; margin-bottom: 8px; }
    .risk-med { background-color: rgba(255, 170, 0, 0.15); border-left: 5px solid #FFAA00; padding: 10px; border-radius: 4px; margin-bottom: 8px; }
    .risk-low { background-color: rgba(0, 204, 150, 0.15); border-left: 5px solid #00CC96; padding: 10px; border-radius: 4px; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💼 Enterprise AI Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI & Process Automation | Audit, Financial Analysis & Risk Flags</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.3], gap="large")

with col_left:
    st.subheader("📁 Ανέβασμα Εταιρικού Εγγράφου")
    uploaded_file = st.file_uploader("Επίλεξε εταιρικό PDF (Ισολογισμός, 10-K, ESG, Πολιτική):", type=["pdf"])

    if uploaded_file is not None:
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
            os.makedirs("./data", exist_ok=True)
            save_path = os.path.join("./data", uploaded_file.name)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("⏳ Επεξεργασία & δημιουργία Vector Embeddings..."):
                chunks_added = index_uploaded_pdf(save_path, uploaded_file.name)
                st.session_state.last_uploaded = uploaded_file.name
                st.success(f"Το αρχείο '{uploaded_file.name}' καταχωρήθηκε επιτυχώς ({chunks_added} αποσπάσματα στο ChromaDB)!")

    st.markdown("---")
    st.subheader("📝 Ερώτημα Στελέχους")
    default_prompt = "Ποια είναι τα βασικά οικονομικά ευρήματα, ποιοι γεωπολιτικοί κίνδυνοι αναφέρονται και ποιες ενέργειες προτείνονται;"
    user_query = st.text_area("Γράψε την ερώτηση:", value=default_prompt, height=110)
    
    run_btn = st.button("🚀 Ανάλυση & Σύνθεση Αναφοράς", use_container_width=True, type="primary")
    st.caption(f"📊 Ενεργά chunks στη βάση δεδομένων: **{collection.count()}**")

with col_right:
    if run_btn and user_query:
        with st.spinner("🔍 Σημασιολογική αναζήτηση στα έγγραφα & σύνθεση executive report..."):
            try:
                res = query_copilot(user_query)
                st.session_state["latest_report"] = res

                st.subheader("📌 Executive Summary")
                st.info(res.executive_summary)

                tab1, tab2, tab3 = st.tabs(["📊 Βασικά Ευρήματα", "⚠️ Risk Matrix", "🎯 Action Items"])

                with tab1:
                    for item in res.detailed_findings:
                        st.markdown(f"- {item}")

                with tab2:
                    for risk in res.risk_flags:
                        lvl = risk.risk_level.upper()
                        css_class = "risk-high" if lvl == "HIGH" else "risk-med" if lvl == "MEDIUM" else "risk-low"
                        st.markdown(f'<div class="{css_class}"><strong>[{lvl} RISK]</strong> {risk.description}</div>', unsafe_allow_html=True)

                with tab3:
                    for act in res.action_items:
                        st.checkbox(act, value=False)

                st.markdown("---")
                st.subheader("📑 Τεκμηρίωση Πηγών (Audit Trail)")
                for idx, cit in enumerate(res.citations):
                    with st.expander(f"Πηγή #{idx+1}: {cit.document_name} (Σελίδα {cit.page_number})"):
                        st.caption(f'"{cit.quote}"')

                # Export Report
                report_md = f"# Executive Briefing Report\n\n## 1. Executive Summary\n{res.executive_summary}\n\n## 2. Key Findings\n"
                for item in res.detailed_findings:
                    report_md += f"- {item}\n"
                report_md += "\n## 3. Risk Matrix\n"
                for risk in res.risk_flags:
                    report_md += f"- **[{risk.risk_level}]**: {risk.description}\n"
                report_md += "\n## 4. Recommended Actions\n"
                for act in res.action_items:
                    report_md += f"- [ ] {act}\n"
                report_md += "\n## 5. Audit Trail & Citations\n"
                for cit in res.citations:
                    report_md += f"- **Doc:** {cit.document_name} (p. {cit.page_number})\n  > \"{cit.quote}\"\n"

                st.download_button(
                    label="📥 Λήψη Executive Report (Markdown)",
                    data=report_md,
                    file_name="executive_summary_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Σφάλμα κατά την εκτέλεση: {e}")