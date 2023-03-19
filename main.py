import telegram
from telegram.ext import Updater, CommandHandler
import openai

bot_token = '<YOUR_TELEGRAM_BOT_TOKEN'
api_key = "<YOUR_OPENAI_API_KEY>"

# initialisez l'API OpenAI avec votre clé d'API
openai.api_key = api_key

# Remplacez <TOKEN> par le token d'API de votre bot
bot = telegram.Bot(token=bot_token)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour! Je m'appelle Alfie. Si vous avez envie de découvrir des anecdotes insolites vous êtes au bon endroit. Utilisez la commande /help pour plus d'aide")


def help_command(update, context):
    help_text = "Bienvenue! Voici les commandes disponibles:\n\n"
    help_text += "/anecdote - Obtenir une anecdote aléatoire\n"
    help_text += "/help - Afficher cette aide"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def generate_anecdote():
    model_engine = "text-davinci-002"
    prompt = "donne une anecdote historique insolite"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    anecdote = response.choices[0].text.strip()
    return anecdote

# Créez une fonction qui envoie une seule anecdote aléatoire lorsque le bot reçoit la commande /anecdote
def send_anecdote(update, context):
    anecdote = generate_anecdote()
    context.bot.send_message(chat_id=update.effective_chat.id, text=anecdote)

# Créez un bot et ajoutez une commande "/anecdote"

updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
anecdote_handler = CommandHandler("anecdote", send_anecdote)
help_handler = CommandHandler("help", help_command)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(anecdote_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(start_handler)

# Démarrez le bot
updater.start_polling()
