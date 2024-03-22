import os
import pandas as pd

def merge_xlsx_files(output_file='CF-Proxy-IP-Global-Merged.xlsx'):
    writer = pd.ExcelWriter(output_file, engine='openpyxl')

    all_data = pd.DataFrame()

    for filename in os.listdir('.'):
        # 跳过输出文件，避免尝试读取它
        if filename == output_file:
            continue

        if filename.endswith('.xlsx') and not filename.startswith('~$'):
            print(f'处理文件: {filename}')
            # 明确指定使用openpyxl引擎读取Excel文件
            df = pd.read_excel(filename, engine='openpyxl')
            all_data = pd.concat([all_data, df], ignore_index=True)

            # 将原始表格数据复制到以文件名命名的新工作表中
            df.to_excel(writer, sheet_name=os.path.splitext(filename)[0], index=False)

    # 将合并后的数据写入到名为ALL的工作表中
    all_data.to_excel(writer, sheet_name='ALL', index=False)

    # 保存并关闭ExcelWriter
    writer.close()


if __name__ == "__main__":
    merge_xlsx_files()
