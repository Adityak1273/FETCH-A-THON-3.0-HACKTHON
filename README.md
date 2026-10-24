# AutoCollective AI 🚗
### From Personal Buyer AI to Multi-Agent Market Negotiation

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

AutoCollective AI is a decentralized multi-agent car purchasing network built on **Fetch.ai**. It transforms fragmented customer demand into collective bargaining leverage.

---

## 🏆 Hackathon Tracks Targeted

1. **Best Personal AI**: Private Personal Buyer Concierge interfacing via ASI:One using the Agent Chat Protocol (ACP).
2. **Best Multi-Agent Workflow**: Autonomous coordination, demand pooling, multi-dealer RFQ broadcasts, and competitive bid ranking.
3. **Best Agentverse Deployment**: Fully discoverable agents utilizing Agentverse and ACP.

---

## 🧠 System Architecture

```text
               ASI:One User Chat
                       │
                       ▼  (ACP: Agent Chat Protocol)
        ┌──────────────────────────────┐
        │   Personal Buyer Concierge   │
        └──────────────┬───────────────┘
                       │  (uAgent Direct Protocol)
                       ▼
        ┌──────────────────────────────┐
        │    Collective Coordinator    │ (Groups matching buyers)
        └──────────────┬───────────────┘
                       │  (Bulk RFQ Broadcast)
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌───────────┐ ┌───────────┐ ┌───────────┐
   │Metro Auto │ │Apex Motors│ │ Star City │
   │Dealer AI  │ │Dealer AI  │ │ Dealer AI │
   └───────────┘ └───────────┘ └───────────┘
         │             │             │
         └─────────────┼─────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ ASI:One Interactive Deal Card│
        └──────────────────────────────┘
```

---

## 🚀 Quickstart Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/autocollective-ai.git
cd autocollective-ai

# Install dependencies
pip install uagents uagents-core requests pydantic

# Run all agents locally in Bureau
python run_all.py
```
