#!/bin/bash
cd $HOME/projects/quantsmith/data && kaggle competitions download -c m5-forecasting-accuracy
unzip ./m5-forecasting-accuracy.zip
rm -rf ./m5-forecasting-accuracy.zip