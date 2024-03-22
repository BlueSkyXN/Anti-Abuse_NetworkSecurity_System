#!/bin/bash

# 定义文件夹路径
FOLDER_PATH="/home/runner/work/Anti-Abuse_NetworkSecurity_System/Anti-Abuse_NetworkSecurity_System/zip-baipiao-eu-org"

# 定义HTTP和HTTPS端口
HTTP_PORTS=(80 8080 8880 2052 2082 2086 2095)
HTTPS_PORTS=(443 2053 2083 2087 2096 8443)

# 遍历文件夹中的所有txt文件
for FILE in ${FOLDER_PATH}/*.txt; do
    # 从文件名获取端口号
    PORT=$(echo $(basename $FILE) | grep -o -E '[0-9]+' | tail -1)
    SCHEMA="http" # 默认协议为HTTP

    # 检查端口号是否在HTTPS端口数组中
    if [[ " ${HTTPS_PORTS[@]} " =~ " ${PORT} " ]]; then
        SCHEMA="https" # 如果是HTTPS端口，则修改协议为HTTPS
    fi

    # 构建输出文件名
    OUTPUT_FILE="${FOLDER_PATH}/$(basename $FILE .txt).xlsx"

    # 构建日志文件名
    LOG_FILE="/home/runner/work/Anti-Abuse_NetworkSecurity_System/Anti-Abuse_NetworkSecurity_System/log/$(basename $FILE .txt).log"

    # 运行URL Availability Checker
    python URL_Availability_Checker.py --input "$FILE" --output "$OUTPUT_FILE" --port $PORT --schema $SCHEMA >> $LOG_FILE
done