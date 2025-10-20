import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="AI Brand Monitoring Calculator",
    page_icon="🔍",
    layout="wide"
)

# Dati dei piani Otterly.ai
PLANS = {
    "Lite": {
        "price_monthly": 29,
        "prompts": 15,
        "features": ["Report brand illimitati", "AI keyword research", "Monitoraggio base"]
    },
    "Standard": {
        "price_monthly": 189,
        "prompts": 100,
        "features": ["Tutto del Lite", "100 prompts/mese", "Analytics avanzati"]
    },
    "Premium": {
        "price_monthly": 489,
        "prompts": 400,
        "features": ["Tutto dello Standard", "400 prompts/mese", "Priority support"]
    }
}

# Piattaforme monitorate
PLATFORMS = ["ChatGPT", "Perplexity", "Google AI Overviews", "Gemini", "Copilot"]

def calculate_cost(num_prompts, billing_cycle="monthly"):
    """Calcola il costo in base al numero di prompts"""
    if num_prompts <= 15:
        plan = "Lite"
        monthly_cost = 29
    elif num_prompts <= 100:
        plan = "Standard"
        monthly_cost = 189
    else:
        plan = "Premium"
        monthly_cost = 489
        if num_prompts > 400:
            extra_prompts = num_prompts - 400
            # Stima costo extra (non ufficiale, da verificare con Otterly)
            monthly_cost += (extra_prompts // 100) * 150
    
    if billing_cycle == "yearly":
        yearly_cost = monthly_cost * 12 * 0.85  # Assumiamo 15% sconto annuale
        return plan, monthly_cost, yearly_cost
    
    return plan, monthly_cost, monthly_cost * 12

def main():
    # Header
    st.title("🔍 AI Brand Monitoring Cost Calculator")
    st.markdown("**Calcola quanto costa monitorare il tuo brand su ChatGPT e altre AI**")
    st.markdown("---")
    
    # Sidebar per informazioni
    with st.sidebar:
        st.header("ℹ️ Informazioni")
        st.markdown("""
        ### Cos'è Otterly.ai?
        Tool per monitorare come il tuo brand appare su:
        - ChatGPT
        - Perplexity
        - Google AI Overviews
        - Gemini
        - Copilot
        
        ### Cosa sono i "Prompts"?
        Le domande/query che vuoi monitorare, es:
        - "Miglior [categoria] in Italia"
        - "Che cos'è [tuo brand]"
        - "[tuo brand] vs competitor"
        """)
        
        st.markdown("---")
        st.markdown("**Tool creato per calcolare i costi di monitoraggio brand su AI**")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Informazioni Brand")
        brand_name = st.text_input("Nome del tuo brand", placeholder="Es: MioBrand SRL")
        industry = st.selectbox(
            "Settore",
            ["E-commerce", "SaaS", "Servizi", "Prodotti", "Consulenza", "Altro"]
        )
        
        st.subheader("🎯 Configurazione Monitoraggio")
        num_prompts = st.number_input(
            "Numero di prompts da monitorare",
            min_value=1,
            max_value=1000,
            value=15,
            step=5,
            help="Un prompt = una query da monitorare (es: 'miglior software per...')"
        )
        
        competitors = st.number_input(
            "Numero di competitor da tracciare",
            min_value=0,
            max_value=20,
            value=3
        )
    
    with col2:
        st.subheader("🤖 Piattaforme AI")
        selected_platforms = st.multiselect(
            "Piattaforme da monitorare",
            PLATFORMS,
            default=["ChatGPT", "Perplexity", "Google AI Overviews"]
        )
        
        st.subheader("💳 Opzioni di pagamento")
        billing_cycle = st.radio(
            "Ciclo di fatturazione",
            ["monthly", "yearly"],
            format_func=lambda x: "Mensile" if x == "monthly" else "Annuale (sconto ~15%)"
        )
        
        frequency = st.select_slider(
            "Frequenza monitoraggio",
            options=["Settimanale", "Giornaliero", "Real-time"],
            value="Settimanale"
        )
    
    st.markdown("---")
    
    # Calcolo e risultati
    if st.button("🧮 Calcola Costi", type="primary", use_container_width=True):
        plan, monthly_cost, yearly_cost = calculate_cost(num_prompts, billing_cycle)
        
        st.success("✅ Calcolo completato!")
        
        # Risultati principali
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Piano Consigliato",
                plan,
                delta=f"{PLANS[plan]['prompts']} prompts inclusi"
            )
        
        with col2:
            if billing_cycle == "monthly":
                st.metric(
                    "Costo Mensile",
                    f"${monthly_cost}",
                    delta=f"${yearly_cost}/anno"
                )
            else:
                st.metric(
                    "Costo Annuale",
                    f"${yearly_cost:.0f}",
                    delta=f"Risparmi ${(monthly_cost * 12 - yearly_cost):.0f}"
                )
        
        with col3:
            cost_per_prompt = monthly_cost / num_prompts
            st.metric(
                "Costo per Prompt",
                f"${cost_per_prompt:.2f}",
                delta="al mese"
            )
        
        # Dettagli del piano
        st.markdown("---")
        st.subheader(f"📊 Dettagli Piano {plan}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Caratteristiche incluse:**")
            for feature in PLANS[plan]["features"]:
                st.markdown(f"✓ {feature}")
            st.markdown(f"✓ Monitoraggio su {len(selected_platforms)} piattaforme")
            st.markdown(f"✓ Tracking di {competitors} competitor")
            st.markdown(f"✓ Aggiornamenti {frequency.lower()}")
        
        with col2:
            st.markdown("**Piattaforme monitorate:**")
            for platform in selected_platforms:
                st.markdown(f"🤖 {platform}")
        
        # Tabella comparativa
        st.markdown("---")
        st.subheader("📈 Confronto Piani")
        
        comparison_data = {
            "Piano": ["Lite", "Standard", "Premium"],
            "Prezzo/mese": ["$29", "$189", "$489"],
            "Prompts": ["15", "100", "400"],
            "Adatto per": [
                "Piccole imprese, test",
                "Medie imprese, SEO",
                "Enterprise, agencies"
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Raccomandazioni
        st.markdown("---")
        st.subheader("💡 Raccomandazioni")
        
        if num_prompts <= 10:
            st.info("💰 **Piano Lite** è perfetto per iniziare. Puoi sempre fare upgrade.")
        elif num_prompts <= 80:
            st.info("⚙️ **Piano Standard** offre un buon equilibrio qualità-prezzo per la tua esigenza.")
        else:
            st.warning("🚀 **Piano Premium** necessario. Considera di contattare Otterly per piani custom se hai bisogno di più di 400 prompts.")
        
        # ROI Estimation
        st.markdown("---")
        st.subheader("📊 Stima ROI")
        st.markdown("""
        **Benefici del monitoraggio:**
        - Visibilità brand su AI: aumento fino al 50% in 3-6 mesi
        - Ottimizzazione contenuti: migliore posizionamento
        - Vantaggio competitivo: anticipa i competitor
        - Crisis management: rispondi rapidamente a menzioni negative
        """)
        
        # Export
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Crea summary per export
            summary = f"""
REPORT CALCOLO COSTI - AI BRAND MONITORING
==========================================
Brand: {brand_name}
Settore: {industry}
Data: {datetime.now().strftime('%d/%m/%Y')}

CONFIGURAZIONE
--------------
Prompts da monitorare: {num_prompts}
Competitor tracciati: {competitors}
Piattaforme: {', '.join(selected_platforms)}
Frequenza: {frequency}

COSTI
-----
Piano consigliato: {plan}
Costo mensile: ${monthly_cost}
Costo annuale: ${yearly_cost:.0f}
Costo per prompt: ${cost_per_prompt:.2f}/mese

PROMPTS INCLUSI NEL PIANO
--------------------------
{PLANS[plan]['prompts']} prompts/mese
"""
            
            st.download_button(
                label="📥 Scarica Report (TXT)",
                data=summary,
                file_name=f"brand_monitoring_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.link_button(
                "🔗 Vai a Otterly.ai",
                "https://otterly.ai/pricing"
            )

if __name__ == "__main__":
    main()
