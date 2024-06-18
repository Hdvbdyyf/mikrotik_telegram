import sys
from librouteros import connect
from getpass import getpass
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

JSON_FILE = 'config.json'
IP_SEARCH_ADDR = '10.1'

class Mikrotik:
    def __init__(self, ipaddr, username, password):
        self.ip = ipaddr
        self.user = username
        self.password = password
        self.con = self.connect()

    def connect(self):
        return connect(username=self.user, password=self.password, host=self.ip)

    def getIpAddresses(self):
        ip_info = self.con(cmd="/ip/address/print")
        return tuple(ip_info)
    
    def getDHCPLeases(self):
        leases = self.con(cmd="/ip/dhcp-server/lease/print")
        return tuple(leases)

    def getInterfaces(self):
        interfaces = self.con.path('interface')

# Define a few command handlers. These usually take the two arguments update and
# context.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


class WowH24Bot:
    def __init__(self, tokenid):
        # Create the Updater and pass it your bot's token.
        self.app = ApplicationBuilder().token(tokenid).build()

        self.app.add_handler(CommandHandler(["start","help"], start))
        self.app.add_handler(CommandHandler("set", set_timer))
        self.app.add_handler(CommandHandler("unset", unset))

        # Start the Bot
        self.app.run_polling()

        
if __name__ == "__main__":

    with open(os.path.join(sys.path[0], JSON_FILE), 'r') as in_file:
        conf = json.load(in_file)

    ip = conf['mikrotik_login']['ip']
    user = conf['mikrotik_login']['username']
    passwd = conf['mikrotik_login']['password']
    mik = Mikrotik(ipaddr=ip, username=user, password=passwd) 
  
    iplist = mik.getDHCPLeases()
    for item in iplist:        
        if IP_SEARCH_ADDR in item["address"]:
            print("Hostname: {} LastSeen: {} status: {} IP: {} ".format(item["host-name"], item["last-seen"], \
                                                                    item["status"], item["address"]))
            
    bot = WowH24Bot(conf['wowh24_bot_config']['token_id'])
