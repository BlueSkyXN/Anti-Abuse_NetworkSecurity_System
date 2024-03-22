# 定义文件夹路径
$FOLDER_PATH = "zip-baipiao-eu-org"

# 定义HTTP和HTTPS端口
$HTTP_PORTS = @(80, 8080, 8880, 2052, 2082, 2086, 2095)
$HTTPS_PORTS = @(443, 2053, 2083, 2087, 2096, 8443)

# 遍历文件夹中的所有txt文件
foreach ($FILE in Get-ChildItem -Path $FOLDER_PATH -Filter "*.txt") {
    # 从文件名获取端口号
    $PORT = [regex]::Matches($FILE.BaseName, '\d+')[-1].Value
    $SCHEMA = "http" # 默认协议为HTTP

    # 检查端口号是否在HTTPS端口数组中
    if ($HTTPS_PORTS -contains $PORT) {
        $SCHEMA = "https" # 如果是HTTPS端口，则修改协议为HTTPS
    }

    # 构建输出文件名
    $OUTPUT_FILE = "$FOLDER_PATH\$($FILE.BaseName).xlsx"

    # 构建日志文件名
    $LOG_FILE = "log/$($FILE.BaseName).log"

    # 运行URL Availability Checker
    python URL_Availability_Checker.py --input "$FILE.FullName" --output "$OUTPUT_FILE" --port $PORT --schema $SCHEMA >> $LOG_FILE
}
