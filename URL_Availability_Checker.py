import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed
from openpyxl import Workbook
import argparse
from datetime import datetime
import ipaddress

def read_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def parse_response_data(response_text):
    data = {}
    for line in response_text.split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            data[key] = value
    return data

def test_ip_availability(ip, domain, port, path, expected_keyword, schema, total, index):
    print(f"正在测试IP {index}/{total}: {ip}")
    url = f"{schema}://{ip}:{port}{path}"
    headers = {'Host': domain}
    try:
        with httpx.Client(http2=True, verify=False) as client:
            response = client.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and expected_keyword in response.text:
                data = parse_response_data(response.text)
                ts = data.get('ts', '')
                utc_time = timestamp_to_utc(ts) if ts else ''
                return (ip, port, domain, '可用', data.get('ip', ''), ts, utc_time, data.get('visit_scheme', ''), data.get('uag', ''), data.get('colo', ''), data.get('http', ''), data.get('loc', ''), data.get('tls', ''), data.get('sni', ''), data.get('warp', ''), '')
            else:
                return (ip, port, domain, '不可用', '', '', '', '', '', '', '', '', '', '', '', '状态码不是200或关键字不匹配')
    except Exception as e:
        return (ip, port, domain, '不可用', '', '', '', '', '', '', '', '', '', '', '', str(e))

def timestamp_to_utc(ts):
    try:
        # 转换时间戳（秒）为UTC时间
        return datetime.fromtimestamp(float(ts), tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return ''

def write_results_to_excel(results, output_file_path):
    wb = Workbook()
    ws = wb.active
    ws.append(['IP', '端口', '域名', '可用性', '访问者IP', '时间戳', 'UTC时间', '访问协议', '用户代理', '数据中心', 'HTTP协议', '访问者地点', 'TLS版本', 'SNI状态', 'Warp状态', 'INFO'])
    for result in results:
        ws.append(result)
    wb.save(output_file_path)

def sort_results(results):
    # 对结果排序，首先按可用性（可用优先），然后按IP地址升序
    return sorted(results, key=lambda x: (x[3] != '可用', ipaddress.ip_address(x[0])))

def main(args):
    ips = read_ips_from_file(args.input)
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(test_ip_availability, ip, args.domain, args.port, args.path, args.expected_keyword, args.schema, len(ips), index+1): ip for index, ip in enumerate(ips)}
        for future in as_completed(future_to_ip):
            try:
                results.append(future.result())
            except Exception as e:
                print(e)
    
    # 排序结果
    sorted_results = sort_results(results)
    write_results_to_excel(sorted_results, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IP可用性测试工具")
    parser.add_argument("--input", help="输入文件路径", default=r"F:\Download\45102-0-80.txt")
    parser.add_argument("--output", help="输出文件路径", default=r"F:\Download\45102-0-80.xlsx")
    parser.add_argument("--domain", help="测试域名", default='dash.cloudflare.com')
    parser.add_argument("--port", help="端口号", type=int, default=80)
    parser.add_argument("--schema", help="'http' 或 'https'", default='http')
    parser.add_argument("--path", help="URL路径", default='/cdn-cgi/trace')
    parser.add_argument("--expected_keyword", help="预期响应关键字", default='gateway=off')
    args = parser.parse_args()

    main(args)
