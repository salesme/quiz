# quiz
命令行版刷题程序，简洁、无声、无趣

# quiz.py功能说明
这些代码文件的主要用途是实现一个基于 SQLite 数据库的问答系统，该系统允许用户管理试题、进行答题测试，并记录答题结果。以下是该系统的主要功能：
## 1. 数据库初始化
创建两个 SQLite 数据库表：
questions：用于存储试题信息，包括题目、选项、答案以及答错次数。
quiz_records：用于记录每次答题的相关信息，如开始时间、结束时间、题目总数、正确数量、错误数量和正确率。
## 2. 试题导入
支持从 CSV 文件中导入试题到questions表中。用户可以通过输入 CSV 文件的路径来完成导入操作。
## 3. 答题功能
提供三种答题模式：
对题重温（review）：选择答错次数为 0 的题目进行答题。
错题清除（wrong）：选择答错次数大于 0 的题目进行答题。
所有题目（all）：选择所有题目进行答题。
用户可以指定本次答题的题目数量。
在答题过程中，用户输入答案后，系统会判断答案的正确性，并更新相应题目的答错次数。
答题结束后，系统会记录答题结果到quiz_records表中，并显示答题摘要，包括答题时间、题目数量、正确数量、错误数量和正确率。
## 4. 错题统计
提供错题统计信息，包括错题数量和答错总次数，并在主菜单中显示。
## 5. 答错计数重置
允许用户将所有试题的答错计数器重置为 0。
## 6. 试题删除
允许用户删除questions表中的所有试题。
## 7. 用户交互界面
通过命令行界面与用户进行交互，提供一个简单的主菜单，用户可以根据菜单提示选择不同的功能。
这段代码的主要用途是将一个 CSV 文件中的行数据转换为列数据，具体来说是将特定格式的题目及选项信息从按行存储的形式转换为按列存储的形式。以下是详细的功能说明：
# row2column.py
## 功能概述
该脚本从一个名为 `ex-rows.csv` 的输入 CSV 文件中读取数据，将其中的题目、选项（A、B、C、D）和答案信息进行重新整理，然后将整理后的数据写入到一个名为 `ex-columns.csv` 的输出 CSV 文件中。
## 详细步骤
### 1. **导入模块**：
    ```python
    import csv
    ```
    导入 `csv` 模块，用于处理 CSV 文件的读写操作。

### 2. **定义文件路径和初始化数据结构**：
    ```python
    input_file = 'ex-rows.csv'
    output_file = 'ex-columns.csv'
    result_data = []
    result_data.append(['question', 'A', 'B', 'C', 'D', 'answer'])
    current_lines = []
    ```
    - `input_file` 和 `output_file` 分别指定输入和输出文件的路径。
    - `result_data` 是一个列表，用于存储最终转换后的数据，初始时添加了标题行。
    - `current_lines` 用于临时存储当前累积的非空行。

### 3. **读取输入文件**：
    ```python
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if any(field.strip() for field in row):
                current_lines.append(row[0] if row else '')
                if len(current_lines) == 6:
                    new_row = current_lines
                    result_data.append(new_row)
                    current_lines = []
    ```
    - 逐行读取输入文件中的数据。
    - 检查每行是否为空，如果不为空，则将每行的第一个元素添加到 `current_lines` 中。
    - 当 `current_lines` 累积到 6 行时，将其作为新的一行添加到 `result_data` 中，并清空 `current_lines`。

### 4. **处理剩余不足 6 行的情况**：
    ```python
    if current_lines:
        while len(current_lines) < 6:
            current_lines.append('')
        result_data.append(current_lines)
    ```
    如果读取完文件后 `current_lines` 中还有剩余的行，但不足 6 行，则用空字符串补齐到 6 个元素，并添加到 `result_data` 中。

### 5. **写入输出文件**：
    ```python
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(result_data)
    ```
    将 `result_data` 中的所有数据写入到输出文件中。

## 总结
通过以上步骤，脚本实现了将输入 CSV 文件中的行数据转换为列数据的功能，使得题目、选项和答案信息以更清晰的列格式存储在输出文件中。
