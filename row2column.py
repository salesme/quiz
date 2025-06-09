import csv

# 输入和输出文件路径
input_file = 'ex-rows.csv'
output_file = 'ex-columns.csv'
# 存储最终转换后的数据
result_data = []
# 添加标题行
result_data.append(['question', 'A', 'B', 'C', 'D', 'answer'])

# 存储当前累积的非空行
current_lines = []

# 读取输入文件
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for row in reader:
        # 检查行是否为空（所有元素都是空字符串则为空行）
        if any(field.strip() for field in row):
            current_lines.append(row[0] if row else '')  # 只取每行的第一个元素
            # 如果累积了 6 行非空行，则进行转换
            if len(current_lines) == 6:
                # 创建新行: [题目, 选项A, 选项B, 选项C, 选项D, 答案]
                new_row = current_lines
                result_data.append(new_row)
                current_lines = []

    # 处理剩余不足 6 行的情况
    if current_lines:
        # 用空字符串补齐到 6 个元素
        while len(current_lines) < 6:
            current_lines.append('')
        result_data.append(current_lines)

# 将转换后的数据写入输出文件
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(result_data)