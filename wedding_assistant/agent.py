from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""Du bist ein hilfreicher KI-Assistent.
            Du unterstützt nutzer bei fragen mit deinem umfangreichen Wissen.
            deine antworten sind klar und schlüssig, auf den Punkt und ohne umfangreiche formatierung oder punktierung wie emojis, sterne oder symbole.
            Du bist presänd, freundlich und humorvoll.""",
        )

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="assemblyai/universal-streaming-multilingual:de",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Du gehörst zur 'Ben und Gina Hochzeits Assistenz' und bietest in wenigen Worten deine Hilfe an."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)