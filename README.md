# Kazakh Speech Corpus 2

This repository provides the recipe for the paper [KSC2: An Industrial-Scale Open-Source Kazakh Speech Corpus](https://www.isca-speech.org/archive/pdfs/interspeech_2022/mussakhojayeva22_interspeech.pdf).

## Pre-trained models

You can download the best performing model [HERE](https://github.com/IS2AI/Kazakh_ASR/blob/main/asr_train_asr_raw_ksc2_char_sp_valid.acc.ave_10best.zip).

### Inference

To convert your audio file to text, please make sure it follows a wav format with sample rate of 16k. Unzip the pre-trained model in the current directory, and make sure that ```asr_model_path & lm_model_path``` refer to valid directories. Install the necessary packages by running ```pip install -r requirements.txt```. 
To perform the evaluation please run:
```
python recognize.py -f <path_to_your_wav>
```

## Dataset

Download ISSAI_KSC2 dataset by filling [THIS](https://docs.google.com/forms/d/e/1FAIpQLSf_usCjxTvbH_2xhA6slH9FAfjrYVd4OHnr-CUcVVW3TEAscg/viewform) form, and untar ```tar -xvf ISSAI_KSC2.tar.gz```  in the directory of your choice. Specify the path to the dataset inside espnet/egs2/Kazakh_ASR/asr1/run.sh file:
```
dataset_path=specify_path
```

## Training

Our code builds upon [ESPnet](https://github.com/espnet/espnet), and requires prior installation of the framework for DNN training. Please follow the [installation guide](https://espnet.github.io/espnet/installation.html) and put the TurkicASR folder inside `espnet/egs2/` directory. Run the traning scripts with `./run.sh`

## Citation
```
@inproceedings{mussakhojayeva22,
  author={Saida Mussakhojayeva, Yerbolat Khassanov, Huseyin Atakan Varol},
  title={KSC2: An Industrial-Scale Open-Source Kazakh Speech Corpus},
  year=2022,
  booktitle={Interspeech},
}
```
