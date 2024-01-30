import os
import hashlib
import wave
import json
import time
import requests
from tqdm import tqdm

from request_util import request, authorization


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


def txt2wave_tencent(filename, text):
    if os.path.exists(filename):
        return

    req = request()
    req.init()
    auth = authorization()
    auth.init()

    # request_data = collections.OrderedDict()
    request_data = dict()
    request_data['Action'] = 'TextToStreamAudio'
    request_data['AppId'] = auth.AppId
    request_data['Codec'] = req.Codec
    request_data['Expired'] = int(time.time()) + auth.Expired
    request_data['ModelType'] = req.ModelType
    request_data['PrimaryLanguage'] = req.PrimaryLanguage
    request_data['ProjectId'] = req.ProjectId
    request_data['SampleRate'] = req.SampleRate
    request_data['SecretId'] = auth.SecretId
    request_data['SessionId'] = req.SessionId
    request_data['Speed'] = req.Speed
    request_data['Text'] = text#req.Text
    request_data['Timestamp'] = int(time.time())
    request_data['VoiceType'] = req.VoiceType
    request_data['Volume'] = req.Volume

    signature = auth.generate_sign(request_data=request_data)
    header = {
        "Content-Type": "application/json",
        "Authorization": signature
    }
    url = "https://tts.cloud.tencent.com/stream"

    r = requests.post(url, headers=header, data=json.dumps(request_data), stream=True)
    '''
    if str(r.content).find("Error") != -1 :
        print(r.content)
        return
    '''
    i = 1
    wavfile = wave.open(filename, 'wb')
    wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
    for chunk in r.iter_content(1000):
        if (i == 1) & (str(chunk).find("Error") != -1):
            print(chunk)
            return
        i = i + 1
        wavfile.writeframes(chunk)

    wavfile.close()


def txt2wave_batch(file_src, folder_dst, isp='TEN'):
    if not os.path.exists(file_src):
        print(f'Error: {file_src} not exists.')
        return

    if not os.path.exists(folder_dst):
        os.makedirs(folder_dst)

    with open(file_src, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc='Processing'):
            filename = filename_format(isp=isp, text=line)
            if isp == 'TEN':
                txt2wave_tencent(os.path.join(folder_dst, filename + '.wav'), line)
            else:
                continue


if __name__ == "__main__":
    txt2wave_batch(r'D:\code3\SadTalker\text2voice\dataset_txt\zh_durecdial_dev.csv', r'D:\code3\SadTalker\text2voice\dataset_wave',
                   isp='TEN')
