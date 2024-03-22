import pandas as pd
from qqwry import QQwry
import argparse
import os

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
                        "纯真_国家": "中国",
                        "纯真_地区": country,
                        "纯真_ISP": area,
                    }
            return {
                "纯真_国家": country,
                "纯真_地区": None,
                "纯真_ISP": area,
            }
        else:
            return {
                "纯真_国家": None,
                "纯真_地区": None,
                "纯真_ISP": None,
            }

    @property
    def provinces(self):
        return ['黑龙江', '吉林', '辽宁', '河北', '山西', '陕西', '甘肃', '青海', '山东', '福建', '浙江', '台湾',
                '河南', '湖北', '湖南', '江西', '江苏', '安徽', '广东', '海南', '四川', '贵州', '云南', '西藏', '新疆',
                '内蒙古', '宁夏', '广西', '北京', '天津', '上海', '重庆']

def process_excel(input_excel, output_excel, dat_file):
    extractor = IPInfoExtractor(dat_file)
    xls = pd.ExcelFile(input_excel)

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            ip_info = [extractor.extract_info(ip) for ip in df['IP']]
            ip_info_df = pd.DataFrame(ip_info)
            result_df = pd.concat([df, ip_info_df], axis=1)
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process IP addresses in an Excel file using QQwry database.")
    parser.add_argument('--input', required=True, help='Path to the input Excel file.')
    parser.add_argument('--output', required=True, help='Path to the output Excel file.')
    parser.add_argument('--dat', default='qqwry.dat', help='Path to the qqwry.dat file. Default is the current directory.')

    args = parser.parse_args()

    if not os.path.exists(args.dat):
        raise FileNotFoundError(f"The specified qqwry.dat file does not exist: {args.dat}")

    process_excel(args.input, args.output, args.dat)
