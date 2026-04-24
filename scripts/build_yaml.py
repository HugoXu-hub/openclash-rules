# ==========================================
# OpenClash config.ini 动态生成脚本
# ==========================================
import os
#import urllib.parse

# 1. 从 GitHub Actions 环境变量获取仓库信息，拼装私有库 Raw 链接
repo = os.environ.get('GITHUB_REPOSITORY', 'YourUsername/YourRepo')
branch = os.environ.get('GITHUB_REF_NAME', 'main')
base_url = f"https://raw.githubusercontent.com/{repo}/{branch}"

custom_rules = []

# 2. 动态解析 rules-src/rules.list 中的 [Custom_link]
try:
    with open('rules-src/rules.list', 'r', encoding='utf-8') as f:
        in_custom = False
        for line in f:
            line = line.strip()
            if line == '[Custom_link]':
                in_custom = True
                continue
            elif line.startswith('['):
                in_custom = False
                continue
            
            if in_custom and line and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    # 直接拼装私有仓库中清洗好的文件链接
                    local_repo_url = f"{base_url}/rules/{name}.list"
                    custom_rules.append({'name': name, 'url': local_repo_url})
except FileNotFoundError:
    print("⚠️ 未找到 rules-src/rules.list，请检查目录结构。")

# 3. 开始拼装 INI 配置文件
ini_content = "[custom]\n;国内-国外分流\n\n;规则集定义\n"

# 优先级 1 & 2：自定义直连和代理
ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct_custom.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy_custom.list\n"

# 优先级 3：动态浮动插入 Custom_link (Google, YouTube 等)
for rule in custom_rules:
    ini_content += f"ruleset={rule['name']},{rule['url']}\n"

# 优先级 4 & 5：处理后的基础通用 Direct 和 Proxy
ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy.list\n"

# 优先级 6：兜底规则
ini_content += "ruleset=🟢 全球直连,[]GEOSITE,CN\n"
ini_content += "ruleset=🟢 全球直连,[]GEOIP,CN,no-resolve\n"
ini_content += "ruleset=🚀 节点选择,[]FINAL\n\n\n"

# ==========================================
# 策略组及图标定义字典
# ==========================================
# 这里的 Key 必须与 rules.list 中 [Custom_link] 定义的名称完全一致
icon_mapping = {
    "AI": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AI.png",
    "AI_Tree": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AI_Tree.png",
    "AI_bot": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AI_bot.png",
    "AI_voice": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AI_voice.png",
    "ASIA": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/ASIA.png",
    "Adblock": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Adblock.png",
    "AdblockPlus": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AdblockPlus.png",
    "AdblockPlus_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/AdblockPlus_2.png",
    "Adguard": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Adguard.png",
    "Adobe": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Adobe.png",
    "Amazon": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Amazon.png",
    "Apple": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple.png",
    "Apple_TV": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple_TV.png",
    "Apple_black": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple_black.png",
    "Apple_rainbow": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple_rainbow.png",
    "Auto_Link": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Auto_Link.png",
    "BT_Bittorrent": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/BT_Bittorrent.png",
    "Bahamut": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bahamut.png",
    "Bahamut_b": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bahamut_b.png",
    "Bahamut_i": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bahamut_i.png",
    "Bilibili": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bilibili.png",
    "Bilibili_Global": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bilibili_Global.png",
    "Bilibili_blue": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bilibili_blue.png",
    "Binance": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Binance.png",
    "Bing": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bing.png",
    "Bitcoin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bitcoin.png",
    "Bluesky": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bluesky.png",
    "Bytedance": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Bytedance.png",
    "Calcifer": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Calcifer.png",
    "Chained": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Chained.png",
    "Chained_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Chained_2.png",
    "ChatGPT": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/ChatGPT.png",
    "China": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/China.png",
    "China_Taipei": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/China_Taipei.png",
    "Claud": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Claud.png",
    "Cloud": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Cloud.png",
    "CloudFlare": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/CloudFlare.png",
    "Consistent_Hashing": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Consistent_Hashing.png",
    "Crypto": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Crypto.png",
    "DIRECT": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/DIRECT.png",
    "Discord": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Discord.png",
    "Disney": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Disney.png",
    "Disney_Castle": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Disney_Castle.png",
    "Disney_Channel": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Disney_Channel.png",
    "Disney_Mickey": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Disney_Mickey.png",
    "Disney_plus": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Disney_plus.png",
    "Dolphin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Dolphin.png",
    "Douyin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Douyin.png",
    "Download": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Download.png",
    "Download_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Download_2.png",
    "EPIC": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/EPIC.png",
    "Emby": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Emby.png",
    "European_Union": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/European_Union.png",
    "F2C": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/F2C.png",
    "FCM_Firebase_Cloud_Messaging": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/FCM_Firebase_Cloud_Messaging.png",
    "Facebook": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Facebook.png",
    "Failover": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Failover.png",
    "Fast": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Fast.png",
    "Fish": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Fish.png",
    "Fish_b": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Fish_b.png",
    "Fish_x": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Fish_x.png",
    "Flight": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Flight.png",
    "Forbidden": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Forbidden.png",
    "GFW": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/GFW.png",
    "GOG": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/GOG.png",
    "Game": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Game.png",
    "GitHub": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/GitHub.png",
    "Global": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Global.png",
    "Globefish": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Globefish.png",
    "Gmail": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Gmail.png",
    "Google": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Google.png",
    "HBO_MAX": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/HBO_MAX.png",
    "Home": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Home.png",
    "Hong_Kong": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Hong_Kong.png",
    "Hugging_face": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Hugging_face.png",
    "Hugging_face_g": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Hugging_face_g.png",
    "Hulu": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Hulu.png",
    "Infuse": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Infuse.png",
    "Instagram": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Instagram.png",
    "Japan": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Japan.png",
    "Jellyfin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Jellyfin.png",
    "Link": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Link.png",
    "Linkedin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Linkedin.png",
    "Linkedin_ray": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Linkedin_ray.png",
    "Load_balancing": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Load_balancing.png",
    "Load_balancing_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Load_balancing_2.png",
    "Load_balancing_3": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Load_balancing_3.png",
    "Location": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Location.png",
    "MLB": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/MLB.png",
    "Magic_Timer": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Magic_Timer.png",
    "Mail": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Mail.png",
    "Messenger": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Messenger.png",
    "Meta_1": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Meta_1.png",
    "Microsoft": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Microsoft.png",
    "Microsoft_365": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Microsoft_365.png",
    "Microsoft_Copilot": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Microsoft_Copilot.png",
    "NBA": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/NBA.png",
    "Netflix": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Netflix.png",
    "Netflix_b": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Netflix_b.png",
    "Network": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Network.png",
    "Network_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Network_2.png",
    "Niche_Link": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Niche_Link.png",
    "Niconico": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Niconico.png",
    "Niconico_Live": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Niconico_Live.png",
    "Niconico_Manga": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Niconico_Manga.png",
    "Olympics": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Olympics.png",
    "Omission": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Omission.png",
    "OneDrive": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/OneDrive.png",
    "Onlyfans": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Onlyfans.png",
    "Other": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Other.png",
    "Outlook": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Outlook.png",
    "Palestine": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Palestine.png",
    "Panda": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Panda.png",
    "Panda_WWF": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Panda_WWF.png",
    "Panda_ai": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Panda_ai.png",
    "PayPal": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/PayPal.png",
    "PayPal_business": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/PayPal_business.png",
    "Peacook": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Peacook.png",
    "Perplexity": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Perplexity.png",
    "Pig": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Pig.png",
    "Piggies": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Piggies.png",
    "Piggies_b": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Piggies_b.png",
    "Pixiv": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Pixiv.png",
    "Playstation": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Playstation.png",
    "Playstation_30th": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Playstation_30th.png",
    "Playstation_remote": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Playstation_remote.png",
    "Plex": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Plex.png",
    "Pornhub": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Pornhub.png",
    "Prime": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Prime.png",
    "Qoura": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Qoura.png",
    "Reddit": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Reddit.png",
    "Remote": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Remote.png",
    "Round_Robin": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Round_Robin.png",
    "SNS": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/SNS.png",
    "Scholar": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Scholar.png",
    "Seancody": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Seancody.png",
    "Server": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Server.png",
    "Settings": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Settings.png",
    "Signal_Light": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Signal_Light.png",
    "Singapore": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Singapore.png",
    "Sony_Live": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Sony_Live.png",
    "South_Korea": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/South_Korea.png",
    "SpeedTest": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/SpeedTest.png",
    "Spotify": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Spotify.png",
    "Steam": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Steam.png",
    "Stream": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Stream.png",
    "Taiwan_Province": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Taiwan_Province.png",
    "Telegram": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Telegram.png",
    "Threads": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Threads.png",
    "Tick": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Tick.png",
    "Tick_2": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Tick_2.png",
    "TikTok": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/TikTok.png",
    "Transfer": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Transfer.png",
    "Twitch": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Twitch.png",
    "Twitter": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Twitter.png",
    "UBISOFT": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/UBISOFT.png",
    "UK": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/UK.png",
    "USA": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/USA.png",
    "Video_Vimeo": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Video_Vimeo.png",
    "Vimeo": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Vimeo.png",
    "Weibo": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Weibo.png",
    "WhatsApp": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/WhatsApp.png",
    "X": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/X.png",
    "Xbox": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Xbox.png",
    "Xianyu": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Xianyu.png",
    "Yin_Yang": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Yin_Yang.png",
    "YouTube": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/YouTube.png",
    "Zoho_new": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Zoho_new.png",
    "Zoho_old": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Zoho_old.png",
    "Zune": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Zune.png",
    "xHamster": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/xHamster.png",
}

ini_content += ";策略组定义\n"

# 动态生成 Custom_link 的策略组并附加图标
for rule in custom_rules:
    name = rule['name']
    base_group_str = f"custom_proxy_group={name}`select`[]♻️ 自动选择`[]DIRECT`.*"
    
    if name in icon_mapping:
        icon_url = icon_mapping[name]
        # select 策略组需要跳过 4 个中间参数，用 ```` 占位
        ini_content += f"{base_group_str}````{icon_url}\n"
    else:
        ini_content += f"{base_group_str}\n"

ini_content += "custom_proxy_group=🚀 节点选择`select`[]♻️ 自动选择`[]DIRECT`.*\n"
ini_content += "custom_proxy_group=🟢 全球直连`select`[]DIRECT\n"
ini_content += "custom_proxy_group=♻️ 自动选择`url-test`.*`http://www.gstatic.com/generate_204`300,,50\n\n"

# 核心开关
ini_content += "enable_rule_generator=true\n"
ini_content += "overwrite_original_rules=true\n"

# 输出到 config/config.ini
os.makedirs('config', exist_ok=True)
with open('config/config.ini', 'w', encoding='utf-8') as f:
    f.write(ini_content)
