#!/bin/bash
# ==========================================
# OpenClash 规则处理脚本
# ==========================================

echo "==> 开始清理和初始化目录"
# 5 & 6: 每次运行前删除 rules 和 tmp 文件夹并重建
rm -rf rules tmp config
mkdir -p rules tmp config rules-src

# 确保用户自定义文件存在，防止后续报错
touch rules-src/Proxy_custom.list rules-src/Direct_custom.list rules-src/rules.list

# 同步复制自定义文件到 rules 目录下，方便 YAML 统一调用 Raw 链接
cp rules-src/Proxy_custom.list rules/Proxy_custom.list
cp rules-src/Direct_custom.list rules/Direct_custom.list

# 定义工具函数：清理（去注释、去空行、去首尾空格、去重排序）
clean_file() {
    if [ -f "$1" ]; then
        sed -i 's/#.*//g' "$1"             # 去掉 # 及后面的注释
        sed -i 's/^[[:space:]]*//g' "$1"   # 去掉行首空格
        sed -i 's/[[:space:]]*$//g' "$1"   # 去掉行尾空格
        sed -i '/^$/d' "$1"                # 去掉空行
        sort -u "$1" -o "$1"               # 去重并排序
    fi
}

echo "==> 开始处理 [Custom_link]"
# 7 & 8: 解析 Custom_link 并处理
awk -F'|' '/^\[Custom_link\]/{flag=1; next} /^\[/{flag=0} flag && NF && !/^#/{print $1, $2}' rules-src/rules.list | while read -r name url; do
    echo "下载 Custom_link: $name"
    curl -sSL "$url" > "tmp/${name}_RAW.list"
    clean_file "tmp/${name}_RAW.list"
    cp "tmp/${name}_RAW.list" "rules/${name}.list"
done

echo "==> 开始处理 [Proxy-src_link]"
# 9: 汇总 Proxy-src_link
awk '/^\[Proxy-src_link\]/{flag=1; next} /^\[/{flag=0} flag && NF && !/^#/{print $0}' rules-src/rules.list | while read -r url; do
    curl -sSL "$url" >> "tmp/Proxy_RAW.list"
done
clean_file "tmp/Proxy_RAW.list"

echo "==> 开始处理 [Direct-src_link]"
# 10: 汇总 Direct-src_link
awk '/^\[Direct-src_link\]/{flag=1; next} /^\[/{flag=0} flag && NF && !/^#/{print $0}' rules-src/rules.list | while read -r url; do
    curl -sSL "$url" >> "tmp/Direct_RAW.list"
done
clean_file "tmp/Direct_RAW.list"

echo "==> 开始计算 Proxy 排除与去重逻辑"
# 11: 汇总 Proxy_exclude_temp.list (所有Custom RAW + Custom自定义源)
cat tmp/*_RAW.list rules-src/Proxy_custom.list rules-src/Direct_custom.list 2>/dev/null | \
    sed -e 's/#.*//g' -e 's/^[[:space:]]*//g' -e 's/[[:space:]]*$//g' -e '/^$/d' | sort > tmp/Proxy_exclude_temp.list

# 提取重复项作为 Proxy_repeat.list
uniq -d tmp/Proxy_exclude_temp.list > tmp/Proxy_repeat.list
# 生成最终唯一的 Proxy_exclude.list
uniq tmp/Proxy_exclude_temp.list > tmp/Proxy_exclude.list

# 12: 对比去重生成 rules/Proxy.list
# comm -12 提取交集(被剔除的)；comm -23 提取差集(留下的)
comm -12 tmp/Proxy_RAW.list tmp/Proxy_exclude.list > tmp/delete_proxy.list
comm -23 tmp/Proxy_RAW.list tmp/Proxy_exclude.list > rules/Proxy.list

echo "==> 开始计算 Direct 排除与去重逻辑"
# 13: 汇总 Direct_exclude_temp.list (Proxy_exclude.list + Direct_custom + rules/Proxy.list)
# 注：为了保持源文件夹纯净，输出路径调整为 tmp/Direct_exclude.list
cat tmp/Proxy_exclude.list rules-src/Direct_custom.list rules/Proxy.list 2>/dev/null | \
    sed -e 's/#.*//g' -e 's/^[[:space:]]*//g' -e 's/[[:space:]]*$//g' -e '/^$/d' | sort > tmp/Direct_exclude_temp.list

# 提取重复项作为 Direct_repeat.list
uniq -d tmp/Direct_exclude_temp.list > tmp/Direct_repeat.list
# 生成最终唯一的 Direct_exclude.list
uniq tmp/Direct_exclude_temp.list > tmp/Direct_exclude.list

# 14: 对比去重生成 rules/Direct.list
comm -12 tmp/Direct_RAW.list tmp/Direct_exclude.list > tmp/delete_direct.list
comm -23 tmp/Direct_RAW.list tmp/Direct_exclude.list > rules/Direct.list

echo "==> 规则处理完毕！"
