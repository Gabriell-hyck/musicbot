Discord Music Bot

Bot Discord keren buat play musik di voice channel pake Python. Bisa search YouTube, manage queue, dan fitur standar music bot lainnya!

✨ Fitur

· 🎧 Play musik dari YouTube (search query atau URL langsung)
· 📋 Queue system buat antrian lagu
· ⏭️ Skip lagu yang lagi playing
· ⏯️ Pause/Resume
· 📜 Liat queue yang lagi antri
· 🧹 Clear semua queue
· 🚪 Auto join/leave voice channel

📋 Requirements

· Python 3.8 atau lebih baru
· FFmpeg terinstall di sistem
· Bot token dari Discord Developer Portal

🚀 Installation

1. Clone Repository

```bash
git clone https://github.com/username/discord-music-bot.git
cd discord-music-bot
```

2. Install FFmpeg

Windows:

· Download dari ffmpeg.org
· Extract folder-nya
· Tambahin path bin folder ke System Environment Variables

Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install ffmpeg
```

macOS:

```bash
brew install ffmpeg
```

3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Atau manual:

```bash
pip install discord.py yt-dlp PyNaCl
```

4. Setup Bot Token

1. Buka Discord Developer Portal
2. Bikin aplikasi baru, masuk ke tab Bot
3. Copy token bot-nya
4. Ganti YOUR_BOT_TOKEN_HERE di file bot.py pake token lo:

```python
bot.run('TOKEN_BOT_LO_DISINI')
```

5. Enable Intents

Di Discord Developer Portal:

· Bot → Privileged Gateway Intents
· Aktifin MESSAGE CONTENT INTENT

6. Invite Bot ke Server

Di Discord Developer Portal:

· OAuth2 → URL Generator
· Pilih scope bot dan applications.commands
· Pilih permissions: Connect, Speak, Send Messages, Read Message History
· Buka generated URL, pilih server, invite!

🎮 Cara Pake

Command List

Command Description
!join Bot join voice channel lo
!play <query> Play lagu dari YouTube (bisa nama lagu atau URL)
!skip Skip lagu sekarang
!pause Pause lagu
!resume Resume lagu yang di-pause
!queue Liat daftar antrian lagu
!clear Hapus semua antrian
!leave Bot keluar dari voice channel

Contoh Penggunaan

```
!join
!play never gonna give you up
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!queue
!skip
!leave
```

📁 Struktur Project

```
discord-music-bot/
│
├── bot.py              # Main bot file
├── requirements.txt    # Dependencies
└── README.md          # This file
```

⚙️ Konfigurasi

Lo bisa ngubah prefix command di:

```python
bot = commands.Bot(command_prefix='!', intents=intents)
```

Ganti ! jadi prefix yang lo mau (contoh: $, ?, /, dll)

🐛 Troubleshooting

Bot gak bisa join voice channel?

· Pastiin lo lagi di voice channel
· Cek bot punya permission Connect dan Speak

FFmpeg error?

· Pastiin FFmpeg udah keinstall dan ke-detect di PATH
· Coba restart terminal/command prompt

No audio?

· Cek volume bot di Discord
· Pastiin bot gak di-mute atau deafened

yt-dlp error?

· Update yt-dlp: pip install --upgrade yt-dlp

📦 Requirements.txt

Bikin file requirements.txt:

```
discord.py==2.3.2
yt-dlp>=2023.12.30
PyNaCl==1.5.0
```
