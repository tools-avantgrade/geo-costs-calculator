import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="AI Brand Monitoring Calculator",
    page_icon="🔍",
    layout="wide"
)

# Dati dei tool e relativi piani
TOOLS_DATA = {
    "Profound": {
        "description": "Answer engine tracking specializzato",
        "currency": "$",
        "plans": {
            "Base": {
                "price_monthly": 499,
                "answer_engines": 4,
                "companies": 1,
                "prompts": 200,
                "data_history": "1 mese",
                "features": ["4 answer engines tracked", "1 company tracked", "200 prompts tracked", "1 mese data history"]
            }
        }
    },
    "Otterly.ai": {
        "description": "Leader nel monitoraggio AI search",
        "currency": "$",
        "plans": {
            "Lite": {
                "price_monthly": 29,
                "prompts": 15,
                "features": ["Report brand illimitati", "AI prompt research", "Monitoraggio base", "Tutte le piattaforme AI"]
            },
            "Standard": {
                "price_monthly": 189,
                "prompts": 100,
                "features": ["Tutto del Lite", "100 prompts/mese", "Analytics avanzati", "Export dati"]
            },
            "Premium": {
                "price_monthly": 489,
                "prompts": 400,
                "features": ["Tutto dello Standard", "400 prompts/mese", "Priority support", "API access"]
            }
        }
    },
    "Ubersuggest": {
        "description": "SEO + AI monitoring completo",
        "currency": "€",
        "plans": {
            "Individual": {
                "price_monthly": 29,
                "users": 1,
                "domains": 1,
                "daily_searches": 150,
                "prompts_analyze": 50,
                "competitors": 5,
                "pages_crawled": 1000,
                "prompts_tracked": 125,
                "ai_prompts": 10,
                "features": ["150 ricerche/giorno", "50 prompts analisi", "5 competitor", "1000 pagine scansionate", "10 AI prompts/mese"]
            },
            "Business": {
                "price_monthly": 49,
                "users": 2,
                "domains": 7,
                "daily_searches": 300,
                "prompts_analyze": 200,
                "competitors": 10,
                "pages_crawled": 5000,
                "prompts_tracked": 150,
                "ai_prompts": 15,
                "prompt_frequency": "ogni 2 settimane",
                "features": ["2 utenti", "7 domini", "300 ricerche/giorno", "200 prompts analisi", "10 competitor", "15 AI prompts/2 settimane"]
            }
        }
    },
    "Conductor": {
        "description": "Enterprise SEO & content platform",
        "currency": "€",
        "plans": {
            "Professional": {
                "price_monthly": 620,
                "pages": 1000,
                "prompts": 500,
                "drafts": 60,
                "features": ["1000 pagine", "500 prompts", "60 drafts", "Content optimization", "SEO insights"]
            },
            "Enterprise": {
                "price_monthly": 1310,
                "pages": 5000,
                "prompts": 1000,
                "drafts": 120,
                "features": ["5000 pagine", "1000 prompts", "120 drafts", "Advanced analytics", "Priority support", "Custom integrations"]
            }
        }
    }
}

PLATFORMS = ["ChatGPT", "Perplexity", "Google AI Overviews", "Gemini", "Copilot"]

def calculate_cost_otterly(num_prompts, billing_cycle="monthly"):
    """Calcola il costo per Otterly.ai"""
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
            monthly_cost += (extra_prompts // 100) * 150
    
    yearly_discount = 0.85 if billing_cycle == "yearly" else 1
    yearly_cost = monthly_cost * 12 * yearly_discount
    
    return plan, monthly_cost, yearly_cost

def calculate_cost_profound(num_prompts, num_companies=1, billing_cycle="monthly"):
    """Calcola il costo per Profound"""
    base_cost = 499
    
    extra_cost = 0
    if num_prompts > 200:
        extra_prompts = num_prompts - 200
        extra_cost += (extra_prompts // 100) * 200
    
    if num_companies > 1:
        extra_cost += (num_companies - 1) * 300
    
    monthly_cost = base_cost + extra_cost
    yearly_discount = 0.85 if billing_cycle == "yearly" else 1
    yearly_cost = monthly_cost * 12 * yearly_discount
    
    return "Base", monthly_cost, yearly_cost

def calculate_cost_ubersuggest(ai_prompts, domains=1, billing_cycle="monthly"):
    """Calcola il costo per Ubersuggest"""
    if ai_prompts <= 10 and domains <= 1:
        plan = "Individual"
        monthly_cost = 29
    else:
        plan = "Business"
        monthly_cost = 49
        if domains > 7:
            monthly_cost += (domains - 7) * 10
    
    yearly_discount = 0.85 if billing_cycle == "yearly" else 1
    yearly_cost = monthly_cost * 12 * yearly_discount
    
    return plan, monthly_cost, yearly_cost

def calculate_cost_conductor(prompts, pages=1000, billing_cycle="monthly"):
    """Calcola il costo per Conductor"""
    if prompts <= 500 and pages <= 1000:
        plan = "Professional"
        monthly_cost = 620
    else:
        plan = "Enterprise"
        monthly_cost = 1310
        if prompts > 1000:
            monthly_cost += ((prompts - 1000) // 500) * 400
        if pages > 5000:
            monthly_cost += ((pages - 5000) // 1000) * 100
    
    yearly_discount = 0.85 if billing_cycle == "yearly" else 1
    yearly_cost = monthly_cost * 12 * yearly_discount
    
    return plan, monthly_cost, yearly_cost

def main():
    # Header
    st.title("🔍 AI Brand Monitoring Cost Calculator")
    st.markdown("**Confronta i costi tra i principali tool di monitoraggio brand su AI**")
    st.markdown("---")
    
    # Sidebar per informazioni
    with st.sidebar:
        st.header("ℹ️ Informazioni Tool")
        
        selected_tool_info = st.selectbox(
            "Seleziona tool per info",
            list(TOOLS_DATA.keys())
        )
        
        st.markdown(f"### {selected_tool_info}")
        st.markdown(f"*{TOOLS_DATA[selected_tool_info]['description']}*")
        
        st.markdown("**Piani disponibili:**")
        for plan_name in TOOLS_DATA[selected_tool_info]['plans'].keys():
            plan = TOOLS_DATA[selected_tool_info]['plans'][plan_name]
            currency = TOOLS_DATA[selected_tool_info]['currency']
            st.markdown(f"- **{plan_name}**: {currency}{plan['price_monthly']}/mese")
        
        st.markdown("---")
        st.markdown("### Piattaforme AI monitorate")
        st.markdown("- ChatGPT\n- Perplexity\n- Google AI Overviews\n- Gemini\n- Copilot")
        
        st.markdown("---")
        st.markdown("### 💡 Cosa sono i Prompts?")
        st.markdown("""
        I **prompts** (o query) sono le domande che vuoi monitorare sulle AI:
        - "Miglior software CRM"
        - "Come scegliere un consulente"
        - "Alternative a [competitor]"
        - "[Brand] vs [competitor]"
        """)
    
    # Selezione tool principale
    st.subheader("🛠️ Seleziona il Tool")
    selected_tool = st.selectbox(
        "Quale tool vuoi usare?",
        list(TOOLS_DATA.keys()),
        help="Ogni tool ha caratteristiche e prezzi diversi"
    )
    
    currency = TOOLS_DATA[selected_tool]['currency']
    
    st.markdown("---")
    
    # Input form - tutto in verticale
    st.subheader("🎯 Configurazione Monitoraggio")
    
    # Input specifici per tool
    if selected_tool == "Otterly.ai":
        num_prompts = st.number_input(
            "Numero di prompts da monitorare",
            min_value=1,
            max_value=1000,
            value=15,
            step=5,
            help="Quante query vuoi tracciare (es: 'miglior software per...', 'come scegliere...')"
        )
    
    elif selected_tool == "Profound":
        num_prompts = st.number_input(
            "Numero di prompts da monitorare",
            min_value=1,
            max_value=1000,
            value=200,
            step=10,
            help="Piano base include 200 prompts"
        )
        num_companies = st.number_input(
            "Numero di company da tracciare",
            min_value=1,
            max_value=10,
            value=1,
            help="Piano base include 1 company"
        )
    
    elif selected_tool == "Ubersuggest":
        ai_prompts = st.number_input(
            "AI Prompts al mese",
            min_value=1,
            max_value=100,
            value=10,
            step=5,
            help="Numero di AI prompts/query al mese da monitorare"
        )
        domains = st.number_input(
            "Numero di domini (progetti)",
            min_value=1,
            max_value=20,
            value=1,
            help="Quanti domini/progetti vuoi monitorare"
        )
    
    elif selected_tool == "Conductor":
        prompts = st.number_input(
            "Numero di prompts",
            min_value=1,
            max_value=5000,
            value=500,
            step=50,
            help="Quanti prompts vuoi tracciare"
        )
        pages = st.number_input(
            "Numero di pagine",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Quante pagine del sito monitorare"
        )
    
    competitors = st.number_input(
        "Numero di competitor da tracciare",
        min_value=0,
        max_value=20,
        value=3,
        help="Quanti competitor vuoi monitorare"
    )
    
    selected_platforms = st.multiselect(
        "🤖 Piattaforme da monitorare",
        PLATFORMS,
        default=["ChatGPT", "Perplexity", "Google AI Overviews"],
        help="Seleziona le piattaforme AI da monitorare"
    )
    
    billing_cycle = st.radio(
        "💳 Ciclo di fatturazione",
        ["monthly", "yearly"],
        format_func=lambda x: "Mensile" if x == "monthly" else "Annuale (sconto ~15%)",
        horizontal=True
    )
    
    frequency = st.select_slider(
        "⏱️ Frequenza monitoraggio",
        options=["Settimanale", "Giornaliero", "Real-time"],
        value="Settimanale"
    )
    
    st.markdown("---")
    
    # Calcolo e risultati
    if st.button("🧮 Calcola Costi", type="primary", use_container_width=True):
        
        # Calcolo in base al tool selezionato
        if selected_tool == "Otterly.ai":
            plan, monthly_cost, yearly_cost = calculate_cost_otterly(num_prompts, billing_cycle)
            main_metric = f"{num_prompts} prompts"
        elif selected_tool == "Profound":
            plan, monthly_cost, yearly_cost = calculate_cost_profound(num_prompts, num_companies, billing_cycle)
            main_metric = f"{num_prompts} prompts, {num_companies} company"
        elif selected_tool == "Ubersuggest":
            plan, monthly_cost, yearly_cost = calculate_cost_ubersuggest(ai_prompts, domains, billing_cycle)
            main_metric = f"{ai_prompts} AI prompts, {domains} domini"
        elif selected_tool == "Conductor":
            plan, monthly_cost, yearly_cost = calculate_cost_conductor(prompts, pages, billing_cycle)
            main_metric = f"{prompts} prompts, {pages} pagine"
        
        st.success(f"✅ Calcolo completato per {selected_tool}!")
        
        # Risultati principali
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Piano Consigliato",
                f"{selected_tool} - {plan}",
                delta=main_metric
            )
        
        with col2:
            if billing_cycle == "monthly":
                st.metric(
                    "Costo Mensile",
                    f"{currency}{monthly_cost}",
                    delta=f"{currency}{yearly_cost:.0f}/anno"
                )
            else:
                savings = (monthly_cost * 12 - yearly_cost)
                st.metric(
                    "Costo Annuale",
                    f"{currency}{yearly_cost:.0f}",
                    delta=f"Risparmi {currency}{savings:.0f}",
                    delta_color="inverse"
                )
        
        with col3:
            if selected_tool in ["Otterly.ai", "Profound"]:
                metric_value = num_prompts if selected_tool == "Otterly.ai" else num_prompts
                cost_per_unit = monthly_cost / metric_value if metric_value > 0 else 0
                st.metric(
                    "Costo per Prompt",
                    f"{currency}{cost_per_unit:.2f}",
                    delta="al mese"
                )
            elif selected_tool == "Ubersuggest":
                cost_per_prompt = monthly_cost / ai_prompts if ai_prompts > 0 else 0
                st.metric(
                    "Costo per AI Prompt",
                    f"{currency}{cost_per_prompt:.2f}",
                    delta="al mese"
                )
            elif selected_tool == "Conductor":
                cost_per_prompt = monthly_cost / prompts if prompts > 0 else 0
                st.metric(
                    "Costo per Prompt",
                    f"{currency}{cost_per_prompt:.2f}",
                    delta="al mese"
                )
        
        # Dettagli del piano
        st.markdown("---")
        st.subheader(f"📊 Dettagli Piano {plan} - {selected_tool}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Caratteristiche incluse:**")
            plan_features = TOOLS_DATA[selected_tool]['plans'][plan]['features']
            for feature in plan_features:
                st.markdown(f"✓ {feature}")
            st.markdown(f"✓ Monitoraggio su {len(selected_platforms)} piattaforme")
            st.markdown(f"✓ Tracking di {competitors} competitor")
            st.markdown(f"✓ Aggiornamenti {frequency.lower()}")
        
        with col2:
            st.markdown("**Piattaforme monitorate:**")
            for platform in selected_platforms:
                st.markdown(f"🤖 {platform}")
        
        # Tabella comparativa tra tutti i tool
        st.markdown("---")
        st.subheader("📈 Confronto tra Tool")
        
        comparison_data = {
            "Tool": [],
            "Piano Base": [],
            "Prezzo/mese": [],
            "Caratteristica Principale": [],
            "Ideale per": []
        }
        
        tool_recommendations = {
            "Profound": ("Base", "$499", "Answer engine tracking", "Enterprise con focus AI-first"),
            "Otterly.ai": ("Lite", "$29", "AI search monitoring", "Startup e PMI"),
            "Ubersuggest": ("Individual", "€29", "SEO + AI completo", "Freelancer e piccoli team"),
            "Conductor": ("Professional", "€620", "Enterprise SEO platform", "Grandi aziende")
        }
        
        for tool, (plan_name, price, feature, ideal) in tool_recommendations.items():
            comparison_data["Tool"].append(tool)
            comparison_data["Piano Base"].append(plan_name)
            comparison_data["Prezzo/mese"].append(price)
            comparison_data["Caratteristica Principale"].append(feature)
            comparison_data["Ideale per"].append(ideal)
        
        df = pd.DataFrame(comparison_data)
        
        # Evidenzia il tool selezionato
        def highlight_selected(row):
            if row['Tool'] == selected_tool:
                return ['background-color: #28a745; color: white'] * len(row)
            return [''] * len(row)
        
        styled_df = df.style.apply(highlight_selected, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Raccomandazioni personalizzate
        st.markdown("---")
        st.subheader("💡 Raccomandazioni")
        
        if selected_tool == "Otterly.ai":
            if num_prompts <= 15:
                st.info("💰 **Ottimo inizio!** Il piano Lite è perfetto per testare il monitoraggio AI con pochi prompts.")
            elif num_prompts <= 100:
                st.info("⚙️ **Scelta equilibrata!** Lo Standard offre un ottimo rapporto qualità-prezzo.")
            else:
                st.warning("🚀 **Uso intensivo!** Considera il Premium o contatta Otterly per piani custom.")
        
        elif selected_tool == "Profound":
            st.info("🎯 **Tool specializzato!** Profound è ideale per focus su answer engines e tracking profondo.")
            if num_prompts > 200:
                st.warning(f"⚠️ Stai superando i 200 prompts inclusi. Costo stimato per {num_prompts - 200} prompts extra.")
        
        elif selected_tool == "Ubersuggest":
            st.info("📊 **All-in-one!** Ubersuggest combina SEO tradizionale con AI prompt monitoring.")
            if domains > 1:
                st.success("✅ Ottimo per gestire più progetti/clienti con prompts diversificati.")
        
        elif selected_tool == "Conductor":
            st.info("🏢 **Enterprise solution!** Conductor è la scelta per grandi organizzazioni.")
            if prompts > 500:
                st.success("✅ Il piano Enterprise ti darà più flessibilità per prompt tracking massivo.")
        
        # ROI Estimation
        st.markdown("---")
        st.subheader("📊 Stima ROI")
        
        roi_benefits = {
            "Otterly.ai": [
                "Visibilità brand su AI: +50% in 3-6 mesi",
                "Ottimizzazione contenuti per risposte AI",
                "Tracking competitor su prompts rilevanti",
                "Identificazione gap di mercato"
            ],
            "Profound": [
                "Deep insights su answer engines",
                "Tracking accurato su 4+ piattaforme AI",
                "Data history per analisi trend prompts",
                "Focus su conversazioni AI"
            ],
            "Ubersuggest": [
                "SEO + AI prompt monitoring combinato",
                "Prompt research tradizionale + AI",
                "Analisi competitor su query comuni",
                "Content ideas per ottimizzazione AI"
            ],
            "Conductor": [
                "Platform enterprise completa",
                "Content workflow automation",
                "Advanced analytics su prompts",
                "Integrations con marketing stack"
            ]
        }
        
        st.markdown(f"**Benefici con {selected_tool}:**")
        for benefit in roi_benefits[selected_tool]:
            st.markdown(f"- {benefit}")
        
        # Export
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Crea summary per export
            summary = f"""
REPORT CALCOLO COSTI - AI BRAND MONITORING
==========================================
Tool selezionato: {selected_tool}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

CONFIGURAZIONE
--------------
{main_metric}
Competitor tracciati: {competitors}
Piattaforme: {', '.join(selected_platforms)}
Frequenza: {frequency}

COSTI
-----
Piano consigliato: {plan}
Costo mensile: {currency}{monthly_cost}
Costo annuale: {currency}{yearly_cost:.0f}
Ciclo: {billing_cycle}

CARATTERISTICHE PIANO
---------------------
"""
            for feature in plan_features:
                summary += f"- {feature}\n"
            
            summary += f"\n---\nCalcolatore by AI Brand Monitoring Calculator"
            
            st.download_button(
                label="📥 Scarica Report (TXT)",
                data=summary,
                file_name=f"{selected_tool.lower().replace('.', '_')}_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col2:
            # Link al tool selezionato
            tool_urls = {
                "Profound": "https://profound.ai",
                "Otterly.ai": "https://otterly.ai/pricing",
                "Ubersuggest": "https://neilpatel.com/ubersuggest/pricing",
                "Conductor": "https://conductor.com/pricing"
            }
            
            st.link_button(
                f"🔗 Vai a {selected_tool}",
                tool_urls[selected_tool]
            )
        
        with col3:
            st.link_button(
                "🔄 Confronta Altri Tool",
                "#",
                help="Torna su e cambia tool per confrontare"
            )

if __name__ == "__main__":
    main()
