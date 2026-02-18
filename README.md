# Wedding Phone Assistant

A voice AI phone assistant for wedding guests. Instead of fielding the same questions from 80 people — *"What's the dress code?"*, *"Where do I park?"*, *"Is there a vegetarian option?"* — your guests simply call a number and get instant, friendly answers.

Built with [LiveKit Agents](https://docs.livekit.io/agents/), fully customizable, and ready for any language.

---

## What it does

- Answers guest questions about **timeline, location, dress code, gifts, food, weather, and more**
- Provides a **natural, conversational phone experience** — no app, no website, just a call
- Stays strictly on topic — politely declines anything unrelated to your wedding (no guarantee, though)
- Speaks your language — configure it as needed

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/wedding-phone-assistant.git
cd wedding-phone-assistant
```

### 2. Install dependencies

Requires [uv](https://docs.astral.sh/uv/). Install it first if you haven't,

Then install the project:

```bash
uv sync
```

### 3. Create a LiveKit account

- Sign up at [livekit.io](https://livekit.io) and create a new project
- Copy your credentials into a `.env` file:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```
**Note**: Best is to use the livekit CLI when creating the project. It will create the .env file automatically.
### 4. Configure your assistant

Copy the example files:

```bash
cp examples/instructions.example.md instructions.md
cp examples/context.example.md context.md
```

**`config.yaml` is your main starting point.** Open it and edit:

```yaml
# Check LiveKit docs for all supported models and languages:
# This repo uses the livekit inference gateway: https://docs.livekit.io/agents/models/
# This example is a German language setup — change as needed
stt: assemblyai/universal-streaming-multilingual:de
llm: openai/gpt-4.1-mini
tts:
  model: cartesia/sonic-3
  voice: b9de4a89-2257-424b-94c2-db18ba68c81a  # find voices at app.cartesia.ai
  language: de
  extra_kwargs:
    speed: 1.1
    emotion: excited

# Make it personal — this is the first thing guests hear
greeting: "You are an assistant for answering questions about the wedding. Introduce yourself and offer help in one sentence."
```


**`instructions.md`** — The assistant's personality, tone, guardrails, and behavior. Includes a `{CONTEXT_MARKDOWN}` placeholder where your wedding info gets injected automatically. Don't remove this placeholder.

**`context.md`** — Your wedding-specific content: timeline, venue, dress code, gifts, food, accommodation, and anything else guests might ask about.

Remove `example` from filenames once you're happy with the content.

### 5. Run the assistant

```bash
uv run python src/agent.py dev
```

---


## Upcoming Features

- [ ] **Hotel search** — Live availability lookup for hotels near your venue
- [ ] **Weather forecast** — Real-time weather for the wedding day, with a smart nudge to call back closer to the date if it's too early for a reliable forecast
- [ ] **Phone number setup guide** — Step-by-step instructions to connect a real phone number via SIP so guests can call from any mobile

