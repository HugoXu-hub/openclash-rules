# ==========================================
# OpenClash config.ini 动态生成脚本
# ==========================================
import os
import urllib.parse

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
    "YouTube": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/YouTube.png",
    "Google": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Google.png",
    "Netflix": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Netflix.png",
    "Telegram": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Telegram.png",
    "Spotify": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Spotify.png",
    "Apple": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/Apple.png",
    "AI": "https://raw.githubusercontent.com/Vbaethon/HOMOMIX/main/Icon/Color/Large/ChatGPT.png",
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
