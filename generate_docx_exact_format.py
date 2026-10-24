import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def build_doc():
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Color Palette
    PRIMARY = RGBColor(30, 41, 59)      # Slate Navy
    ACCENT_BLUE = RGBColor(37, 99, 235) # Vibrant Cobalt
    MUTED_GRAY = RGBColor(100, 116, 139)
    TEXT_MAIN = RGBColor(15, 23, 42)

    # Heading Style
    normal = doc.styles['Normal']
    normal.font.name = 'Segoe UI'
    normal.font.size = Pt(10)
    normal.font.color.rgb = TEXT_MAIN

    # Top Brand Bar
    p_brand = doc.add_paragraph()
    p_brand.paragraph_format.space_before = Pt(0)
    p_brand.paragraph_format.space_after = Pt(2)
    r_brand = p_brand.add_run("AUTOCOLLECTIVE AI × FETCH.AI")
    r_brand.font.name = 'Segoe UI'
    r_brand.font.size = Pt(13)
    r_brand.font.bold = True
    r_brand.font.color.rgb = ACCENT_BLUE

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("Complete Project Blueprint, Architecture, Tech Stack & Workflow Guide")
    r_title.font.name = 'Segoe UI Semibold'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Fetch-A-Thon 3.0 | GCET National AI Agent Hackathon Edition")
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = MUTED_GRAY

    # Metadata Table (Row of 3 cards exactly like reference)
    meta_table = doc.add_table(rows=1, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="E2E8F0")

    meta_items = [
        ("Project Name", "AutoCollective AI (Car Concierge)"),
        ("Event", "Fetch-A-Thon 3.0 (GCET Greater Noida)"),
        ("Version & Date", "v3.0.0 · October 2026")
    ]

    for col_idx, (label, val) in enumerate(meta_items):
        cell = meta_table.cell(0, col_idx)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r_lbl = p.add_run(f"{label}\n")
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.color.rgb = MUTED_GRAY
        r_lbl.font.bold = True
        r_val = p.add_run(val)
        r_val.font.size = Pt(9.5)
        r_val.font.bold = True
        r_val.font.color.rgb = PRIMARY

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Helper function for section headings
    def add_sec_heading(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_text)
        r.font.name = 'Segoe UI Semibold'
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = PRIMARY
        return p

    # 📋 1. Executive Summary & Problem Statement
    add_sec_heading("📋 1. Executive Summary & Problem Statement")
    
    p_ex1 = doc.add_paragraph()
    p_ex1.paragraph_format.space_after = Pt(6)
    p_ex1.add_run(
        "AutoCollective AI is a decentralized, autonomous multi-agent group car buying and collective negotiation ecosystem engineered for car buyers across India. "
        "Unlike traditional car buying portals that isolate individual buyers—forcing them into opaque showroom markups, inflated ex-showroom add-ons, and fixed non-negotiable pricing—AutoCollective AI pools fragmented individual retail buyers into autonomous bulk-purchasing clusters. "
        "It dynamically matches buyers by exact car model, variant, and regional PIN code to unlock wholesale fleet pricing (5% to 15% instant savings) through autonomous multi-agent reverse auctions."
    )

    p_ex2 = doc.add_paragraph()
    p_ex2.paragraph_format.space_after = Pt(12)
    p_ex2.add_run(
        "AutoCollective AI is engineered specifically to align with the core requirements of Fetch-A-Thon 3.0 at Galgotias College of Engineering & Technology (GCET), "
        "incorporating Fetch.ai uAgents, Agentverse cloud hosting, Agent Chat Protocol (ACP v0.2.0), Almanac fast-track registry, and ASI:One natural language agent discovery to qualify for both the ₹1,00,000 national prize pool and specialized awards (Best Personal AI, Best Multi-Agent Workflow, and Best Agentverse / ASI:One Build)."
    )

    # 💻 2. Complete Technology Stack
    add_sec_heading("💻 2. Complete Technology Stack")
    
    t_stack = doc.add_table(rows=7, cols=3)
    t_stack.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_stack, color="CBD5E1")

    headers = ["Layer / Domain", "Technologies & Libraries", "Role in AutoCollective Architecture"]
    for i, h in enumerate(headers):
        c = t_stack.cell(0, i)
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    stack_rows = [
        ("Client Frontend & Portal", "HTML5 Neo-Brutalist Layout, CSS3 Poster Theme, Vanilla ES6+ JS, JetBrains Mono & Space Grotesk", "Light-theme retro poster UI (localhost:3000) with dynamic vehicle image mapping, interactive trading terminal feed, and 9-field buyer registration."),
        ("Multi-Source Web Scraping", "Non-blocking DuckDuckGo proxy index, CarWale, CarDekho, Spinny, Cars24 live engines", "Zero-mock dynamic pricing engine extracting real-time base, ex-showroom, and on-road prices across India without static hardcoded arrays."),
        ("Currency & Heuristic Normalizer", "Custom RegEx & Luxury Brand Classification Heuristics", "Autonomous valuation engine formatting luxury models (Porsche, Range Rover, Defender, Audi, BMW, Mercedes) in Crores (₹X.XX Cr) and mass-market cars in Lakhs (₹X.XX L)."),
        ("Autonomous Multi-Agent Layer", "Fetch.ai uAgents Python SDK (0.12+), Pydantic v2 Schemas, AsyncIO Bureau", "Personal Buyer Concierge, Group Coordinator Agent, and 3 Dealership Agents executing automated volume discount calculations & reverse auctions."),
        ("Cloud Registry & Agent Hosting", "Fetch.ai Agentverse Cloud, Agent Chat Protocol (ACP v0.2.0), Almanac Ledger Registry", "Persistent cloud agent (@adityak1273, agent1q09hp6xw...) discoverable globally, handling live ACP chats with zero-latency acknowledgments."),
        ("Agentic Search & Natural Chat", "ASI:One (asi1.ai) Agent Discovery, Conversational ACP Endpoints", "Enables retail buyers and dealerships to interact with the AutoCollective Car Concierge using natural language directly inside ASI:One.")
    ]

    for r_idx, (col0, col1, col2) in enumerate(stack_rows, start=1):
        for c_idx, val in enumerate([col0, col1, col2]):
            c = t_stack.cell(r_idx, c_idx)
            set_cell_background(c, "FFFFFF" if r_idx % 2 == 1 else "F8FAFC")
            set_cell_margins(c, top=80, bottom=80, left=110, right=110)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = ACCENT_BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 🏗️ 3. End-to-End System Architecture Blueprint
    add_sec_heading("🏗️ 3. End-to-End System Architecture Blueprint")
    
    p_arch = doc.add_paragraph()
    p_arch.paragraph_format.space_after = Pt(6)
    p_arch.add_run(
        "AutoCollective AI implements a hybrid Local-to-Cloud Agent architecture that pairs local edge execution (for rapid visual configuration, buyer authentication, and regional dealer auction simulation) with autonomous cloud agents on Agentverse (for decentralized coordination, global Almanac discovery, and ASI:One natural language chat)."
    )

    steps = [
        ("Step 1: On-Device Buyer Registration & Demand Setup", "The user accesses the portal (localhost:3000), completes a clean 9-field registration (Name, Email ID, Mobile Number, Gender, Age, Address, PIN Code, Password, Recheck Password), and configures their desired car (e.g. 'Porsche 911 in Delhi' or 'Tata Punch in Mumbai') with Group Collective Pooling selected."),
        ("Step 2: Real-Time Multi-Source Dynamic Scraping", "Instead of querying static mock JSON, the system dispatches an asynchronous GET query across verified Indian automotive indices (CarWale, CarDekho, Spinny, Cars24), pulling raw on-road benchmarks in real-time."),
        ("Step 3: Autonomous Currency & Luxury Normalization", "The extracted text is sanitized, stripping search engine artifacts. Brand heuristics evaluate vehicle tier: multi-crore exotics format correctly in Crores (₹2.52 Cr), while budget vehicles format in Lakhs (₹6.13 Lakhs)."),
        ("Step 4: Autonomous Group Pooling & Pool Hash Assignment", "The request is converted into an ACP ChatMessage or UserCarProfile schema. The Group Coordinator creates a deterministic pool hash (e.g. #delhi_porsche_911) and registers active buyers in the pool registry."),
        ("Step 5: Dealership Reverse Auction & Volume Bidding", "Once the pool threshold (≥2 buyers) is satisfied, the Coordinator broadcasts a RequestForQuote (RFQ). Three distinct dealership uAgents (Metro Hyundai, Apex Motors, Star City Auto) compute fleet discount margins (6%–12% off base + free comprehensive warranty) and submit cryptographic bids."),
        ("Step 6: Final Comparison Report & ASI:One Delivery", "The Coordinator evaluates all bids, reconciles the lowest net cost, and streams the FinalComparisonReport to the local dashboard trading feed and back to the user's live session on ASI:One.")
    ]

    for st_title, st_desc in steps:
        p_st = doc.add_paragraph()
        p_st.paragraph_format.space_after = Pt(4)
        r_st_head = p_st.add_run(f"{st_title}: ")
        r_st_head.font.bold = True
        r_st_head.font.size = Pt(9.5)
        r_st_head.font.color.rgb = PRIMARY
        r_st_body = p_st.add_run(st_desc)
        r_st_body.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 🤖 4. Fetch.ai Multi-Agent Specifications
    add_sec_heading("🤖 4. Fetch.ai Multi-Agent Specifications")
    
    doc.add_paragraph("The project features multiple distinct uAgents communicating over Fetch.ai's agent communication protocol:")

    # Table with agent specifications formatted like reference
    t_agent_specs = doc.add_table(rows=3, cols=1)
    t_agent_specs.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_agent_specs, color="CBD5E1")

    agent_specs_content = [
        ("Agent 1: AutoCollective Car Concierge (Agentverse Cloud Agent)",
         "• Address: agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9 | Handle: @adityak1273\n"
         "• Protocol: Agent Chat Protocol (ACP v0.2.0) with ChatMessage and ChatAcknowledgement handlers.\n"
         "• Responsibilities: Ingests natural language inquiries from ASI:One chat and web hooks. Parses buyer car model, target city, and purchase preference (Solo vs Group). Triggers live multi-source web price verification and assigns pool hash identifiers.\n"
         "• Output: Emits structured chat responses to ASI:One and dispatches buyer profile payloads to the Group Coordinator."),

        ("Agent 2: Group Pooling Coordinator & Negotiator Agent (Local Bureau)",
         "• Protocol: CollectiveNegotiationProtocol (Pydantic models: UserCarProfile, RequestForQuote, FinalComparisonReport)\n"
         "• Responsibilities: Aggregates incoming buyers into dynamic pools by city and model. When pool size reaches ≥2 or ≥3, initiates a RequestForQuote (RFQ) to all registered dealership agents.\n"
         "• Output: Compares incoming dealership bids, calculates collective savings, and generates the final group purchase report."),

        ("Agents 3, 4, 5: Certified Dealership Bidding Network (Local Bureau)",
         "• Protocol: DealershipBiddingProtocol (Inbound: RequestForQuote -> Outbound: DealershipBid)\n"
         "• Responsibilities: Three independent dealership uAgents (Metro Hyundai, Apex Motors, Star City Auto) with distinct margin algorithms. Automatically apply volume discount rules (e.g. 1 buyer = 0%, 2-4 buyers = 6% off, 5+ buyers = 12% off + Free 3-Yr Comprehensive Warranty + Insurance).\n"
         "• Output: Emits competing DealershipBid responses with guaranteed price locks and delivery lead times.")
    ]

    for idx, (title_text, details) in enumerate(agent_specs_content):
        cell = t_agent_specs.cell(idx, 0)
        set_cell_background(cell, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_head = p.add_run(f"{title_text}\n")
        r_head.font.bold = True
        r_head.font.size = Pt(9.5)
        r_head.font.color.rgb = ACCENT_BLUE

        r_det = p.add_run(details)
        r_det.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 🔍 5. ASI:One Integration & Interaction Models
    add_sec_heading("🔍 5. ASI:One Integration & Interaction Models")
    
    doc.add_paragraph("ASI:One acts as the agentic conversational interface connecting human users (buyers and dealerships) directly with the AutoCollective Multi-Agent Network:")

    t_asi = doc.add_table(rows=4, cols=2)
    t_asi.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_asi, color="CBD5E1")

    asi_headers = ["Natural Language Query into ASI:One", "Autonomous Agent Response & Action Executed"]
    for i, h in enumerate(asi_headers):
        c = t_asi.cell(0, i)
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=90, bottom=90, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    asi_rows = [
        ('"What is the best on-road price for a Porsche 911 in Delhi?"',
         "Agent queries live web indices: 'Porsche 911 in Delhi is benchmarked at approx ₹2.52 Crore (ex-showroom/on-road base). A collective pool #delhi_porsche_911 is currently active with 1 buyer. Join to unlock corporate fleet discount margins.'"),
        ('"I want to buy a Tata Punch in Mumbai in a group pool"',
         "Agent registers user in pool: 'Added you to pool #mumbai_tata_punch. Active buyers: 2/3. Threshold met! Dispatching RFQ to regional dealerships: Metro Motors, Apex Tata Fleet, Star City Auto. Volume bid unlocked: 7% off base price.'"),
        ('"Check status of my group car quote for Creta in Bangalore"',
         "Agent scans active dealership bids: 'Bids finalized for Bangalore Creta Pool! Apex Motors won with ₹10.45 Lakhs (6.2% volume discount + Free 1st Year Insurance). Estimated delivery: 14 business days.'")
    ]

    for r_idx, (q, resp) in enumerate(asi_rows, start=1):
        c0 = t_asi.cell(r_idx, 0)
        c1 = t_asi.cell(r_idx, 1)
        set_cell_background(c0, "FFFFFF" if r_idx % 2 == 1 else "F8FAFC")
        set_cell_background(c1, "FFFFFF" if r_idx % 2 == 1 else "F8FAFC")
        set_cell_margins(c0, top=80, bottom=80, left=110, right=110)
        set_cell_margins(c1, top=80, bottom=80, left=110, right=110)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(q)
        r0.font.size = Pt(8.5)
        r0.font.italic = True
        r0.font.color.rgb = PRIMARY

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(resp)
        r1.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 🎯 6. Live Hackathon Pitch & Judge Demo Script (3-Minute Walkthrough)
    add_sec_heading("🎯 6. Live Hackathon Pitch & Judge Demo Script (3-Minute Walkthrough)")
    
    pitches = [
        ("Minute 0:00 - 0:45 (The Problem & The Void)",
         "Introduce yourself and highlight the systemic imbalance in retail automotive sales: 'When an individual walks into a car showroom, they are at the mercy of non-negotiable retail margins and arbitrary accessories. But when corporations buy cars in fleets, dealerships slash prices by 10% to 15%. AutoCollective AI democratizes fleet buying power for individual retail consumers using autonomous Fetch.ai uAgents.'"),

        ("Minute 0:45 - 1:30 (Live Edge Demo & Real-Time Scraping)",
         "Show the live AutoCollective web dashboard running on localhost:3000. Point out the light poster aesthetic, the 9-field buyer registration, and demonstrate searching for both a luxury vehicle ('Porsche 911 in Delhi') and a mass-market car ('Tata Punch in Mumbai'). Highlight the live terminal feed, the dynamic car photography, and how the price engine accurately identifies Crores (₹2.52 Cr) vs Lakhs (₹6.13 L) using live web scraping with zero hardcoded data."),

        ("Minute 1:30 - 2:15 (Fetch.ai Multi-Agent Handshake & Reverse Auction)",
         "Switch to the terminal / Agentverse console. Show how the Group Coordinator aggregates buyers by city and car model into pool hashes, triggers an autonomous RequestForQuote, and pits three independent dealership agents (Metro Hyundai, Apex Motors, Star City Auto) against each other in an automated reverse auction to win the collective order."),

        ("Minute 2:15 - 3:00 (ASI:One Discovery & Closing)",
         "Open ASI:One (asi1.ai) and query the live Agentverse agent @adityak1273. Demonstrate asking for price quotes and joining pools directly in conversational English. Conclude with: 'AutoCollective AI bridges live web intelligence with Fetch.ai's decentralized agent economy to save car buyers lakhs of rupees on every purchase.'")
    ]

    for p_time, p_body in pitches:
        p_pitch = doc.add_paragraph()
        p_pitch.paragraph_format.space_after = Pt(4)
        r_pt = p_pitch.add_run(f"{p_time}: ")
        r_pt.font.bold = True
        r_pt.font.size = Pt(9.5)
        r_pt.font.color.rgb = PRIMARY
        r_pb = p_pitch.add_run(p_body)
        r_pb.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 🔗 7. Project Assets & Repository References
    add_sec_heading("🔗 7. Project Assets & Repository References")

    t_assets = doc.add_table(rows=4, cols=2)
    t_assets.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_assets, color="CBD5E1")

    assets = [
        ("Agentverse Cloud Deployment", "• Agent Handle: @adityak1273\n• Agent Address: agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9\n• Public Profile: https://agentverse.ai/agents/details/agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9/profile"),
        ("ASI:One Live Session", "• Public Shared Chat: https://asi1.ai/chat/d534e5c0-5443-4f6b-b318-536a9ab09921"),
        ("Local Workspace & Source Code", "• Local Path: C:\\Users\\hp\\.gemini\\antigravity\\scratch\\autocollective-ai\n• Git Repository: Local master branch with all agents, schemas, and UI"),
        ("Host Institution & Target Awards", "• Hackathon Venue: Galgotias College of Engineering & Technology (GCET), Greater Noida\n• Target Tracks: Best Personal AI, Best Multi-Agent Workflow, Best Agentverse / ASI:One Build, National Top Tier")
    ]

    for idx, (label, val) in enumerate(assets):
        c0 = t_assets.cell(idx, 0)
        c1 = t_assets.cell(idx, 1)
        set_cell_background(c0, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = ACCENT_BLUE

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(8.5)

    doc.save("C:\\Users\\hp\\.gemini\\antigravity\\scratch\\autocollective-ai\\AutoCollective_AI_Technical_Architecture_Blueprint.docx")
    print("Exact format Word document generated successfully!")

if __name__ == "__main__":
    build_doc()
