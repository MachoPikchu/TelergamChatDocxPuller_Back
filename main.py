import os
import json
from dotenv import load_dotenv
from telethon import TelegramClient, events
from docx import Document

load_dotenv()

# Config
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER")
target_channel = os.getenv("TARGET_CHANNEL")

buffer_dir = '../buffer'
json_file = 'chapters.json'

os.makedirs(buffer_dir, exist_ok=True)

client = TelegramClient("session_realtime", api_id, api_hash)

if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        chapters = json.load(f)
else:
    chapters = []

def extract_text_from_docx(file_path):
    """Read DOCX and return all paragraphs as one string"""
    try:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
        return ""

def extract_title(text, fallback="Untitled"):
    """Use first non-empty line or fallback as title"""
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return fallback

@client.on(events.NewMessage(chats=target_channel))
async def handler(event):
    """Triggered on new message with DOCX"""
    if event.document and event.file.name.endswith(".docx"):
        file_name = event.file.name
        file_path = os.path.join(buffer_dir, file_name)

        try:
            print(f"\n📥 New DOCX: {file_name}")
            await event.download_media(file_path)

            content = extract_text_from_docx(file_path)
            if not content:
                print("⚠️ Skipped empty document.")
                return

            title = extract_title(content, fallback=file_name)
            chapter = {
                "title": title,
                "content": content.strip()
            }

            chapters.append(chapter)

            # Save updated JSON
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(chapters, f, ensure_ascii=False, indent=2)

            print(f"✅ Saved '{title}' to chapters.json")

        except Exception as e:
            print(f"[ERROR] Problem processing {file_name}: {e}")

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Removed {file_name} from buffer")

print("🔄 Listening for new DOCX chapters...")
client.start(phone_number)
client.run_until_disconnected()
