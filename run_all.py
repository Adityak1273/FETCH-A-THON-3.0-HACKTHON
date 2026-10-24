from uagents import Bureau
from dealer_agents import dealer_metro, dealer_apex, dealer_star
from negotiator_agent import coordinator, DEALER_LIST
from personal_buyer_agent import personal_agent
import personal_buyer_agent

# Register dealer addresses in coordinator
DEALER_LIST.extend([dealer_metro.address, dealer_apex.address, dealer_star.address])

# Link personal agent to coordinator
personal_buyer_agent.COORDINATOR_ADDRESS = coordinator.address

bureau = Bureau()
bureau.add(dealer_metro)
bureau.add(dealer_apex)
bureau.add(dealer_star)
bureau.add(coordinator)
bureau.add(personal_agent)

if __name__ == "__main__":
    print("=" * 60)
    print("AutoCollective AI Multi-Agent Network Starting...")
    print(f"Personal Agent Address : {personal_agent.address}")
    print(f"Coordinator Address    : {coordinator.address}")
    print(f"Dealer Metro Address   : {dealer_metro.address}")
    print(f"Dealer Apex Address    : {dealer_apex.address}")
    print(f"Dealer Star Address    : {dealer_star.address}")
    print("=" * 60)
    bureau.run()
