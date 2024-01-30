import os
import json
from tqdm import tqdm


def extract_durecdial(file_src, file_dst):
    if not os.path.exists(file_src):
        print(f'Error: {file_src} not exists.')
        return

    file_dst = os.path.abspath(file_dst)
    path, name = os.path.split(file_dst)
    if os.path.exists(file_dst):
        print(f'Error: overwrite file {file_dst}')
        return

    if not os.path.exists(path):
        os.makedirs(path)
    csv = open(file_dst, 'a+', encoding='utf-8')

    with open(file_src, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc='Processing'):
            y = json.loads(line)
            c = y['conversation']
            for i in range(len(c)):
                if c[i][0] == '[':
                    c[i] = c[i][4:]
                #c[i] = c[i].replace(' ', '')
                csv.write(c[i] + '\n')

    csv.close()
    return


if __name__ == "__main__":
    extract_durecdial(r'D:\DatasetAIGC\DuRecDial\dev.txt', './dataset_txt/zh_durecdial_dev.csv')
    extract_durecdial(r'D:\DatasetAIGC\DuRecDial\test.txt', './dataset_txt/zh_durecdial_test.csv')
    extract_durecdial(r'D:\DatasetAIGC\DuRecDial\train.txt', './dataset_txt/zh_durecdial_train.csv')
