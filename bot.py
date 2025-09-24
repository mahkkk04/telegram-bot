import asyncio
import subprocess
import sys
import json
import requests
import os
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Configure logging with clearer format
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("JarvisBot")

class JarvisBot:
    def __init__(self, tg_token):
        self.token = tg_token
        self.ollama_ready = False
        self.models = []
        self.active_model = None
        self.api_url = "http://localhost:11434"
        self.memory_path = "jarvis_memory.txt"
        self.system_prompt = self._load_prompt()
        self.memory = self._load_memory()
        
    def _load_prompt(self):
        """Load core system instructions"""
        return (
            "You are JARVIS, an advanced AI assistant. "
            "You are sharp, witty, professional with dry humor, "
            "and remember everything unless told to forget."
        )

    def _load_memory(self):
        """Retrieve memory entries from file"""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    return content if content else "No stored memories."
            except Exception as e:
                logger.error(f"Could not read memory: {e}")
                return "No stored memories."
        return "No stored memories."
    
    def _save_memory(self, note):
        """Append memory with timestamp"""
        try:
            stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"[{stamp}] {note}"
            with open(self.memory_path, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
            self.memory = entry if self.memory == "No stored memories." else self.memory + "\n" + entry
            return True
        except Exception as e:
            logger.error(f"Save memory failed: {e}")
            return False
    
    def _context(self, msg):
        return (
            f"{self.system_prompt}\n\n"
            f"MEMORY:\n{self.memory}\n\n"
            f"USER: {msg}"
        )
        
    def check_ollama(self):
        """Verify Ollama installation"""
        try:
            result = subprocess.run(
                ["ollama", "--version"], capture_output=True, text=True, timeout=8
            )
            if result.returncode == 0:
                logger.info(f"Ollama: {result.stdout.strip()}")
                self.ollama_ready = True
                return True
            return False
        except Exception as e:
            logger.error(f"Ollama check failed: {e}")
            return False
    
    def fetch_models(self):
        """Retrieve available models"""
        try:
            resp = requests.get(f"{self.api_url}/api/tags", timeout=8)
            if resp.status_code == 200:
                payload = resp.json()
                self.models = [m["name"] for m in payload.get("models", [])]
                if self.models:
                    self.active_model = self.models[0]
                return True
            return False
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return False
    
    def respond(self, user_prompt, model=None):
        """Generate a reply with context"""
        if not self.ollama_ready or not self.active_model:
            return "❌ Ollama not configured or no model active."
        
        use_model = model if model in self.models else self.active_model
        payload = {"model": use_model, "prompt": self._context(user_prompt), "stream": False}
        
        try:
            resp = requests.post(f"{self.api_url}/api/generate", json=payload, timeout=100)
            return resp.json().get("response", "No output.") if resp.status_code == 200 else f"❌ API error {resp.status_code}"
        except Exception as e:
            return f"❌ Failed to connect: {e}"
    
    # === Telegram Commands ===
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = (
            "🤖 **JARVIS at your service**\n\n"
            "Commands:\n"
            "• `/status` – Check bot + model state\n"
            "• `/models` – List models\n"
            "• `/model <name>` – Change model\n"
            "• `/memory` – View memories\n"
            "• `/forget` – Erase all memories\n\n"
            "Say *remember this: ...* to store facts."
        )
        await update.message.reply_text(text, parse_mode="Markdown")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.check_ollama()
        if self.ollama_ready: self.fetch_models()
        
        msg = (
            f"🔎 **Status**\n"
            f"Ollama: {'✅' if self.ollama_ready else '❌'}\n"
            f"Models: {len(self.models)}\n"
            f"Active: {self.active_model or 'None'}\n"
            f"Memories: {0 if self.memory == 'No stored memories.' else len(self.memory.splitlines())}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    async def memory_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.memory == "No stored memories.":
            await update.message.reply_text("🧠 Nothing remembered yet.")
        else:
            await update.message.reply_text(f"🧠 Memories:\n\n{self.memory}")
    
    async def forget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            if os.path.exists(self.memory_path):
                os.remove(self.memory_path)
            self.memory = "No stored memories."
            await update.message.reply_text("🧠 Memory wiped clean.")
        except:
            await update.message.reply_text("❌ Could not wipe memory.")
    
    async def handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message.text
        
        if "remember this:" in msg.lower():
            note = msg.lower().split("remember this:")[1].strip()
            if note and self._save_memory(note):
                await update.message.reply_text("🧠 Logged.")
                return
        
        reply = self.respond(msg)
        await update.message.reply_text(reply)
    
    def run(self):
        logger.info("Starting Jarvis...")
        self.check_ollama()
        if self.ollama_ready: self.fetch_models()
        
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("status", self.status))
        app.add_handler(CommandHandler("memory", self.memory_cmd))
        app.add_handler(CommandHandler("forget", self.forget))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler))
        app.run_polling()

def main():
    TG_TOKEN = "your-token-here"
    if TG_TOKEN == "your-token-here":
        print("❌ Replace with actual token.")
        sys.exit(1)
    
    bot = JarvisBot(TG_TOKEN)
    bot.run()

if __name__ == "__main__":
    main()
