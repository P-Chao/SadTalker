import os
from types import SimpleNamespace
from text2voice.txt2wave import filename_format, txt2wave_tencent
from tqdm import tqdm

def run_batch(file_csv, folder_wav, folder_img, folder_dst):
    if not os.path.exists(file_csv):
        print(f'Error: {file_csv} not exists.')
        return

    if not os.path.exists(folder_wav):
        print(f'Error: {folder_wav} not exists.')
        return

    config = SimpleNamespace()
    config.isp = 'TEN'
    config.vid = 301037

    with open(file_csv, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc='Processing'):
            filename = filename_format(isp=config.isp, gender='F', vid=config.vid, language='zh', exp='mid', text=line)
            file_wav = os.path.join(folder_wav, filename + '.avi')
            if not os.path.exists(file_wav):
                txt2wave_tencent(file_wav, line)





if __name__ == "__main__":
    run_batch(r'D:\code3\SadTalker\text2voice\dataset_txt\zh_durecdial_dev.csv', r'D:\code3\SadTalker\text2voice\dataset_wave',
              r'D:\code3\SadTalker\text2voice\dataset_img', r'D:\code3\SadTalker\text2voice\dataset_avi')