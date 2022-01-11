# Crop Classification Using Multitemporal Sentinel Images by 1D Convolutional LSTM Model

## Requirements
```
python 3.9.7
tensorflow 2.5.0
keras 2.4.3
sklearn 0.24.2
imblearn 0.8.0
numpy 1.21.2
pandas 1.3.3
matplotlib 3.4.3
seaborn 0.11.2
gdal 3.3.2
```
## Installation

Run the code below to clone the repository to your local machine and change it to your working directory.
```
git clone https://github.com/ajigeo/convlstm-classification.git
cd convlstm-classification
```

All the libraries required for executing this code is shared as a yaml file. It can be installed by running the command,
```
conda env create -f environment.yml
```

## Usage
The code was run in Windows 10.
Run the first 5 cells, to import the libraries, read the training data, preprocess it, building the DL model and fit the model.

To plot the training accuracy and loss,
```python
from utils import plot_performance
plot_performance(model_history, 'Classification Model Performance')
```

