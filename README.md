<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <!-- Background circle with pulse animation -->
  <circle cx="50" cy="50" r="45" fill="#0088cc" opacity="0.1">
    <animate attributeName="r" values="45;50;45" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.1;0.3;0.1" dur="2s" repeatCount="indefinite"/>
  </circle>
  
  <!-- Main Telegram circle -->
  <circle cx="50" cy="50" r="40" fill="#0088cc">
    <animateTransform attributeName="transform" type="rotate" values="0 50 50;360 50 50" dur="10s" repeatCount="indefinite"/>
  </circle>
  
  <!-- Telegram paper plane icon -->
  <g transform="translate(50, 50)">
    <!-- Paper plane path -->
    <path d="M-15,-8 L15,0 L-15,8 L-10,0 Z" fill="white">
      <animateTransform attributeName="transform" type="translate" values="0,0;3,0;0,0" dur="1.5s" repeatCount="indefinite"/>
    </path>
    <circle cx="5" cy="0" r="1.5" fill="white" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0.3;0.8" dur="1s" repeatCount="indefinite"/>
    </circle>
    <!-- Motion lines for send effect -->
    <g opacity="0.6">
      <line x1="16" y1="-2" x2="22" y2="-3" stroke="white" stroke-width="1">
        <animate attributeName="opacity" values="0;0.6;0" dur="2s" repeatCount="indefinite"/>
      </line>
      <line x1="16" y1="0" x2="24" y2="0" stroke="white" stroke-width="1">
        <animate attributeName="opacity" values="0;0.6;0" dur="2s" repeatCount="indefinite" begin="0.2s"/>
      </line>
      <line x1="16" y1="2" x2="22" y2="3" stroke="white" stroke-width="1">
        <animate attributeName="opacity" values="0;0.6;0" dur="2s" repeatCount="indefinite" begin="0.4s"/>
      </line>
    </g>
  </g>
  
  <!-- Subtle glow effect -->
  <circle cx="50" cy="50" r="40" fill="none" stroke="#00aaff" stroke-width="1" opacity="0.5">
    <animate attributeName="opacity" values="0.5;0.8;0.5" dur="3s" repeatCount="indefinite"/>
  </circle>
</svg>
<h1 align="center">🤖 Telegram Bot</h1>


## 🛠️ Tech Stack

| Technology     | Description                    |
| -------------- | ----------------------------- |
| Python         | Main backend language          |
| python-telegram-bot | Telegram API integration |
| SQLite/PostgreSQL | Data persistence            |
| Docker         | Containerization              |
| GitHub Actions | CI/CD and automated tests     |

## 📦 Installation

```bash
git clone https://github.com/mahkkk04/telegram-bot.git
cd telegram-bot
pip install -r requirements.txt
```

## 📝 Usage

1. **Configure your environment variables**  
   Copy `.env.example` to `.env` and fill in your Telegram Bot Token and DB credentials.

2. **Run the bot**  
   ```bash
   python main.py
   ```
   Or use Docker:
   ```bash
   docker-compose up --build
   ```

3. **Extend functionality**  
   Add new modules under the `modules/` directory and register them in `main.py`!


## 🔗 Links

- [Telegram API Docs](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [GitHub Actions](https://github.com/features/actions)

---


  <b>Made with Python & Telegram API • By AnubhavChaturvedi-GitHub</b>
</p>
