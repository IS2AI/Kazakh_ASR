#!/usr/bin/env python

import sys, argparse, os, glob
from tqdm import tqdm
from pathlib import Path
import regex, re
import wave
import contextlib

seed=4

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ksc2_path')
    print(' '.join(sys.argv))
    args = parser.parse_args()
    return args

def get_duration(file_path):
    duration = None
    if os.path.exists(file_path) and Path(file_path).stat().st_size > 0:
        with contextlib.closing(wave.open(file_path,'r')) as f:
            frames = f.getnframes()
            if frames>0:
                rate = f.getframerate()
                duration = frames / float(rate)
    return duration if duration else 0
            
def get_text(path):
    with open(path, 'r') as f:
        return f.read()

def make_dict(path):
    wavs = glob.glob(path + "/*.wav")
    files = {}
    for wav in wavs:
        folder_name = wav.split('/')[-2]
        text = get_text(wav.replace('.wav', '.txt'))
        rec_id = folder_name + '_' + os.path.basename(wav)
        files[rec_id] = (wav, text)
    return files

def prep_data(data_dirs):
    files = {}
    for dir in tqdm(data_dirs):
        x = make_dict(dir)
        files.update(x)
    return files

def normalize_text(text):
    #replace = {'а':'a', 'с':'c',  'â':'a',  'í':'i', 'î':'i',  'û':'u', 'ı':'i'}
    text = text.strip()
    text  = re.sub("[\(\{\[].*?[\)\}\]]", "", text) #remove (text*) and same for [], {}
    text = re.sub('[-—–]', '-', text) # normalize hyphen
    text = text.lower()
    text = " ".join(regex.findall('\p{alpha}+', text)) # for v1
    return text

def write_dir(files, eval_dir):
    wav_format = '-r 16000 -c 1 -b 16 -t wav - downsample |'
    total_dur = 0
    path_root = os.path.join('data', eval_dir)
    os.makedirs(path_root, exist_ok=True) 
    ### files is a dict
    rec_ids = list(files.keys())
    rec_ids.sort(key=lambda x: str(x))
    
    with open(path_root + '/text', 'w', encoding="utf-8") as f1, \
    open(path_root + '/utt2spk', 'w', encoding="utf-8") as f2, \
    open(path_root + '/spk2utt', 'w', encoding="utf-8") as f3, \
    open(path_root + '/wav.scp', 'w', encoding="utf-8") as f4:    
        for rec_id in rec_ids:
            wav, text = files[rec_id]
            text = normalize_text(text)
            if len(text) > 256 or len(text) < 5: continue
            dur = get_duration(wav)
            if dur > 30 or dur < 1: continue
            if rec_id=='.': print(rec_id, wav, text)
            total_dur += dur

            f1.write(rec_id + ' ' + text + '\n')
            f2.write(rec_id + ' ' + rec_id + '\n')
            f3.write(rec_id + ' ' + rec_id + '\n')
            f4.write(rec_id + ' sox ' + wav  + ' ' + wav_format +  '\n')

    print(eval_dir, "duration:", total_dur/3600)

def main():
    args = get_args()
    data_path = args.ksc2_path
    
    for eval_dir in ['train', 'dev', 'test']:
        print('Preparing', eval_dir)
        dirs = glob.glob(data_path + '/*_'+eval_dir+'/')
        files = prep_data(dirs)
        write_dir(files, eval_dir)
    
if __name__ == "__main__":
    main()