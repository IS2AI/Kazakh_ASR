# Kazakh_ASR
This repository provides the recipe for the paper [KSC2: An Industrial-Scale Open-Source Kazakh Speech Corpus](link-will-be-later). 

## Setup and Requirements 

Our code builds upon [ESPnet](https://github.com/espnet/espnet), and requires prior installation of the framework. Please follow the [installation guide](https://espnet.github.io/espnet/installation.html) and put the Kazakh_ASR folder inside `espnet/egs2/` directory.

After succesfull installation of ESPnet & Kaldi, go to `Kazakh_ASR/asr1`. 

## Downloading the dataset
 
Download [ISSAI_KSC_335RS dataset](https://issai.nu.edu.kz/kz-speech-corpus/) and untar in the directory of your choice. Specify the path to the dataset inside `espnet/egs2/Kazakh_ASR/asr1/run.sh` file:
```
dataset_path=/path_to_dataset/
```

## Training

To train the models, run the script `./run.sh` inside `Kazakh_ASR/asr1/` folder.

## Pre-trained model

You can find the link to the latest pre-trained Transformer model [here](https://issai.nu.edu.kz/wp-content/uploads/2020/10/model.tar.gz). Untar it in `Kazakh_ASR/asr1/`. 

## Inference
To decode a single audio, specify wav file as well as the path of the pretrained models in `recognize.py` script.
```
asr_model_path="exp/asr_train_ksc2_raw_ksc2_char_sp" ### path to asr_model
lm_model_path="exp/lm_train_lm_ksc2_char" ### path to LM
wav_file='path_to_wav_to_be_recognized' ### wav file to be recognized; sample rate=16k
```
Then, run the following script:
```
python recognize.py
```
