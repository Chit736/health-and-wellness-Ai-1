import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== SETUP LOGGING =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== ENVIRONMENT VARIABLES CHECK =====
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ ERROR: BOT_TOKEN environment variable is not set!")
    logger.info("💡 Please set BOT_TOKEN in Render.com environment variables")
    logger.info("💡 Get token from @BotFather on Telegram")
    exit(1)

# ===== HEALTH KNOWLEDGE BASE =====
HEALTH_KNOWLEDGE = {
    'en': {
        'heart': """❤️ **Heart Health Tips:**

• **Exercise:** 30 minutes daily walking
• **Diet:** More fruits, vegetables, fish
• **Avoid:** Smoking, excessive salt
• **Monitor:** Blood pressure regularly
• **Sleep:** 7-8 hours per night""",

        'diabetes': """🩸 **Diabetes Management:**

• **Monitor:** Blood sugar levels
• **Diet:** Balanced meals, low sugar
• **Exercise:** Regular physical activity
• **Medication:** Take as prescribed
• **Check-ups:** Regular doctor visits""",

        'exercise': """💪 **Exercise Recommendations:**

• **Cardio:** 150 mins/week (walking, cycling)
• **Strength:** 2x/week (weights, resistance)
• **Flexibility:** Daily stretching
• **Hydration:** Drink water during exercise
• **Rest:** 1-2 days recovery per week""",

        'nutrition': """🥗 **Nutrition Advice:**

• **Fruits & Veggies:** 5 servings daily
• **Protein:** Fish, chicken, beans, tofu
• **Carbs:** Whole grains, brown rice
• **Fats:** Healthy oils, nuts, avocado
• **Water:** 8 glasses daily""",

        'sleep': """😴 **Sleep Health:**

• **Duration:** 7-9 hours per night
• **Consistency:** Same sleep schedule
• **Environment:** Dark, quiet, cool room
• **Avoid:** Screens before bedtime
• **Routine:** Relaxing pre-sleep activities"""
    },
    
    'my': {
        'heart': """❤️ **နှလုံးကျန်းမာရေး အကြံပြုချက်များ:**

• **လေ့ကျင့်ခန်း:** တစ်နေ့မိနစ် ၃၀ လမ်းလျှောက်ခြင်း
• **အစားအစာ:** သစ်သီးများ၊ ဟင်းသီးဟင်းရွက်များ၊ ငါး
• **ရှောင်ကြဉ်ရန်:** ဆေးလိပ်သောက်ခြင်း၊ ဆားအလွန်အကျွံ
• **စောင့်ကြည့်ခြင်း:** သွေးပေါင်ချိန်ပုံမှန်စစ်ဆေးခြင်း
• **အိပ်စက်ခြင်း:** တစ်ညလျှင် ၇-၈ နာရီ""",

        'diabetes': """🩸 **ဆီးချိုရောဂါ စီမံခန့်ခွဲမှု:**

• **စောင့်ကြည့်ခြင်း:** သွေးတွင်းသကြားဓာတ်အဆင့်
• **အစားအစာ:** မျှတသောအစားအစာ၊ သကြားနည်း
• **လေ့ကျင့်ခန်း:** ပုံမှန်ကိုယ်လက်လှုပ်ရှားမှု
• **ဆေးဝါး:** ညွှန်ကြားထားသည့်အတိုင်းသောက်သုံးခြင်း
• **ဆေးစစ်ခြင်း:** ပုံမှန်ဆရာဝန်ပြသခြင်း""",

        'exercise': """💪 **လေ့ကျင့်ခန်း အကြံပြုချက်များ:**

• **နှလုံးသွေးကြောလေ့ကျင့်ခန်း:** တစ်ပတ်လျှင် ၁၅၀ မိနစ် (လမ်းလျှောက်ခြင်း၊ စက်ဘီးစီးခြင်း)
• **ကြွက်သားသန်မာရေး:** တစ်ပတ်လျှင် ၂ ကြိမ် (အလေးမခြင်း)
• **ကြွက်သားဆန့်ခြင်း:** နေ့စဉ်ဆန့်ခြင်း
• **ရေဓာတ်ဖြည့်ခြင်း:** လေ့ကျင့်ခန်းလုပ်နေစဉ် ရေသောက်ခြင်း
• **အနားယူခြင်း:** တစ်ပတ်လျှင် ၁-၂ ရက်အနားယူခြင်း""",

        'nutrition': """🥗 **အာဟာရ အကြံပြုချက်များ:**

• **သစ်သီးနှင့်ဟင်းသီးဟင်းရွက်:** တစ်နေ့လျှင် ၅ ကြိမ်
• **ပရိုတင်း:** ငါး၊ ကြက်၊ ပဲ၊ တိုဖူး
• **ကစီဓာတ်:** ဂျုံကြမ်း၊ ဆန်လုံးညို
• **အဆီ:** ကျန်းမာရေးနှင့်ညီညွတ်သောဆီများ၊ အခွံမာသီးများ
• **ရေ:** တစ်နေ့လျှင် ၈ ခွက်""",

        'sleep': """😴 **အိပ်စက်ခြင်း ကျန်းမာရေး:**

• **ကြာချိန်:** တစ်ညလျှင် ၇-၉ နာရီ
• **မှန်ကန်မှု:** အိပ်ချိန်တူညီခြင်း
• **ပတ်ဝန်းကျင်:** မှောင်ခြင်း၊ တိတ်ဆိတ်ခြင်း၊ အေးခြင်း
• **ရှောင်ကြဉ်ရန်:** အိပ်ခါနီးဖုန်းသုံးခြင်း
• **အလေ့အထ:** အိပ်ခါနီး အနားယူခြင်း"""
    }
}

# ===== COMMAND HANDLERS =====
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    
    welcome_text = f"""
👋 **Hello {user_name}!** 

I'm your **24/7 Health & Wellness AI Assistant** 🤖

I can help you with:
❤️ Heart health
🩸 Diabetes care  
💪 Exercise tips
🥗 Nutrition advice
😴 Sleep health

**Quick commands:**
/start - Show this welcome message
/heart - Heart health tips
/diabetes - Diabetes management  
/exercise - Workout advice
/nutrition - Food guidance
/sleep - Sleep health tips

**Or just type what you need help with!** 💫

_Bot ID: {user_id}_
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')
    logger.info(f"User {user_name} ({user_id}) started the bot")

async def heart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /heart command"""
    await update.message.reply_text(HEALTH_KNOWLEDGE['en']['heart'], parse_mode='Markdown')

async def diabetes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /diabetes command"""
    await update.message.reply_text(HEALTH_KNOWLEDGE['en']['diabetes'], parse_mode='Markdown')

async def exercise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /exercise command"""
    await update.message.reply_text(HEALTH_KNOWLEDGE['en']['exercise'], parse_mode='Markdown')

async def nutrition_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /nutrition command"""
    await update.message.reply_text(HEALTH_KNOWLEDGE['en']['nutrition'], parse_mode='Markdown')

async def sleep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sleep command"""
    await update.message.reply_text(HEALTH_KNOWLEDGE['en']['sleep'], parse_mode='Markdown')

# ===== MESSAGE HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    user_message = update.message.text.lower()
    user_name = update.message.from_user.first_name
    
    logger.info(f"Message from {user_name}: {user_message}")
    
    # Detect language and respond
    user_language = detect_language(user_message)
    response = generate_health_response(user_message, user_language)
    
    await update.message.reply_text(response, parse_mode='Markdown')

def detect_language(message):
    """Detect user language from message"""
    myanmar_keywords = ['မင်္ဂလာပါ', 'ကျေးဇူး', 'ဆီးချို', 'နှလုံး', 'လေ့ကျင့်ခန်း', 'အာဟာရ', 'အိပ်ခြင်း']
    if any(keyword in message for keyword in myanmar_keywords):
        return 'my'
    return 'en'

def generate_health_response(message, language='en'):
    """Generate AI health response"""
    lang_data = HEALTH_KNOWLEDGE.get(language, HEALTH_KNOWLEDGE['en'])
    
    # Check for health topics
    if any(word in message for word in ['heart', 'cardio', 'blood pressure', 'နှလုံး', 'သွေးတိုး']):
        return lang_data['heart']
    elif any(word in message for word in ['diabet', 'sugar', 'blood sugar', 'ဆီးချို', 'သကြား']):
        return lang_data['diabetes']
    elif any(word in message for word in ['exercise', 'workout', 'fitness', 'လေ့ကျင့်ခန်း', 'အားကစား']):
        return lang_data['exercise']
    elif any(word in message for word in ['nutrition', 'food', 'diet', 'eat', 'အာဟာရ', 'အစာ', 'စား']):
        return lang_data['nutrition']
    elif any(word in message for word in ['sleep', 'bed', 'tired', 'အိပ်', 'အိပ်ခြင်း', 'အိပ်ရေး']):
        return lang_data['sleep']
    else:
        if language == 'my':
            return "🤖 **ကျေးဇူးပြု၍ အောက်ပါတို့ထဲမှ တစ်ခုခုကို မေးမြန်းပါ:**\n• နှလုံးကျန်းမာရေး\n• ဆီးချိုရောဂါ\n• လေ့ကျင့်ခန်းများ\n• အာဟာရဆိုင်ရာ\n• အိပ်စက်ခြင်းကျန်းမာရေး\n\nသို့မဟုတ် command များသုံးပါ: /heart, /diabetes, /exercise, /nutrition, /sleep"
        else:
            return "🤖 **I can help you with:**\n• Heart health\n• Diabetes care\n• Exercise tips\n• Nutrition advice\n• Sleep health\n\n**Or use commands:** /heart, /diabetes, /exercise, /nutrition, /sleep"

# ===== ERROR HANDLER =====
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")

# ===== MAIN FUNCTION =====
def main():
    """Start the bot"""
    try:
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("heart", heart_command))
        app.add_handler(CommandHandler("diabetes", diabetes_command))
        app.add_handler(CommandHandler("exercise", exercise_command))
        app.add_handler(CommandHandler("nutrition", nutrition_command))
        app.add_handler(CommandHandler("sleep", sleep_command))
        
        # Add message handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        # Check environment and start bot
        if os.environ.get('RENDER') or os.environ.get('PORT'):
            # Running on Render.com - use webhook
            PORT = int(os.environ.get('PORT', 10000))
            WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')
            
            if not WEBHOOK_URL:
                logger.error("❌ WEBHOOK_URL not set in environment variables")
                logger.info("💡 Please set WEBHOOK_URL in Render.com environment variables")
                exit(1)
                
            logger.info(f"🌐 Starting webhook on port {PORT}")
            logger.info(f"🌐 Webhook URL: {WEBHOOK_URL}")
            
            app.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
                url_path=BOT_TOKEN
            )
        else:
            # Running locally - use polling
            logger.info("🔍 Starting polling...")
            app.run_polling()
            
    except Exception as e:
        logger.error(f"❌ Bot failed to start: {e}")
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Health & Wellness AI Bot...")
    print("💡 Make sure BOT_TOKEN is set in environment variables")
    main()
