#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}

# Data preparation related
dataset_path=

log "$0 $*"


. ./utils/parse_options.sh

. ./path.sh
. ./cmd.sh


if [ $# -gt 1 ]; then
  log "${help_message}"
  exit 2
fi

log "Data Preparation"
train_dir=data/train
dev_dir=data/dev
test_dir=data/test

mkdir -p $train_dir
mkdir -p $dev_dir
mkdir -p $test_dir

# Transcriptions preparation
for dir in $train_dir $dev_dir $test_dir; do
  log Preparing $dir transcriptions
  log $dataset_path
  local/prep_data.py $dataset_path
  exit
done

log "Successfully finished. [elapsed=${SECONDS}s]"
