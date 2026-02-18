from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, inference
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).parent

instructions_raw = Path("instructions.md").read_text(encoding="utf-8")
context_md = Path("context.md").read_text(encoding="utf-8")
FINAL_INSTRUCTIONS = instructions_raw.replace("{CONTEXT_MARKDOWN}", context_md)

load_dotenv(".env.local")
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=FINAL_INSTRUCTIONS,
        )

    async def on_enter(self):
        await self.session.generate_reply(
            instructions=config["greeting"]
        )

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt=config["stt"],
        llm=config["llm"],
        tts=inference.TTS(model=config["tts"]["model"],
                          voice=config["tts"]["voice"],
                          language=config["tts"]["language"],
                          extra_kwargs={
                           "speed": config["tts"]["extra_kwargs"]["speed"],
                          "emotion": config["tts"]["extra_kwargs"]["emotion"]   
                          }),
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


if __name__ == "__main__":
    agents.cli.run_app(server)