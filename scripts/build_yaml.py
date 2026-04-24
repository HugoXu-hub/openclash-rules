# ==========================================
# OpenClash config.ini 动态生成脚本 (方案二：正则图标注入版)
# ==========================================
import os

# 从 GitHub Actions 环境变量获取仓库信息
repo = os.environ.get('GITHUB_REPOSITORY', 'YourUsername/YourRepo')
branch = os.environ.get('GITHUB_REF_NAME', 'main')
base_url = f"https://raw.githubusercontent.com/{repo}/{branch}"

# 图标映射字典 (用于生成 proxy_config 规则)
icon_mapping = {
    "YouTube": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/YouTube.png",
    "Google": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Google.png",
    "Netflix": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Netflix.png",
    "Telegram": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Telegram.png",
    "Spotify": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Spotify.png",
    "Apple": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple.png",
    "AI": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/ChatGPT.png",
    "🚀 节点选择": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Proxy.png",
    "🟢 全球直连": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Direct.png",
    "♻️ 自动选择": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Auto.png"
}

custom_rules = []

# 解析 rules-src/rules.list 中的 [Custom_link]
if os.path.exists('rules-src/rules.list'):
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
                    local_repo_url = f"{base_url}/rules/{name}.list"
                    custom_rules.append({'name': name, 'url': local_repo_url})

# 1. 拼装 [custom] 头部和图标注入规则
ini_content = "[custom]\n;--- 图标正则注入 ---\n"
for name, icon_url in icon_mapping.items():
    # 语法: proxy_config=正则匹配名称$图标链接
    ini_content += f"proxy_config={name}${icon_url}\n"

ini_content += "\n;--- 规则集定义 ---\n"

# 2. 按照优先级拼装 ruleset
ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct_custom.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy_custom.list\n"

for rule in custom_rules:
    ini_content += f"ruleset={rule['name']},{rule['url']}\n"

ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy.list\n"
ini_content += "ruleset=🟢 全球直连,[]GEOSITE,CN\n"
ini_content += "ruleset=🟢 全球直连,[]GEOIP,CN,no-resolve\n"
ini_content += "ruleset=🚀 节点选择,[]FINAL\n\n\n"

# 3. 拼装策略组定义 (保持纯净，不带反引号占位)
ini_content += ";--- 策略组定义 ---\n"
for rule in custom_rules:
    ini_content += f"custom_proxy_group={rule['name']}`select`[]♻️ 自动选择`[]DIRECT`.*\n"

ini_content += "custom_proxy_group=🚀 节点选择`select`[]♻️ 自动选择`[]DIRECT`.*\n"
ini_content += "custom_proxy_group=🟢 全球直连`select`[]DIRECT\n"
ini_content += "custom_proxy_group=♻️ 自动选择`url-test`.*`http://www.gstatic.com/generate_204`300,,50\n\n"

# 核心开关
ini_content += "enable_rule_generator=true\n"
ini_content += "overwrite_original_rules=true\n"

# 输出到 config/config.ini
os.makedirs('config', exist_ok=True)
with open('config/config.ini', 'w', encoding='utf-8', newline='\n') as f:
    f.write(ini_content)

print("==> config.ini (方案二：图标正则版) 配置文件生成完毕！")
