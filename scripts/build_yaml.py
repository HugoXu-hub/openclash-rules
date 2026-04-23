# ==========================================
# OpenClash config.ini 动态生成脚本
# ==========================================
import os

# 从 GitHub Actions 环境变量获取仓库所有者、仓库名和分支，以便拼装私有库链接
repo = os.environ.get('GITHUB_REPOSITORY', 'YourUsername/YourRepo')
branch = os.environ.get('GITHUB_REF_NAME', 'main')
base_url = f"https://raw.githubusercontent.com/{repo}/{branch}"

custom_rules = []

# 16 & 17: 动态解析 rules-src/rules.list 中的 [Custom_link]
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
                # 舍弃 parts[1] 的外部链接
                # 直接拼装私有仓库中刚才 merge.sh 处理并生成的对应文件链接
                local_repo_url = f"{base_url}/rules/{name}.list"
                custom_rules.append({'name': name, 'url': local_repo_url})

# 21: 按照优先级拼装 ruleset 字符串
ini_content = "[custom]\n;国内-国外分流\n\n;规则集定义\n"
# 最高优先级：自定义直连和代理 (这里使用规则库内部路径的Raw链接)
ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct_custom.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy_custom.list\n"

# 动态浮动插入 Custom_link
for rule in custom_rules:
    ini_content += f"ruleset={rule['name']},{rule['url']}\n"

# 次级优先级：处理后的 Direct 和 Proxy
ini_content += f"ruleset=🟢 全球直连,{base_url}/rules/Direct.list\n"
ini_content += f"ruleset=🚀 节点选择,{base_url}/rules/Proxy.list\n"

# 兜底规则
ini_content += "ruleset=🟢 全球直连,[]GEOIP,CN,no-resolve\n"
ini_content += "ruleset=🚀 节点选择,[]FINAL\n\n\n"

# 拼装策略组定义
ini_content += ";策略组定义\n"
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
with open('config/config.ini', 'w', encoding='utf-8') as f:
    f.write(ini_content)

print("==> config.ini 配置文件生成完毕！")
