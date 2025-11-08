bot.py

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot Token - BotFather ကရတဲ့ Token နဲ့အစားထိုးပါ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable is not set!")
    print("Please set your Telegram Bot Token in Render.com environment variables")
    exit(1)
# Health Knowledge Base
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
• **Water:** 8 glasses daily"""
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
• **ဆေးစစ်ခြင်း:** ပုံမှန်ဆရာဝန်ပြသခြင်း"""
    }
}

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    welcome_text = f"""
👋 **Hello {user_name}!** 

I'm your **24/7 Health & Wellness AI Assistant** 🤖

I can help you with:
❤️ Heart health
🩸 Diabetes care  
💪 Exercise tips
🥗 Nutrition advice

**Quick commands:**
/heart - Heart health tips
/diabetes - Diabetes management  
/exercise - Workout advice
/nutrition - Food guidance

Just type what you need help with! 💫
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_language = detect_language(user_message)
    
    response = generate_health_response(user_message, user_language)
    await update.message.reply_text(response, parse_mode='Markdown')

def detect_language(message):
    myanmar_keywords = ['မင်္ဂလာပါ', 'ကျေးဇူး', 'ဆီးချို', 'နှလုံး', 'လေ့ကျင့်ခန်း']
    if any(keyword in message for keyword in myanmar_keywords):
        return 'my'
    return 'en'

def generate_health_response(message, language='en'):
    lang_data = HEALTH_KNOWLEDGE.get(language, HEALTH_KNOWLEDGE['en'])
    
    if any(word in message for word in ['heart', 'cardio', 'blood pressure', 'နှလုံး', 'သွေးတိုး']):
        return lang_data['heart']
    elif any(word in message for word in ['diabet', 'sugar', 'blood sugar', 'ဆီးချို', 'သကြား']):
        return lang_data['diabetes']
    elif any(word in message for word in ['exercise', 'workout', 'fitness', 'လေ့ကျင့်ခန်း', 'အားကစား']):
        return lang_data['exercise']
    elif any(word in message for word in ['nutrition', 'food', 'diet', 'eat', 'အာဟာရ', 'အစာ', 'စား']):
        return lang_data['nutrition']
    else:
        if language == 'my':
            return "🤖 **ကျေးဇူးပြု၍ အောက်ပါတို့ထဲမှ တစ်ခုခုကို မေးမြန်းပါ:**\n• နှလုံးကျန်းမာရေး\n• ဆီးချိုရောဂါ\n• လေ့ကျင့်ခန်းများ\n• အာဟာရဆိုင်ရာ"
        else:
            return "🤖 **I can help you with:**\n• Heart health\n• Diabetes care\n• Exercise tips\n• Nutrition advice\n\nJust ask me anything!"

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

def main():
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("heart", lambda u,c: u.message.reply_text(HEALTH_KNOWLEDGE['en']['heart'], parse_mode='Markdown')))
    app.add_handler(CommandHandler("diabetes", lambda u,c: u.message.reply_text(HEALTH_KNOWLEDGE['en']['diabetes'], parse_mode='Markdown')))
    app.add_handler(CommandHandler("exercise", lambda u,c: u.message.reply_text(HEALTH_KNOWLEDGE['en']['exercise'], parse_mode='Markdown')))
    app.add_handler(CommandHandler("nutrition", lambda u,c: u.message.reply_text(HEALTH_KNOWLEDGE['en']['nutrition'], parse_mode='Markdown')))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("🤖 Health AI Bot is running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
