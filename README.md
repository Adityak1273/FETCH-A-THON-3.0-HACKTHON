# AutoCollective AI 🚗
### From Personal Buyer AI to Multi-Agent Market Negotiation

[![Live Vercel Portal](https://img.shields.io/badge/Live%20Dashboard-Vercel%20Deployed-success?style=for-the-badge&logo=vercel)](https://fetch-a-thon-30-hackthon-guuor6t9b-adityak1273-8754.vercel.app/)
[![Agentverse](https://img.shields.io/badge/Agentverse-Cloud%20Active-blue?style=for-the-badge)](https://agentverse.ai/agents/details/agent1q09hp6xwguamvsrzd5xgqc8qxyhn3dfgf67pjpz6my68llydt8y9clcwqu9/profile)
[![ASI:One Live Session](https://img.shields.io/badge/ASI:One-Live%20Chat-orange?style=for-the-badge)](https://asi1.ai/chat/d534e5c0-5443-4f6b-b318-536a9ab09921)
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

AutoCollective AI is a decentralized multi-agent car purchasing network built on **Fetch.ai**. It transforms fragmented customer demand into collective bargaining leverage.

🔗 **Live Production Deployment**: [https://fetch-a-thon-30-hackthon-guuor6t9b-adityak1273-8754.vercel.app/](https://fetch-a-thon-30-hackthon-guuor6t9b-adityak1273-8754.vercel.app/)

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
