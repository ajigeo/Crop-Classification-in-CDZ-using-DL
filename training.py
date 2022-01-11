from models import fused_model
from keras.utils.vis_utils import plot_model
from keras.callbacks import ModelCheckpoint
from utils import preprocessing_split, plot_performance, model_metrics
import pandas as pd
import numpy as np
#%%
train_data = pd.read_csv('E:/GT/clean_merge_train_points.csv')
test_data = pd.read_csv('E:/GT/clean_merge_test_points.csv')
crop_variables = train_data.columns[1:]
#indices_bands = ['ndvi', 'ppr', 'pvr', 'sipi', 'gndvi', 'lci', 'ndsi', 'ndre','ndii', 'ndwi']
vv_bands =  list(train_data.columns[23:39:2]) #['vv1','vv2','vv3','vv4','vv5','vv6','vv7','vv8']
vh_bands = list(train_data.columns[24:40:2]) #['vh1','vh2','vh3','vh4','vh5','vh6','vh7','vh8']
mss_bands = list(train_data.columns[1:13]) #['b1','b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b8a','b10','b11','b12']
#%%
X_train_vh, X_val_vh, X_test_vh, y_train, y_val,y_test = preprocessing_split(vh_bands,train_data,test_data)
X_train_vv, X_val_vv, X_test_vv, _, _, _ = preprocessing_split(vv_bands,train_data,test_data)
X_train_mss, X_val_mss, X_test_mss, _, _, _ = preprocessing_split(mss_bands,train_data,test_data)
#%%
my_fused_model = fused_model()
plot_model(my_fused_model, to_file='multiple_inputs.png', show_shapes=True,show_layer_names=False)
#%%
mc_fused = ModelCheckpoint('E:/fused_inception5.h5', monitor='val_accuracy', mode='max', verbose=0, save_best_only=True)

EPOCHS = 10
BATCH_SIZE = 643

fused_model_history = my_fused_model.fit(
	x=[X_train_vh, X_train_vv, X_train_mss], y=y_train,
	validation_data=([X_val_vh, X_val_vv, X_val_mss], y_val),
	epochs=EPOCHS,batch_size=BATCH_SIZE,
    callbacks=[mc_fused])
#%%
plot_performance(fused_model_history, 'SAR Model Performance')
#%%
fused_preds = my_fused_model.predict([X_test_vh,X_test_vv,X_test_mss])
fused_predictions = fused_preds.argmax(1)

#%%
sar_acc, sar_kappa, sar_table = model_metrics(fused_predictions,y_test)

#%%
from raster import read_image, plot_output

image_data = read_image('E:/data/sentinel-samples/june_july_aug_s1/SAR_MS_stack.tif')
raster_bands = image_data[0]
raster_bands = raster_bands.transpose(1,2,0)
transformations = image_data[2]
#%%
b1 = raster_bands[:,:,0]
b2 = raster_bands[:,:,1]
b3 = raster_bands[:,:,2]
b4 = raster_bands[:,:,3]
b5 = raster_bands[:,:,4]
b6 = raster_bands[:,:,5]
b7 = raster_bands[:,:,6]
b8 = raster_bands[:,:,7]
b8a = raster_bands[:,:,8]
b10 = raster_bands[:,:,9]
b11 = raster_bands[:,:,10]
b12 = raster_bands[:,:,11]
'''
ndvi = raster_bands[:,:,12]
ppr = raster_bands[:,:,13]
pvr = raster_bands[:,:,14]
sipi = raster_bands[:,:,15]
gndvi = raster_bands[:,:,16]
lci = raster_bands[:,:,17]
ndsi = raster_bands[:,:,18]
ndre = raster_bands[:,:,19]
ndii = raster_bands[:,:,20]
ndwi = raster_bands[:,:,21]
'''
vh1 = raster_bands[:,:,22]
vh2 = raster_bands[:,:,24]
vh3 = raster_bands[:,:,26]
vh4 = raster_bands[:,:,28]
vh5 = raster_bands[:,:,30]
vh6 = raster_bands[:,:,32]
vh7 = raster_bands[:,:,34]
vh8 = raster_bands[:,:,36]
vv1 = raster_bands[:,:,23]
vv2 = raster_bands[:,:,25]
vv3 = raster_bands[:,:,27]
vv4 = raster_bands[:,:,29]
vv5 = raster_bands[:,:,31]
vv6 = raster_bands[:,:,33]
vv7 = raster_bands[:,:,35]
vv8 = raster_bands[:,:,37]

#%% Stacking the layers into different channels
mss_stacked = np.dstack((b1,b2,b3,b4,b5,b6,b7,b8,b8a,b10,b11,b12))
reshaped_mss_stack = mss_stacked.reshape(mss_stacked.shape[0]*mss_stacked.shape[1],12,1)

vv_stacked = np.dstack((vv1,vv2,vv3,vv4,vv5,vv6,vv7,vv8))
reshaped_vv_stack = vv_stacked.reshape(vv_stacked.shape[0]*vv_stacked.shape[1],8,1)

vh_stacked = np.dstack((vh1,vh2,vh3,vh4,vh5,vh6,vh7,vh8))
reshaped_vh_stack = vh_stacked.reshape(vh_stacked.shape[0]*vh_stacked.shape[1],8,1)
#%%  Predicting Rasters
raster_preds = my_fused_model.predict([reshaped_vh_stack,reshaped_vv_stack,reshaped_mss_stack])
fusion_plot = raster_preds.argmax(1)
reshaped_fusion_plot = fusion_plot.reshape(raster_bands.shape[0],raster_bands.shape[1])

#%% Final plot
plot_output(reshaped_fusion_plot,transformations)