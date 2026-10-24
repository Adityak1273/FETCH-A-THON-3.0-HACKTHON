import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))

        # Running header on pages 2+
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "AUTOCOLLECTIVE AI × FETCH.AI — PROJECT BLUEPRINT & ARCHITECTURE")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "FETCH-A-THON 3.0 · GCET EDITION")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, letter[0] - 54, 42)

        self.setFont("Helvetica", 7.5)
        self.drawString(54, 30, "AutoCollective AI · Official Project Blueprint & Technical Specification")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 30, page_text)
        self.restoreState()

def build_pdf():
    downloads_path = os.path.expanduser("~/Downloads")
    pdf_filename = os.path.join(downloads_path, "AutoCollective_AI_Full_Project_Summary_Blueprint.pdf")

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")       # Deep Slate
    BLUE = colors.HexColor("#2563EB")          # Accent Cobalt
    MUTED = colors.HexColor("#64748B")         # Cool Slate
    TEXT = colors.HexColor("#1E293B")          # Main Text
    BG_LIGHT = colors.HexColor("#F8FAFC")      # Table Alternating Row
    BORDER_LIGHT = colors.HexColor("#E2E8F0")  # Borders
    TANGERINE = colors.HexColor("#EA580C")     # Step highlights

    # Typography Styles
    style_super = ParagraphStyle(
        'Super',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=BLUE,
        spaceAfter=3
    )

    style_title = ParagraphStyle(
        'Title',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=4
    )

    style_sub = ParagraphStyle(
        'Sub',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=MUTED,
        spaceAfter=10
    )

    style_h1 = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT,
        spaceAfter=5
    )

    style_body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
        spaceAfter=4
    )

    style_table_text = ParagraphStyle(
        'TText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT
    )

    style_table_header = ParagraphStyle(
        'THeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    style_script_time = ParagraphStyle(
        'STime',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=TANGERINE,
        spaceBefore=4,
        spaceAfter=2
    )

    style_script_body = ParagraphStyle(
        'SBody',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
        spaceAfter=3
    )

    style_script_act = ParagraphStyle(
        'SAct',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=BLUE,
        spaceAfter=6
    )

    story = []

    # Title Header Block
    story.append(Paragraph("AUTOCOLLECTIVE AI × FETCH.AI", style_super))
    story.append(Paragraph("Complete Project Blueprint, Architecture, Tech Stack & Workflow Guide", style_title))
    story.append(Paragraph("Fetch-A-Thon 3.0 | GCET National AI Agent Hackathon Edition · Official Submission Package", style_sub))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Project:</b> AutoCollective AI", style_table_text), Paragraph("<b>Event:</b> Fetch-A-Thon 3.0 (GCET)", style_table_text), Paragraph("<b>Version:</b> v3.0.0 (Oct 2026)", style_table_text)],
        [Paragraph("<b>Agent Handle:</b> @adityak1273", style_table_text), Paragraph("<b>Address:</b> agent1q09hp6x...wqu9", style_table_text), Paragraph("<b>Tracks:</b> Best Personal AI, Multi-Agent", style_table_text)],
        [Paragraph("<b>Live Portal:</b> fetch-a-thon-30-...vercel.app", style_table_text), Paragraph("<b>Repo:</b> github.com/Adityak1273/...", style_table_text), Paragraph("<b>ASI:One:</b> asi1.ai live session active", style_table_text)]
    ]
    t_meta = Table(meta_data, colWidths=[175, 175, 154])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # 1. Executive Summary & Problem Statement
    story.append(Paragraph("📋 1. Project Summary & Core Problem Statement", style_h1))
    story.append(Paragraph(
        "<b>The Problem:</b> When an everyday consumer walks into a car showroom in India, they stand completely isolated. "
        "Dealerships exploit this informational asymmetry with inflated ex-showroom add-ons, non-negotiable dealer charges, mandatory accessory bundles, and rigid retail margins. "
        "Conversely, corporate fleet buyers command <b>10% to 15% bulk discounts</b> directly from regional distributors because of concentrated volume.",
        style_body
    ))
    story.append(Paragraph(
        "<b>The AutoCollective Solution:</b> <b>AutoCollective AI</b> eliminates this retail penalty by pooling fragmented retail car shoppers into autonomous bulk-purchasing clusters. "
        "Using Fetch.ai uAgents on Agentverse and ASI:One, the platform groups buyers by exact vehicle model, variant, and regional PIN code. "
        "Once a collective pool threshold (&ge;2 buyers) is reached, an autonomous reverse auction is triggered across competing regional dealership uAgents, "
        "unlocking wholesale corporate fleet pricing and saving buyers &yen;50,000 to &yen;3,50,000+ per vehicle.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Zero Mock Data Mandate:</b> Unlike typical hackathons relying on pre-fed static tables, AutoCollective features an asynchronous web scraping proxy "
        "indexing live prices from CarWale, CarDekho, Spinny, and Cars24 across India. Luxury exotics (Porsche 911, Range Rover, Defender, Audi) "
        "are autonomously normalized into <b>Crores (&yen;X.XX Cr)</b>, while mass-market cars format in <b>Lakhs (&yen;X.XX L)</b>.",
        style_body
    ))

    # 2. Complete Technology Stack
    story.append(Paragraph("💻 2. Complete Technology Stack", style_h1))
    stack_data = [
        [Paragraph("<b>Layer / Domain</b>", style_table_header), Paragraph("<b>Technologies & Libraries</b>", style_table_header), Paragraph("<b>Role in AutoCollective Architecture</b>", style_table_header)],
        [Paragraph("<b>Client Frontend & Portal</b>", style_table_text), Paragraph("HTML5 Neo-Brutalist Layout, CSS3 Poster Theme, Vanilla ES6+ JS", style_table_text), Paragraph("Light poster dashboard on Vercel with real-time scraped pricing, dynamic car imagery, and 9-field buyer registration.", style_table_text)],
        [Paragraph("<b>Multi-Source Scraping</b>", style_table_text), Paragraph("Non-blocking DuckDuckGo proxy, CarWale, CarDekho, Spinny, Cars24", style_table_text), Paragraph("Zero-mock dynamic pricing engine pulling live ex-showroom and on-road prices across India in real-time.", style_table_text)],
        [Paragraph("<b>Valuation & Heuristics</b>", style_table_text), Paragraph("Custom RegEx & Luxury Automotive Brand Tier Classifier", style_table_text), Paragraph("Autonomous currency normalizer formatting exotics in Crores (&yen;X.XX Cr) and standard cars in Lakhs (&yen;X.XX L).", style_table_text)],
        [Paragraph("<b>Multi-Agent Bureau</b>", style_table_text), Paragraph("Fetch.ai uAgents Python SDK (0.12+), Pydantic v2, AsyncIO Bureau", style_table_text), Paragraph("5 sovereign uAgents (Concierge, Group Coordinator, 3 Dealerships) executing volume discount calculations and reverse auctions.", style_table_text)],
        [Paragraph("<b>Cloud Agentverse Host</b>", style_table_text), Paragraph("Fetch.ai Agentverse Cloud, Almanac Ledger Registry, ACP v0.2.0", style_table_text), Paragraph("Persistent public cloud agent (@adityak1273, agent1q09hp6x...) with ChatAcknowledgement handshake & instant query responses.", style_table_text)],
        [Paragraph("<b>Agentic Search & Chat</b>", style_table_text), Paragraph("ASI:One (asi1.ai) Natural Language Discovery, Conversational ACP", style_table_text), Paragraph("Enables consumers to query live on-road prices and join buying pools directly in plain English inside ASI:One.", style_table_text)],
        [Paragraph("<b>Container & Edge Host</b>", style_table_text), Paragraph("Docker, Docker Compose, Vercel Serverless Edge, GitHub CI/CD", style_table_text), Paragraph("Production deployment with clean vercel.json routing and multi-platform Docker containerization.", style_table_text)]
    ]
    t_stack = Table(stack_data, colWidths=[120, 150, 234])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for row in range(1, len(stack_data)):
        bg = colors.white if row % 2 == 1 else BG_LIGHT
        t_stack.setStyle(TableStyle([('BACKGROUND', (0, row), (-1, row), bg)]))
    story.append(t_stack)
    story.append(Spacer(1, 8))

    # 3. Technical Architecture Blueprint
    story.append(Paragraph("🏗️ 3. Technical Architecture Blueprint & Execution Pipeline", style_h1))
    story.append(Paragraph(
        "AutoCollective AI implements a hybrid Local-to-Cloud architecture pairing local edge execution (for rapid visual configuration, buyer authentication, and regional dealer auction simulation) with autonomous cloud agents on Agentverse (for decentralized coordination, global Almanac discovery, and ASI:One natural language chat):",
        style_body
    ))

    steps_text = [
        ("Step 1: On-Device Demand Ingestion", "The buyer accesses the portal (localhost:3000 or Vercel), completes a clean 9-field registration (Name, Email, Mobile, Address, PIN, Gender, Age, Password), and configures their desired car (e.g. 'Porsche 911 in Delhi') with Group Pooling armed."),
        ("Step 2: Real-Time Multi-Source Dynamic Scraping", "Instead of static JSON, an asynchronous query executes across CarWale, CarDekho, Spinny, and Cars24, pulling raw on-road benchmarks in real-time."),
        ("Step 3: Autonomous Currency & Luxury Normalization", "Brand heuristics evaluate vehicle tier: multi-crore exotics format correctly in Crores (&yen;2.52 Cr), while budget vehicles format in Lakhs (&yen;6.13 Lakhs)."),
        ("Step 4: Autonomous Group Pooling & Pool Hash Assignment", "The request is converted into an ACP ChatMessage or UserCarProfile schema. The Group Coordinator creates a deterministic pool hash (#delhi_porsche_911) and updates the group registry."),
        ("Step 5: Dealership Reverse Auction & Volume Bidding", "Once pool threshold (&ge;2 buyers) is met, the Coordinator broadcasts an RFQ. Three dealership uAgents (Metro Hyundai, Apex Motors, Star City Auto) compute fleet discount margins (6%-12% off base + free warranty) and submit cryptographic bids."),
        ("Step 6: Final Comparison Report & Delivery", "The Coordinator evaluates all bids, reconciles the lowest net cost, and streams the FinalComparisonReport to the dashboard terminal feed and into ASI:One chat.")
    ]

    for st_title, st_desc in steps_text:
        p_st = Paragraph(f"<b>▶ {st_title}:</b> {st_desc}", style_body)
        story.append(p_st)

    story.append(Spacer(1, 8))

    # 4. Multi-Agent Specifications
    story.append(Paragraph("🤖 4. Fetch.ai Multi-Agent Specifications", style_h1))
    agent_specs = [
        [Paragraph("<b>Agent 1: AutoCollective Car Concierge (Agentverse Cloud)</b><br/>"
                   "• Address: agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9 | Handle: @adityak1273<br/>"
                   "• Protocol: Agent Chat Protocol (ACP v0.2.0) with ChatMessage and ChatAcknowledgement handlers.<br/>"
                   "• Responsibilities: Ingests natural language inquiries from ASI:One and web hooks. Triggers live multi-source web price verification and assigns pool hash identifiers.<br/>"
                   "• Output: Emits structured chat responses to ASI:One and dispatches buyer profile payloads to the Group Coordinator.", style_table_text)],
        [Paragraph("<b>Agent 2: Group Pooling Coordinator & Negotiator Agent (Local Bureau)</b><br/>"
                   "• Protocol: CollectiveNegotiationProtocol (Pydantic models: UserCarProfile, RequestForQuote, FinalComparisonReport)<br/>"
                   "• Responsibilities: Aggregates incoming buyers into dynamic pools by city and model. When pool size reaches &ge;2, initiates a RequestForQuote (RFQ) to registered dealership agents.<br/>"
                   "• Output: Compares incoming dealership bids, calculates collective savings, and generates the final group purchase report.", style_table_text)],
        [Paragraph("<b>Agents 3, 4, 5: Certified Dealership Bidding Network (Local Bureau)</b><br/>"
                   "• Protocol: DealershipBiddingProtocol (RequestForQuote &rarr; DealershipBid)<br/>"
                   "• Responsibilities: Three independent dealership uAgents (Metro Hyundai, Apex Motors, Star City Auto) with distinct margin algorithms. Apply volume discount rules (e.g. 6% to 12% off base + Free 3-Yr Warranty + Free Insurance).<br/>"
                   "• Output: Emits competing DealershipBid responses with guaranteed price locks and delivery lead times.", style_table_text)]
    ]
    t_agents = Table(agent_specs, colWidths=[504])
    t_agents.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_agents)
    story.append(Spacer(1, 8))

    # 5. Speech Script & Live Demo Guide
    story.append(Paragraph("🎤 5. 3-Minute Hackathon Demo Speech & Action Guide", style_h1))
    story.append(Paragraph("<i>Use this exact script for team presentations, pitch rounds, and screen recording demos with side-by-side prototype actions:</i>", style_body))

    pitches = [
        ("Minute 0:00 - 0:45 · The Hook & The Problem Statement",
         '"Judges and innovators, when an everyday consumer buys a car in India, they stand completely alone. Dealerships take advantage of this with opaque markups, inflated ex-showroom add-ons, and non-negotiable retail margins. But when corporate corporations purchase cars in bulk fleets, dealerships eagerly slash prices by 10 to 15 percent. We built AutoCollective AI—a decentralized multi-agent network on Fetch.ai that pools retail buyers together to unlock wholesale fleet discounts automatically."',
         'ACTION: Open the live dashboard (fetch-a-thon-30-hackthon-guuor6t9b-adityak1273-8754.vercel.app). Point out the clean poster theme and 9-field buyer registration modal.'),

        ("Minute 0:45 - 1:30 · Live Edge Prototype & Real-Time Intelligence",
         '"Unlike other projects with static, hardcoded JSON tables, our system executes zero-mock real-time web scraping across CarWale, CarDekho, Spinny, and Cars24. Watch what happens when I search for a Porsche 911 in Delhi: our currency heuristic detects the exotic tier and displays &yen;2.52 Crore. If I search for a Tata Punch in Mumbai, it correctly displays in Lakhs. The visual preview updates dynamically, and the terminal streams live agent routing events in real-time."',
         'ACTION: Query "Porsche 911" in "Delhi". Show the extracted snippet, &yen;2.52 Crore pricing, sports car photo, and live terminal feed.'),

        ("Minute 1:30 - 2:15 · Multi-Agent Reverse Auction",
         '"When our Group Coordinator Agent detects two or more buyers targeting the same car in the same region, it assigns a pool hash on the Almanac ledger and issues an autonomous Request For Quote. In our Bureau, three competing dealership agents—Metro Hyundai, Apex Motors, and Star City Auto—execute an automated reverse auction, undercutting each other to offer up to 12% fleet savings plus free warranties."',
         'ACTION: Switch to Bureau logs or dashboard terminal showing competing bids from Metro Hyundai and Apex Motors.'),

        ("Minute 2:15 - 3:00 · ASI:One Discovery & Closing",
         '"Finally, our agent @adityak1273 is live on Fetch.ai Agentverse. Anyone can discover and converse with our agent directly on ASI:One in plain English. AutoCollective AI bridges live web intelligence with Fetch.ai\'s decentralized agent economy to save Indian families lakhs of rupees on every purchase. Thank you!"',
         'ACTION: Open ASI:One (asi1.ai/chat/d534e5c0-5443-4f6b-b318-536a9ab09921) and showcase the live chat with @adityak1273.')
    ]

    for time_title, speech_text, action_text in pitches:
        story.append(Paragraph(time_title, style_script_time))
        story.append(Paragraph(f"<b>Speaking Script:</b> {speech_text}", style_script_body))
        story.append(Paragraph(f"<b>👉 Live Demo Action:</b> {action_text}", style_script_act))

    story.append(Spacer(1, 8))

    # 6. Official Project Submission Links
    story.append(Paragraph("🔗 6. Official Project Submission Links", style_h1))
    links_data = [
        [Paragraph("<b>Live Vercel Deployment</b>", style_body_bold), Paragraph("https://fetch-a-thon-30-hackthon-guuor6t9b-adityak1273-8754.vercel.app/", style_table_text)],
        [Paragraph("<b>GitHub Repository</b>", style_body_bold), Paragraph("https://github.com/Adityak1273/FETCH-A-THON-3.0-HACKTHON.git", style_table_text)],
        [Paragraph("<b>Agentverse Agent Profile</b>", style_body_bold), Paragraph("https://agentverse.ai/agents/details/agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9/profile", style_table_text)],
        [Paragraph("<b>ASI:One Live Session</b>", style_body_bold), Paragraph("https://asi1.ai/chat/d534e5c0-5443-4f6b-b318-536a9ab09921", style_table_text)]
    ]
    t_links = Table(links_data, colWidths=[160, 344])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_links)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully at: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
