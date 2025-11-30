import json
import logging
import os
from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)
from sheets_handler import GoogleSheetsManager
from utils import generate_cmid
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TOKEN: Final = "8004531313:AAFe2WBF58xmPA261uGbzzH7H7pj5tJjwh8"
BOT_USERNAME: Final = "@CodiverseBot"

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t2-chimera:free")

# Initialize OpenAI Client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Conversation States
NAME, SERVICE, DETAILS = range(3)
CHECK_CMID = range(1)

# Initialize Sheets Manager
sheets_manager = GoogleSheetsManager()

# Load Persona
try:
    with open("persona.json", "r") as f:
        PERSONA = json.load(f)
except FileNotFoundError:
    logger.error("persona.json not found!")
    PERSONA = {}

# Load FAQ Data
try:
    with open("faq_data.json", "r") as f:
        FAQ_DATA = json.load(f)
except FileNotFoundError:
    logger.error("faq_data.json not found!")
    FAQ_DATA = {}

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the bot and shows the main menu."""
    user = update.effective_user
    welcome_msg = (
        f"Hello {user.first_name}! 👋🏻\n"
        f"I am DodoAi - Codiverse Support Specialist.\n\n"
        f"I can help you start a new project or check the status of an existing one.\n\n"
        f"What would you like to do?"
    )
    
    reply_keyboard = [["🚀 Start New Project", "🔍 Check Project Status"], ["❓ Help", "🌐 Visit Website"]]
    
    await update.message.reply_text(
        welcome_msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays help information."""
    help_text = (
        "Here's how I can help:\n\n"
        "🚀 **Start New Project**: I'll collect your requirements and assign you a Member ID (CMID).\n"
        "🔍 **Check Project Status**: Use your CMID to track progress.\n"
        "🌐 **Visit Website**: Learn more about Codiverse.\n\n"
        "Just type your query or select an option from the menu!"
    )
    await update.message.reply_text(help_text)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Operation cancelled. How else can I help you?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

# --- New Project Conversation Flow ---

async def start_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the new project flow."""
    await update.message.reply_text(
        "Great! Let's get your project started. 🚀\n\n"
        "First, could you please tell me your **Full Name**?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collects name and asks for service type."""
    context.user_data["name"] = update.message.text
    
    reply_keyboard = [["📱 Mobile App", "💻 Website"], ["🤖 AI/Automation", "🎨 Design/Branding"]]
    
    await update.message.reply_text(
        f"Nice to meet you, {context.user_data['name']}! \n\n"
        "What kind of service are you looking for?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collects service type and asks for details."""
    context.user_data["service"] = update.message.text
    
    await update.message.reply_text(
        "Got it. Please describe your project requirements in detail.\n"
        "Include things like features, target audience, or any specific ideas you have.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DETAILS

async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Collects details, saves to Sheet, and generates CMID."""
    details = update.message.text
    name = context.user_data["name"]
    service = context.user_data["service"]
    
    await update.message.reply_text("Thank you! Processing your request... ⏳")
    
    # Generate CMID
    cmid = generate_cmid()
    
    # Save to Google Sheets
    success = sheets_manager.add_lead(cmid, name, service, details)
    
    if success:
        await update.message.reply_text(
            f"✅ **Request Received Successfully!**\n\n"
            f"Here is your **Codiverse Member ID (CMID)**:\n`{cmid}`\n\n"
            f"⚠️ **Please save this ID safely.** You will need it to check your project status in the future.\n\n"
            f"Our team will review your requirements and get back to you shortly!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ **Oops! Something went wrong.**\n"
            "I couldn't save your request at the moment. Please try again later or contact support."
        )
    
    return ConversationHandler.END

# --- Status Check Conversation Flow ---

async def check_status_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the status check flow."""
    await update.message.reply_text(
        "Sure, I can check that for you. 🔍\n\n"
        "Please enter your **Codiverse Member ID (CMID)**:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CHECK_CMID

async def get_cmid_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Looks up the CMID and returns status."""
    cmid = update.message.text.strip()
    
    await update.message.reply_text("Searching records... ⏳")
    
    result = sheets_manager.get_status(cmid)
    
    if result:
        response = (
            f"📋 **Project Status for {cmid}**\n\n"
            f"👤 **Name:** {result['name']}\n"
            f"🛠 **Service:** {result['service']}\n"
            f"📊 **Current Status:** {result['status']}\n"
            f"📅 **Last Updated:** {result['timestamp']}\n\n"
            f"If you have further questions, feel free to ask!"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ **CMID Not Found**\n\n"
            f"I couldn't find any project with ID `{cmid}`.\n"
            f"Please check if you typed it correctly.",
            parse_mode="Markdown"
        )
        
    return ConversationHandler.END

# --- General Message Handler ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles general messages using OpenRouter LLM."""
    text = update.message.text
    
    if "website" in text.lower() and "visit" in text.lower():
         await update.message.reply_text("You can visit us at: https://codiverse-dev.vercel.app")
         return

    # Construct System Prompt
    system_prompt = f"""
    You are Dodo AI, the support specialist for Codiverse.
    
    **Your Persona:**
    {json.dumps(PERSONA, indent=2)}
    
    **FAQ Knowledge Base:**
    {json.dumps(FAQ_DATA, indent=2)}
    
    **Instructions:**
    - Answer the user's question based on the Persona and FAQ.
    - Be professional, friendly, and helpful.
    - If the answer is not in the FAQ, politely suggest they contact support or visit the website.
    - Keep responses concise and relevant to Telegram chat.
    """

    try:
        completion = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenRouter API Error: {e}")
        response = "I apologize, but I'm having trouble connecting to my brain right now. Please try again later."

    await update.message.reply_text(response)

# --- Error Handler ---

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')


# --- Main Application ---

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Conversation Handler for New Project
    project_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🚀 Start New Project$"), start_project)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
            DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Conversation Handler for Status Check
    status_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🔍 Check Project Status$"), check_status_start)],
        states={
            CHECK_CMID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cmid_status)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Conversations
    app.add_handler(project_conv)
    app.add_handler(status_conv)

    # General Messages (Fallback)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
