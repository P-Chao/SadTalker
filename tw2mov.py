import os
from types import SimpleNamespace
import hashlib
#from text2voice.txt2wave import filename_format, txt2wave_tencent
from tqdm import tqdm

from glob import glob


def filename_format(isp='TEN', gender='F', vid=301037, language='zh', exp='mid', speed=10, text=''):
    """
    format: ${ISP}_${gender}_${VID}_${LANGUAGE}_${EXP}_${SPEED}_${TEXT_HASH}
    example:
    ISP: ALI: aliyun
         TEN: tencent
         XUN: xunfei
         AZU: azure
    LANGUAGE: zh/en
    gender: female, male, none
    """
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    hash_id = str(md5.hexdigest())
    return f'{isp}_{gender}_V{vid:06d}_{language}_{exp}_S{speed:02d}_{hash_id}'


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

    image_dirs = glob(os.path.join(folder_img, '*.png'))

    with open(file_csv, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc='Processing'):
            filename = filename_format(isp=config.isp, gender='F', vid=config.vid, language='zh', exp='mid', text=line)
            file_wav = os.path.join(folder_wav, filename + '.wav')
            if not os.path.exists(file_wav):
                #txt2wave_tencent(file_wav, line)
                print('Error, wav file not exists')
                continue

            # images
            for file_img in image_dirs:
                _, name = os.path.split(file_img)
                name, _ = os.path.splitext(name)

                folder_result = os.path.join(folder_dst, name)
                if not os.path.exists(folder_result):
                    os.makedirs(folder_result)
                file_dst = os.path.join(folder_result, filename)

                cmd_txt = f'python inference.py --source_image {file_img} --driven_audio {file_wav} --size 512 ' \
                          f'--result_dir {file_dst}'
                os.system(cmd_txt)


if __name__ == "__main__":
    run_batch(r'D:\code3\SadTalker\text2voice\dataset_txt\zh_durecdial_dev.csv', r'D:\code3\SadTalker\text2voice\dataset_wave',
              r'D:\code3\SadTalker\examples\source_image', r'D:\code3\SadTalker\text2voice\dataset_avi')