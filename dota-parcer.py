import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import telebot

heroes = ["abaddon", "alchemist", "ancient-apparition", "anti-mage", "arc-warden", "axe",
"bane", "batrider", "beastmaster", "bloodseeker", "bounty-hunter", "brewmaster",
"bristleback", "broodmother", "centaur-warrunner", "chaos-knight", "chen", "clinkz",
"clockwerk", "crystal-maiden", "dark-seer", "dark-willow", "dawnbreaker", "dazzle",
"death-prophet", "disruptor", "doom", "dragon-knight", "drow-ranger", "earth-spirit",
"earthshaker", "elder-titan", "ember-spirit", "enchantress", "enigma", "faceless-void",
"grimstroke", "gyrocopter", "hoodwink", "huskar", "invoker", "io", "jakiro", "juggernaut",
"keeper-of-the-light", "kunkka", "legion-commander", "leshrac", "lich", "lifestealer",
"lina", "lion", "lone-druid", "luna", "lycan", "magnus", "mars", "medusa", "meepo",
"mirana", "monkey-king", "morphling", "naga-siren", "nature's-prophet", "necrophos", "night-stalker", "nyx-assassin", "ogre-magi", "omniknight", "oracle", "outworld-devourer", "pangolier", "phantom-assassin","phantom-lancer", "phoenix", "puck","pudge","pugna","queen-of-pain","razzor","riki","rubick", "sand-king","shadow-demon","shadow-fiend","shadow-shaman", "silencer",
"skywrath-mage", "slardar", "slark", "snapfire", "sniper", "spectre", "spirit-breaker", "storm-spirit", "sven", "techies", "templar-assassin", "terrorblade", "tidehunter", "timbersaw", "tinker", "tiny", "treant-protector", "troll-warlord", "tusk", "underlord", "undying", "ursa", "vengeful-spirit", "venomancer", "viper", "visage", "void-spirit", "warlock", "weaver", "windranger", "winter-wyvern", "witch-doctor", "wraith-king", "zeus"]
heroes_for_telegramm = ', '.join(heroes)

def vichlenenie(hero_name):
    lst = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = f"https://www.dotabuff.com/heroes/{hero_name}/counters"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all(class_='sortable')

    for table in tables:
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            lst.append(row.text)
    heroes_win_rates = []

    for item in lst:
        matches = re.findall(r'([a-zA-Z\s]+)(\d+\.\d+%)(\d+\.\d+%)', item)
        for match in matches:
            hero = match[0].strip()
            first_value = match[1]
            second_value = match[2]
            heroes_win_rates.append((hero, first_value, second_value))
    return heroes_win_rates

def sovpadeniya(hero_name):
    heroes = ["abaddon", "alchemist", "ancient-apparition", "anti-mage", "arc-warden", "axe",
"bane", "batrider", "beastmaster", "bloodseeker", "bounty-hunter", "brewmaster",
"bristleback", "broodmother", "centaur-warrunner", "chaos-knight", "chen", "clinkz",
"clockwerk", "crystal-maiden", "dark-seer", "dark-willow", "dawnbreaker", "dazzle",
"death-prophet", "disruptor", "doom", "dragon-knight", "drow-ranger", "earth-spirit",
"earthshaker", "elder-titan", "ember-spirit", "enchantress", "enigma", "faceless-void",
"grimstroke", "gyrocopter", "hoodwink", "huskar", "invoker", "io", "jakiro", "juggernaut",
"keeper-of-the-light", "kunkka", "legion-commander", "leshrac", "lich", "lifestealer",
"lina", "lion", "lone-druid", "luna", "lycan", "magnus", "mars", "medusa", "meepo",
"mirana", "monkey-king", "morphling", "naga-siren", "nature's-prophet", "necrophos", "night-stalker", "nyx-assassin", "ogre-magi", "omniknight", "oracle", "outworld-devourer", "pangolier", "phantom-assassin","phantom-lancer", "phoenix", "puck","pudge","pugna","queen-of-pain","razzor","riki","rubick", "sand-king","shadow-demon","shadow-fiend","shadow-shaman", "silencer",
"skywrath-mage", "slardar", "slark", "snapfire", "sniper", "spectre", "spirit-breaker", "storm-spirit", "sven", "techies", "templar-assassin", "terrorblade", "tidehunter", "timbersaw", "tinker", "tiny", "treant-protector", "troll-warlord", "tusk", "underlord", "undying", "ursa", "vengeful-spirit", "venomancer", "viper", "visage", "void-spirit", "warlock", "weaver", "windranger", "winter-wyvern", "witch-doctor", "wraith-king", "zeus"]
    if hero_name in heroes:
        return True
    else:
        return False

token = "6607460200:AAGbsPoZToRKOCt772-a_X3Rf_Uimstlo5Q"
bot = telebot.TeleBot(token)
@bot.message_handler(content_types = ['text'])
def echo_message(message):
    text = message.text
    if text=='/start':
       bot.send_message(message.chat.id, (f'Напиши любое из этих имен. Если напишешь не правильно, то просто напиши заново :)'))
       bot.send_message(message.chat.id, (f'{heroes_for_telegramm}'))
    else:
       hero_name = str(text)
       if sovpadeniya(hero_name):
           result = vichlenenie(hero_name)
           for item in result:
                 hero = item[0].lower()
                 disadvantage = item[1]
                 win_rate = item[2]
                 if float(disadvantage[:-1]) >= 1:
                     bot.send_message(message.chat.id, (f"{hero}: {win_rate} - процентов побед \n\n{disadvantage} - неудобства "))
                     bot.send_message(message.chat.id, (f'Это все что мне удалось найти о {hero_name} :)'))
                 else: 
                     bot.send_message(message.chat.id, (f'Неправильно написал героя! Напиши заново пожалуйста :)'))


bot.infinity_polling()
