from qqwry import QQwry
import csv



# 可配置的变量
ip_list_file = r"45102-0-80.txt"  # IP列表的文件路径
output_csv_file = r"45102-0-80.csv"  # 输出CSV文件的路径
qqwry_dat_file = r"qqwry.dat"  # qqwry.dat文件的路径

class IPInfoExtractor:
    def __init__(self, dat_file):
        self.q = QQwry()
        if not self.q.load_file(dat_file, loadindex=True):
            raise Exception("Failed to load qqwry.dat file.")
        
    def extract_info(self, ip):
        result = self.q.lookup(ip)
        if result:
            country, area = result
            for p in self.provinces:
                if p in country:
                    return {
                        "country": "中国",
                        "region": country,  # 使用原始的country字段作为地区信息
                        "isp": area,  # 使用原始的area字段作为ISP信息
                        "original_info": result  # 保存原始查询结果
                    }
            return {
                "country": country,
                "region": None,  # 如果没有匹配到省份，地区留空
                "isp": area,
                "original_info": result  # 保存原始查询结果
            }
        else:
            return None
        
    @property
    def provinces(self):
        # 定义省份和直辖市列表
        return ['黑龙江', '吉林', '辽宁', '河北', '山西', '陕西', '甘肃', '青海', '山东', '福建', '浙江', '台湾',
                '河南', '湖北', '湖南', '江西', '江苏', '安徽', '广东', '海南', '四川', '贵州', '云南', '西藏', '新疆',
                '内蒙古', '宁夏', '广西', '北京', '天津', '上海', '重庆']

def load_ip_list(ip_file):
    """加载IP列表"""
    with open(ip_file, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def save_to_csv(csv_file, data):
    """将查询结果保存到CSV文件"""
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', '国家', '地区', 'ISP', 'RAW'])
        for row in data:
            writer.writerow([row['ip'], row['country'], row.get('region', '未知'), row['isp'], row['original_info']])

def main():
    q = IPInfoExtractor(qqwry_dat_file)

    ip_list = load_ip_list(ip_list_file)
    results = []

    for ip in ip_list:
        info = q.extract_info(ip)
        if info:
            info['ip'] = ip  # 添加IP到结果字典中
            results.append(info)

    save_to_csv(output_csv_file, results)
    print(f'结果已保存到 {output_csv_file}')

if __name__ == '__main__':
    main()