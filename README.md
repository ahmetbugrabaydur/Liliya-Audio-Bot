# Liliya: The Innkeeper's Daughter (Audio Bot)

A specialized Telegram music bot with a dual-client architecture designed for tabletop RPG and D&D sessions.

## Introduction: The Quest for Music
In Telegram bot development, the `phone.CreateGroupCall` error is a known limitation. This restriction prevents standard bot accounts from joining voice chats directly, often making it difficult to automate music in groups.

Liliya was developed to overcome this challenge. Instead of accepting this limitation, I implemented a Dual-Client Architecture. By pairing a traditional bot with a dedicated Userbot (Assistant), I bypassed these restrictions to provide high-quality audio streaming.

## The Challenge & Solution
Standard Telegram bots cannot manage or join voice calls due to API restrictions. 

**Liliya solves this by using two separate clients:**
- **The Bot Client:** Manages user commands, messaging, and interface updates.
- **The Assistant Client (Userbot):** A dedicated account that joins the voice chat to stream audio using the `PyTgCalls` library.

## Features
- **Queue System:** Support for multiple songs with sequential playback.
- **Playback Controls:** Full support for pause, resume, mute, and unmute commands.
- **Navigation:** Skip to the next track or stop the session to clear the queue.
- **D&D Optimized:** Tailored for the specific needs of the FRP community.

## Prerequisites
Before running the bot, ensure you have the following installed on your system:
- **Python 3.8+**: The core programming language.
- **Node.js 16+**: Required for the PyTgCalls engine.
- **FFmpeg**: Essential for processing and streaming audio data.

## Configuration
To get the bot running, open `main.py` and fill in your credentials:
- **API_ID & API_HASH**: Obtain these from the [Telegram Core website](https://my.telegram.org).
- **BOT_TOKEN**: Create a bot and get the token from [@BotFather](https://t.me/BotFather).

## Installation & Setup

**Clone the repository:**
```markdown
**Clone the repository:**
```bash
git clone https://github.com/ahmetbugrabaydur/Liliya-Audio-Bot.git
cd Liliya-Audio-Bot
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the bot
```bash
python main.py
