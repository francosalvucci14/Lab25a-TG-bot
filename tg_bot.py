import telebot
from telebot import types
from functools import wraps
from logs import log_file, LOG_DIR
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def is_known_username(username):
    '''
    Returns a boolean if the username is known in the user-list.
    '''
    known_usernames = ['Acr0n1m0', 'davidenox','Levvonci', 'Spaadd','CromoCon','alesandu','Compssss']

    return username in known_usernames


def private_access():
    """
    Restrict access to the command to users allowed by the is_known_username function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.username

            if is_known_username(username):
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='Che cazzo voi?')
                bot.reply_to(message, text='Non hai i diritti per utilizzare questo comando')

        return f_restrict  # true decorator

    return deco_restrict

# Comandi cand e infores disabilitati
# @bot.message_handler(commands=['cand'])
# def cand(msg):
#     markup = types.InlineKeyboardMarkup(row_width=2)
    
#     # candSi = types.InlineKeyboardButton(
#     #     'Si', callback_data='candYes')
#     # candNo = types.InlineKeyboardButton(
#     #     'No', callback_data='candNo')

#     #markup.add(candSi,candNo)
#     sendCand = bot.send_message(
#         msg.chat.id, 'Ti vuoi candidare per il ruolo di responsabile del Laboratorio 25a? [S/N]', reply_markup=markup)
#     bot.register_next_step_handler(sendCand,sendCandFunc)

# def sendCandFunc(msg):
#     si = ['si','Si','Yes','yes','y','s','S']
#     no = ['no','No','n','N']

#     if msg.text in si:
#         log_obj = {
#             'chat_id': msg.chat.id,
#             'message_id': msg.message_id,
#             'message': 'Utente '+str(msg.from_user.first_name)+' ha risposto SI alla candidatura',
#             'user': f'{str(msg.from_user.first_name)}: [{msg.from_user.username}]'
#         }
#         log_file_cand(log_obj)
#         bot.send_message(msg.chat.id,'Grazie, abbiamo ricevuto la tua candidatura')
#     elif msg.text in no:
#         log_obj = {
#             'chat_id': msg.chat.id,
#             'message_id': msg.message_id,
#             'message': 'Utente '+str(msg.from_user.first_name)+' ha risposto NO alla candidatura',
#             'user': f'{str(msg.from_user.first_name)}: [{msg.from_user.username}]'
#         }
#         log_file_cand(log_obj)
#         bot.send_message(msg.chat.id,'Grazie per il tuo tempo')
#     else:
#         bot.send_message(msg.chat.id, "Attento! Non hai speficicato la tua risposta alla candidatura.\nRipeti il comando /cand")

# @bot.message_handler(commands=['infores'])
# def infoRes(msg):
#     bot.send_message(msg.chat.id,"Ecco tutto quello che devi sapere se vuoi entrare a far parte dei responsabili del laboratorio 25a")
#     #bot.send_poll(msg.chat.id,"Test polling",["si","no"],False,None,False)
#     bot.send_message(msg.chat.id,"Essere responsabili del laboratorio significa che:\n- Avrai accesso alle chiavi del laboratorio, quindi potrai, e dovrai, andare in segreteria a prenderle\n- Potrai chiudere il laboratorio quando vuoi, basta che prima di farlo avvisi della chiusura e mandi via tutti\n- Se uno degli altri responsabili non c'è, non dovrai aspettare per l'apertura, sarai tu stesso ad aprire\n- Ricorda sempre di far rispettare le regole del laboratorio, e se vedi qualcuno che non fa informatica, CACCIALO\n⚠️⚠️⚠️ Occhio ad una cosa, se un giorno apri il laboratorio, e di conseguenza firmi, la responsabilità è TUA. Se succede qualcosa e sei l'unico responsabile presente, scusa il termine, so CAZZI TUA. Quindi presta bene attenzione⚠️⚠️⚠️.\nPer altre informazioni chiedi ai responsabili già presenti")



@bot.message_handler(commands=['start'])
def startMSG(message):
    log_obj = {
        'chat_id': message.chat.id,
        'message_id': message.message_id,
        'message': 'Comando lanciato: start',
        'user': message.from_user.username,
        'command': 'start'
    }

    bot.send_message(message.chat.id, 'Lab25a Bot Operativo')
    bot.send_message(message.chat.id, 'Per iniziare ad utilizzare il bot lancia il comando /list')
   # bot.send_message(message.chat.id, 'Ciao, al momento sono aperte le candidature per i nuovi responsabili del laboratorio.\nSe ti interessa lancia i comandi /infores e /cand\n[Mi raccomando, leggi bene il messaggio ottenuto dal comando /infores, ci sono tutte le informazioni per quanto riguarda essere uno dei responsabili del laboratorio :)]')
    log_file(log_obj)

@bot.message_handler(commands=['msg'])
@private_access()
def msg(message):
    log_obj = {
        'chat_id': message.chat.id,
        'message_id': message.message_id,
        'message': 'Comando lanciato: msg',
        'user': message.from_user.username,
        'command': 'msg'
    }
    log_file(log_obj)
    markup = types.InlineKeyboardMarkup(row_width=2)

    aperto = types.InlineKeyboardButton(
        'Lab Aperto', callback_data='answer_open')
    chiuso = types.InlineKeyboardButton(
        'Lab Chiuso', callback_data='answer_close')
    caffesi = types.InlineKeyboardButton(
        'Caffe Disponibile', callback_data='answer_coffe')
    caffeno = types.InlineKeyboardButton(
        'Caffe Terminato', callback_data='answer_nocoffe')

    markup.add(aperto, chiuso, caffesi, caffeno)
    bot.send_message(
        message.chat.id, 'Cosa vuoi scrivere sul gruppo?', reply_markup=markup)


@bot.message_handler(commands=['com'])
@private_access()
def comunications(msg):
    log_obj = {
        'chat_id': msg.chat.id,
        'message_id': msg.message_id,
        'message': 'Comando lanciato: com',
        'user': msg.from_user.username,
        'command': 'com'
    }
    log_file(log_obj)
    markup = types.InlineKeyboardMarkup(row_width=2)
    send = bot.send_message(
        msg.chat.id, 'Cosa vuoi comunicare agli utenti?[se hai sbagliato a lanciare il comando, scrivi NO]', reply_markup=markup)
    bot.register_next_step_handler(send, comm)


def comm(msg):
    if 'NO' in msg.text:
        bot.send_message(msg.chat.id,'Invio annullato')
    else:
    # -1001681659911 è l'ID di prova
        bot.send_message(-1001921431467, msg.text)
        bot.send_message(msg.chat.id, 'Ho comunicato il messaggio')


@bot.callback_query_handler(func=lambda call: True)
def answerOnGroup(callback):
    if callback.message:
        # bot.send_message(callback.message.chat.id,'Comunicazione avvenuta')
        if callback.data == "answer_open":
            # {datetime.datetime.now().strftime("%H:%M:%S")}')
            bot.send_message(-1001921431467, f'Il laboratorio 25a è aperto')
            bot.send_message(callback.message.chat.id,
                             'Comunicazione avvenuta')
        if callback.data == "answer_close":
            bot.send_message(-1001921431467,
                             'Il laboratorio 25a è chiuso')
            bot.send_message(callback.message.chat.id,
                             'Comunicazione avvenuta')
        if callback.data == "answer_coffe":
            bot.send_message(-1001921431467, 'Il caffè è disponibile')
            bot.send_message(callback.message.chat.id,
                             'Comunicazione avvenuta')
        if callback.data == "answer_nocoffe":
            bot.send_message(-1001921431467, 'Il caffè è terminato')
            bot.send_message(callback.message.chat.id,
                             'Comunicazione avvenuta')


@bot.message_handler(commands=['list'])
def listCMD(msg):
    log_obj = {
        'chat_id': msg.chat.id,
        'message_id': msg.message_id,
        'message': 'Comando lanciato: list',
        'user': msg.from_user.username,
        'command': 'list'
    }
    log_file(log_obj)
    markup = types.InlineKeyboardMarkup(row_width=2)
    bot.send_message(
        msg.chat.id, 'Ecco la lista dei comandi disponibili', reply_markup=markup)
    bot.send_message(msg.chat.id, '- Comando /msg\n Questo comando permette di inviare un messaggio preimpostato al gruppo (Admin)\n\n - Comando /com\n Questo comando permette di inviare una comunicazione al gruppo (Admin)\n\n - Comando /list\n Genera questa lista\n\n - Comando /help\n Questo comando ti permette di richiedere assistenza, su qualunque topic, direttamente ai responsabili del laboratorio, che sono: \n - @Acr0nim0 (Franco)\n - @Levvonci (Leonardo)\n - @davidenox (Davide)\n - @Spaadd (Nicolò)\n - @CromoCon (Marius)\n - @alesandu (Alessandro)\n - @Compssss (Francesco)\n')


@bot.message_handler(commands=['help'])
def help(msg):
    log_obj = {
        'chat_id': msg.chat.id,
        'message_id': msg.message_id,
        'message': 'Comando lanciato: help',
        'user': msg.from_user.username,
        'command': 'help'
    }
    log_file(log_obj)
    markup = types.InlineKeyboardMarkup(row_width=2)
    bot.send_message(
        msg.chat.id, 'Per qualunque problema/richiesta chiedi a loro : \n - @Acr0nim0 (Franco)\n - @Levvonci (Leonardo)\n - @davidenox (Davide)\n - @Spaadd (Nicolò)\n - @CromoCon (Marius)\n - @alesandu (Alessandro)\n - @Compssss (Francesco)\n')
    sendHelp = bot.send_message(
        msg.chat.id, 'Per cosa chiedi assistenza?(per favore, scrivi il messaggio completo, e non piangere).\nRicorda di scrivere il nome del responsabile a cui vuoi richiedere assistenza, separato da "to";\nLe parole chiave dei resposabili sono:\n - to franco\n - to davide\n - to leonardo\n - to nicolò\n - to marius\n - to alessandro[es. Il bot non funziona to franco]', reply_markup=markup)
    bot.register_next_step_handler(sendHelp, sendHelpFunc)


def sendHelpFunc(msg):
    markup = types.InlineKeyboardMarkup(row_width=2)
    split = msg.text.split("to ")
    if 'to franco' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Franco")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to davide' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Davide")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to leonardo' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Leonardo")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to nicolò' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Nicolò")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to marius' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Marius")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to alessandro' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Alessandro")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    elif 'to francesco' in msg.text:
        # -1001681659911 è l'ID di prova
        bot.send_message(-1001681659911,
                         f"Da LaBot, hai ricevuto una richiesta di assistenza : {split[0]}, da @{msg.from_user.username}. Richiesto l'intervento di Francesco")
        bot.send_message(
            msg.chat.id, f'Ho comunicato il messaggio a {split[1]}')
    else:
        bot.send_message(msg.chat.id, "Attento! Hai dimenticato di specificare il responsabile a cui hai chiesto assistenza.\nRipeti il comando /help e, dopo aver esposto il tuo problema, specifica il responsabile con la sintassi corretta.")


if __name__ == '__main__':
    bot.polling()
