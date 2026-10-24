import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def build_architecture_doc():
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Palette
    NAVY = RGBColor(15, 23, 42)      # #0F172A
    COBALT = RGBColor(37, 99, 235)   # #2563EB
    STEEL = RGBColor(71, 85, 105)    # #475569
    DARK_TEXT = RGBColor(30, 41, 59) # #1E293B
    ORANGE = RGBColor(234, 88, 12)   # #EA580C
    GREEN = RGBColor(16, 185, 129)   # #10B981

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = DARK_TEXT

    # Header / Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_badge = title_p.add_run("TECHNICAL BLUEPRINT & SYSTEM ARCHITECTURE\n")
    run_badge.font.name = 'Segoe UI'
    run_badge.font.size = Pt(9.5)
    run_badge.font.bold = True
    run_badge.font.color.rgb = COBALT

    run_title = title_p.add_run("AutoCollective AI: Decentralized Multi-Agent Car Buying & Collective Group Bidding Architecture")
    run_title.font.name = 'Segoe UI Semibold'
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    r_sub = sub_p.add_run("Technical Specification for Fetch-A-Thon 3.0 • Built with Fetch.ai uAgents, Agentverse Cloud, ACP Protocol, ASI:One & Neo-Brutalist Local Dashboard\n")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = STEEL

    r_meta = sub_p.add_run("Author: Team AutoCollective (@adityak1273) | Track Target: Best Personal AI, Best Multi-Agent Workflow, Best Agentverse Deployment | Date: October 2026")
    r_meta.font.size = Pt(9)
    r_meta.font.bold = True
    r_meta.font.color.rgb = STEEL

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Callout Box: Executive Summary
    summary_table = doc.add_table(rows=1, cols=1)
    summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = summary_table.cell(0, 0)
    set_cell_background(c, "F1F5F9")
    set_cell_margins(c, top=140, bottom=140, left=200, right=200)
    p_box = c.paragraphs[0]
    p_box.paragraph_format.space_after = Pt(4)
    r_box_title = p_box.add_run("📌 Executive Summary & Architectural Mission\n")
    r_box_title.font.bold = True
    r_box_title.font.size = Pt(11)
    r_box_title.font.color.rgb = COBALT

    r_box_body = p_box.add_run(
        "AutoCollective AI is a decentralized multi-agent automotive procurement ecosystem that eliminates predatory retail markups by pooling fragmented retail buyers into autonomous bulk-purchasing clusters. "
        "The system combines an autonomous cloud-hosted Concierge Agent on Agentverse (accessible via Fetch.ai ACP and ASI:One natural language chat) with a high-performance local dashboard that connects to multiple certified dealership uAgents, groups buyers by vehicle model and regional pin code, and leverages zero-mock real-time web scraping to extract accurate on-road benchmarks across India."
    )
    r_box_body.font.size = Pt(10)
    r_box_body.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # SECTION 1: HIGH-LEVEL ARCHITECTURAL TOPOLOGY
    h1 = doc.add_heading("1. High-Level Architectural Topology", level=1)
    h1.style.font.name = 'Segoe UI Semibold'
    h1.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "The AutoCollective architecture is divided into three interconnected runtime environments, each handling specific responsibilities in an asynchronous, non-blocking pipeline:"
    )

    t_layers = doc.add_table(rows=4, cols=3)
    t_layers.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_layers)

    headers = ["Layer / Subsystem", "Technology Stack", "Core Responsibilities"]
    for i, h_text in enumerate(headers):
        cell = t_layers.cell(0, i)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    layer_data = [
        ("Cloud Agent Subsystem\n(Agentverse Cloud)", "Fetch.ai uAgents Cloud, Agent Chat Protocol (ACP), Almanac fast-track registry, ASI:One Chat interface", "Acts as the global autonomous public gateway. Exposes natural language dialogue on asi1.ai, registers the agent identity on the Fetch.ai ledger Almanac, parses buyer intent, triggers multi-source web price verification, and announces pooling opportunities."),
        ("Local Multi-Agent Bureau\n(Local Python Runtime)", "Python 3.10+, uAgents Bureau, Pydantic v2 schemas, AsyncIO event loops, Dealership Rules Engines", "Orchestrates 5 local uAgents running concurrently in a Bureau. Handles private group pooling, volume threshold evaluation (e.g. 3+ buyers = 7% discount, 5+ = 12% discount), dealership reverse-auction bidding, and multi-quote comparison reports."),
        ("Local Interactive Dashboard\n(Client-Side Web Portal)", "HTML5 Neo-Brutalism, CSS3 Poster styling, Vanilla JavaScript ES6+, Python HTTP Server (Port 3000)", "Provides zero-friction human-in-the-loop configuration. Features buyer registration (10 comprehensive profile fields), dynamic vehicle image recognition, live log streaming (ACP routing, Almanac hashing), and client-side multi-source web index extraction.")
    ]

    for row_idx, data in enumerate(layer_data, start=1):
        for col_idx, text in enumerate(data):
            cell = t_layers.cell(row_idx, col_idx)
            set_cell_background(cell, "FFFFFF" if row_idx % 2 == 1 else "F8FAFC")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COBALT

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # SECTION 2: FETCH.AI AGENTVERSE DEPLOYED AGENT ARCHITECTURE
    h2 = doc.add_heading("2. Fetch.ai Agentverse Cloud Agent Architecture", level=1)
    h2.style.font.name = 'Segoe UI Semibold'
    h2.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "The cloud agent deployed on Agentverse represents the public persona of the AutoCollective network. "
        "It is continuously discoverable on the decentralized Almanac ledger, allowing any external wallet, user, or other Fetch.ai agent to interact with it."
    )

    p_spec = doc.add_paragraph()
    p_spec.add_run("Key Agent Specifications:\n").font.bold = True
    specs = [
        ("Agent Name", "AutoCollective Car Concierge"),
        ("Agentverse Handle", "@adityak1273"),
        ("Decentralized Address", "agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9"),
        ("Public Almanac Profile", "https://agentverse.ai/agents/details/agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9/profile"),
        ("ASI:One Live Session", "https://asi1.ai/chat/d534e5c0-5443-4f6b-b318-536a9ab09921"),
        ("Protocol Compliance", "Agent Chat Protocol (ACP v0.2.0) with ChatMessage and ChatAcknowledgement handlers")
    ]
    for k, v in specs:
        p_spec.add_run(f"• {k}: ").font.bold = True
        p_spec.add_run(f"{v}\n")

    doc.add_paragraph(
        "How the Agentverse Agent Executes Internally:\n"
        "1. ACP Inbound Listener: Listens for incoming ChatMessage packets sent from users via ASI:One or cross-agent requests.\n"
        "2. Acknowledgment Handshake: Instantly dispatches a ChatAcknowledgement message to confirm handshake validity and prevent session timeout.\n"
        "3. NLP Parsing Engine: Regex & NLP tokenizers extract the target Vehicle Model, Target City, and Purchase Preference (Solo Retail vs Group Collective Buying).\n"
        "4. Live Multi-Source Price Scraper: Dispatches an asynchronous non-blocking GET request to https://r.jina.ai/ over DuckDuckGo search indexes. Queries CarWale, CarDekho, Spinny, and Cars24 concurrently without mock databases.\n"
        "5. Crores vs. Lakhs Currency Normalizer: Automatically applies Indian currency classification heuristics. If a luxury brand (Porsche, Range Rover, Defender, Audi, BMW, Mercedes, Ferrari) is queried, values are formatted in Crores (₹X.XX Cr); mass-market vehicles (Punch, Creta, Swift) format in Lakhs (₹X.XX Lakhs).\n"
        "6. Collective Pool Hash Registration: Generates a deterministic pool key (e.g. #mumbai_porsche_911) and outputs group slot confirmation back to the chat."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # SECTION 3: LOCAL MULTI-AGENT WORKFLOW & BUREAU ARCHITECTURE
    h3 = doc.add_heading("3. Local Multi-Agent Workflow & Bureau Architecture", level=1)
    h3.style.font.name = 'Segoe UI Semibold'
    h3.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "In our local repository (autocollective-ai), the private negotiation layer runs inside a unified uAgents Bureau. "
        "The Bureau manages inter-agent message passing without requiring external webhooks or public ports, allowing rapid simulation of dealership reverse-auctions."
    )

    t_agents = doc.add_table(rows=6, cols=3)
    t_agents.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_agents)

    a_headers = ["Agent Name", "Port / Address", "Role & Logic Pipeline"]
    for i, h_text in enumerate(a_headers):
        cell = t_agents.cell(0, i)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    a_data = [
        ("Personal Buyer Concierge\n(personal_buyer_agent.py)", "Port 8000\nagent1q_personal...", "Ingests buyer specification, builds UserCarProfile Pydantic schema, and transmits request to the Group Coordinator."),
        ("Group Pooling Coordinator\n(negotiator_agent.py)", "Port 8001\nagent1q_negotiator...", "Aggregates incoming buyers by pool_id (city + model). When group threshold >= 2 is reached, converts solo requests into a RequestForQuote (RFQ) with a group size modifier."),
        ("Metro Hyundai Dealership\n(dealer_agents.py)", "Port 8002\nagent1q_metro...", "Authorized dealership agent with a volume discount matrix: 1 buyer = 0%, 2-4 buyers = 6% off base, 5+ buyers = 12% off + Free 3-Yr Comprehensive Warranty."),
        ("Apex Motors Dealership\n(dealer_agents.py)", "Port 8003\nagent1q_apex...", "Aggressive competitor agent offering 7.5% fleet reduction for pools >= 3 buyers, plus complimentary first-year insurance."),
        ("Star City Auto Dealership\n(dealer_agents.py)", "Port 8004\nagent1q_starcity...", "Premium certified network offering cash back credits and expedited priority factory delivery for collective orders.")
    ]

    for row_idx, data in enumerate(a_data, start=1):
        for col_idx, text in enumerate(data):
            cell = t_agents.cell(row_idx, col_idx)
            set_cell_background(cell, "FFFFFF" if row_idx % 2 == 1 else "F8FAFC")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COBALT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # SECTION 4: LOCAL WEB DASHBOARD ARCHITECTURE
    h4 = doc.add_heading("4. Local Web Dashboard Architecture (localhost:3000)", level=1)
    h4.style.font.name = 'Segoe UI Semibold'
    h4.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "The frontend dashboard (index.html) is built to provide an intuitive, high-engagement interface adhering to a modern retro-poster aesthetic. "
        "It completely decouples the user experience from technical agent syntax."
    )

    doc.add_paragraph(
        "Key Subsystems of the Dashboard:\n"
        "• Light Poster Neo-Brutalist Theme: Styled with warm poster cream (#FFFBF5), canary yellow headers, tangerine accents, 2px solid ink borders, and sharp graphic shadows.\n"
        "• Dynamic Vehicle Imagery Engine: Uses smart image classification to render authentic photographs corresponding to the user's query (Porsche 911, Range Rover, Defender, Audi, Fortuner, Creta, Thar, Punch).\n"
        "• Comprehensive Buyer Registration Module: Implements a clean 9-field authentication form (Name, Email ID, Mobile Number, Gender, Age, Address, PIN Code, Password, Recheck Password) with client-side verification and localStorage identity persistence.\n"
        "• Live Multi-Agent Event Terminal: Emulates an operational trading terminal, displaying timestamped logs showing ACP packet routing, Almanac lookups, web scraper progress, and dealer bid reconciliation.\n"
        "• Dual Mode Selector: Supports testing both Solo Retail Purchase and Group Collective Pooling workflows with a single toggle."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # SECTION 5: STEP-BY-STEP DATA FLOW & COMMUNICATION LIFECYCLE
    h5 = doc.add_heading("5. Step-by-Step Data Flow & Communication Lifecycle", level=1)
    h5.style.font.name = 'Segoe UI Semibold'
    h5.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "The following sequence illustrates how a user request traverses the full ecosystem from browser input to final negotiated quotation:"
    )

    steps = [
        ("Step 1: Identity & Demand Setup", "The user registers their buyer profile on the dashboard (Name, Mobile, Location PIN) and configures their desired car (e.g. 'Porsche 911 in Delhi') with Group Pooling selected."),
        ("Step 2: Real-Time Multi-Index Query", "The dashboard or cloud agent initiates an asynchronous web query across CarWale, CarDekho, Spinny, and Cars24 via the non-blocking proxy, pulling live price benchmarks."),
        ("Step 3: Currency & Formatting Heuristic", "The currency normalizer evaluates brand tier: Luxury vehicles (Porsche, Range Rover, Audi) are formatted in Crores (₹2.52 Cr), while mass-market cars stay in Lakhs."),
        ("Step 4: Dispatch to Agentverse / Bureau", "The request is converted into an ACP ChatMessage or UserCarProfile schema and broadcast to the Group Pooling Coordinator."),
        ("Step 5: Autonomous Pool Formation", "The Coordinator checks the active pool registry. If threshold >= 2 is met, it groups buyers and issues RequestForQuote broadcasts to Metro Hyundai, Apex Motors, and Star City Auto."),
        ("Step 6: Dealer Bidding War", "Each dealership agent computes its discount using its internal volume margin rules and responds with a DealershipBid."),
        ("Step 7: Final Comparison Report", "The Coordinator evaluates all incoming bids, selects the optimal discount package, and presents the FinalComparisonReport on the dashboard and via ASI:One chat.")
    ]

    for title, desc in steps:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.space_after = Pt(4)
        r_st = p_step.add_run(f"▶ {title}\n")
        r_st.font.bold = True
        r_st.font.size = Pt(10)
        r_st.font.color.rgb = ORANGE

        r_sd = p_step.add_run(desc)
        r_sd.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # SECTION 6: HACKATHON WINNING HIGHLIGHTS FOR TEAMMATES
    h6 = doc.add_heading("6. Key Highlights & Pitch Points for Teammates", level=1)
    h6.style.font.name = 'Segoe UI Semibold'
    h6.style.font.color.rgb = NAVY

    doc.add_paragraph(
        "When explaining this architecture in presentations or video demos, emphasize these core innovations:\n"
        "1. Zero Mock Data: Unlike typical hackathon submissions with hardcoded pricing arrays, our agent queries live Indian web indices dynamically.\n"
        "2. Genuine Decentralized Deployment: Agent is live on the public Fetch.ai Agentverse Almanac ledger and callable directly by anyone on asi1.ai.\n"
        "3. Solves Real-World Economic Friction: Group car buying gives individual retail consumers the bargaining power of corporate fleet purchasers.\n"
        "4. Resilient Architecture: Decoupled design ensures the local dashboard continues functioning with live web extraction even if local uAgents Bureau is paused."
    )

    doc.save("C:\\Users\\hp\\.gemini\\antigravity\\scratch\\autocollective-ai\\AutoCollective_AI_Technical_Architecture_Blueprint.docx")
    print("Word document created successfully!")

if __name__ == "__main__":
    build_architecture_doc()
