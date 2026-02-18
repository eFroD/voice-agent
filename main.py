from wedding_assistant.agent import server as agent_server
from livekit import agents

def main():
    agents.cli.run_app(agent_server)


if __name__ == "__main__":
    main()
