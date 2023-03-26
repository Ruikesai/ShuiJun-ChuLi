import os
import re
import csv

# 定义正则表达式模式，以匹配文本中的字段
pattern = r'用户昵称：(.+)\n用户id：(.+)\n微博数：(.+)\n关注数：(.+)\n粉丝数：(.+)'

# 创建一个CSV文件并写入标题行
with open('user_data.xls', mode='w', newline='', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(['昵称', 'ID', '微博数', '关注数', '粉丝数', 'tag率', '原创率', '平均点赞', '平均转发', '平均评论'])

    # 循环读取每个txt文件
    for filename in os.listdir():
        if filename.endswith('.txt'):
            with open(filename, mode='r') as f:
                text = f.read()

                #测试
                total_likes = 0
                total_retweets = 0
                total_comments = 0

                for line in text.split('\n'):
                    if line.startswith('点赞数'):
                        num_likes = int(line.split("：")[1])
                        total_likes += num_likes

                    if line.startswith('转发数'):
                        num_retweets = int(line.split("：")[1])
                        total_retweets += num_retweets

                    if line.startswith('评论数'):
                        num_comments = int(line.split("：")[1])
                        total_comments += num_comments

                # 使用正则表达式提取字段
                match = re.search(pattern, text)

                # 如果找到匹配项，则将字段写入CSV文件中
                if match:
                    tag_lines = [line for line in text.split('\n') if line.startswith('#')]
                    ret_lines = [line for line in text.split('\n') if line.startswith('转发内容')]
                    ret_rate = len(ret_lines) * 7 / len(text.split('\n'))
                    tag_rate = len(tag_lines) * 7 / len(text.split('\n'))

                    arv_likes = total_likes * 7 / len(text.split('\n'))
                    arv_retweets = total_retweets * 7 / len(text.split('\n'))
                    arv_comments = total_comments * 7 / len(text.split('\n'))

                    writer.writerow([match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), tag_rate, 1-ret_rate, arv_likes, arv_retweets, arv_comments])
