#!/usr/bin/env python

import sys, argparse, os, glob
from tqdm import tqdm
import regex, re
import wave

seed=4

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ksc2_path')
    print(' '.join(sys.argv))
    args = parser.parse_args()
    return args

import struct

def bytes_to_int(bytes: list) -> int:
        result = 0
        for byte in bytes:
            result = (result << 8) + byte
        return result

def get_flac_duration(filename):
    with open(filename, 'rb') as f:
        if f.read(4) != b'fLaC':
            raise ValueError('File is not a flac file')
        header = f.read(4)
        while len(header):
            meta = struct.unpack('4B', header)  # 4 unsigned chars
            block_type = meta[0] & 0x7f  # 0111 1111
            size = bytes_to_int(header[1:4])

            if block_type == 0:  # Metadata Streaminfo
                streaminfo_header = f.read(size)
                unpacked = struct.unpack('2H3p3p8B16p', streaminfo_header)
                samplerate = bytes_to_int(unpacked[4:7]) >> 4
                sample_bytes = [(unpacked[7] & 0x0F)] + list(unpacked[8:12])
                total_samples = bytes_to_int(sample_bytes)
                duration = float(total_samples) / samplerate

                return duration
            header = f.read(4)

def get_text(path):
    with open(path, 'r') as f:
        return f.read()

def make_dict(path):
    audios = glob.glob(path + "/*.flac")
    files = {}
    for audio in audios:
        folder_name = audio.split('/')[-2]
        text = get_text(audio.replace('.flac', '.txt'))
        rec_id = folder_name + '_' + os.path.basename(audio)
        files[rec_id] = (audio, text)
    return files

def prep_data(data_dirs):
    files = {}
    for d in tqdm(data_dirs):
        x = make_dict(d)
        files.update(x)
    return files

def normalize_text(text):
    text = text.strip()
    text  = re.sub("[\(\{\[].*?[\)\}\]]", "", text)
    text = re.sub('[-—–]', '-', text)
    text = text.lower()
    text = " ".join(regex.findall('\p{alpha}+', text))
    return text

def write_dir(files, eval_dir):
    formatting = '-f wav -ar 16000 -ab 16 -ac 1 - |' ## this repo assumes the input are the .flac files
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
            audio, text = files[rec_id]
            text = normalize_text(text)
            dur = get_flac_duration(audio)
            total_dur += dur

            f1.write(rec_id + ' ' + text + '\n')
            f2.write(rec_id + ' ' + rec_id + '\n')
            f3.write(rec_id + ' ' + rec_id + '\n')
            f4.write(rec_id + ' ffmpeg -i ' + audio  + ' ' + formatting +  '\n')

    print(eval_dir, "duration:", total_dur/3600)

def main():
    args = get_args()
    data_path = args.ksc2_path
    
    for eval_dir in ['train', 'dev', 'test']:
        print('Preparing', eval_dir)
        dirs = glob.glob(data_path + '/'+eval_dir.capitalize()+'/*')
        files = prep_data(dirs)
        write_dir(files, eval_dir)
    
if __name__ == "__main__":
    main()