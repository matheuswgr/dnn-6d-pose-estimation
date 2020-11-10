# 6D Pose Estimation Based on Deep Learning

## Introduction (Pivoto)  

Object detection has always been an important problem in computer vision. This problem like many others, witnesses a large shift due to the advent of deep learning. With focus on intelligent manipulation robots applications, the objective of this project is to develop a computationally efficient machine learning model for semantic segmentation based object 6D pose estimation from RGB images.  

## Theme / Scope / Motivation (Wagner)

Supervised learning, regression, semantic segmentation, input data=rgb images,
Contextualization of the problem = computer vision, focusing on intelligent manipulation robots and/or navigation in unstructured environments

## Related Work (Lobo)

There are plenty of publications about the subject with numerous approaches. For examples, some networks developed for the task are PoseNet, PoseCNN and PVNet. All of them use CNNs in their architecture (first introduced by PoseNet).

However, the way that the network reaches to a final 6D pose value varies in each net. PoseNet directly regress a 6D camera pose from a single RGB image, PoseCNN localizes the object in the 2D image and predicts their depths to obtain the full pose while PVNet uses a keypoint-based method. These are only some examples of nets.
The PVNet that was published in 2018 has reached the impressive 86.27% accuracy using average 3D distance of model points (ADD) metrics with a modification to consider symmetric objects (ADD-S) in LINEMOD dataset.


## Goals (Wagner)

Our goal is to achieve accuracies up to +-1% of related work speedup greater than 1 (understand tradeoffs). Como saída uma análise de sensibilidade da acurácia e da velocidade em função de alguma técnicas de otimização.
What we expect to see as results?

## Methodology (Pivoto)
With our dataset, the first part will consist of training a convolutional network for semantic labeling (encoder and decoder) and evaluete its metrics. After that, the plan is to use this network together with a linear regression model for the pose estimation and, again, evaluate its metrics. With the base of our process defined, the goal is to apply each technique of optmization separatly, determinining the sensibility and calibration of hyperparameters and evalueting its metrics. Finally, after refining the whole process, we will apply all of the techniques together and assess the final results.

Pegar o dataset
Treinar uma rede convolucional pra segmentação semantica (encoder e decoder)
avaliar os resultados (métricas)
utilizar essa rede em conjunto com um modelo de regressão para realizar a estimação de pose
avaliar os resultados (métricas)
aplicar cada técnica de otimização separada
sensibilidade e calibração de hiperparâmetros
avaliar resultados (métricas)
sensibilidade e calibração de hiperparâmetros
aplicar todas as técnicas em conjunto
avaliar resultados (métricas)

How are we going to proceed to achieve our goals?

## Tools (Wagner)

Keras, tensorflow, google colab, linemod, linemod occluded.
Frameworks, datasets, libraries etc.

## Hardware Specs (Lobo)

Cloud TPU and GPU provided in Google Colab will be used. The goal is evaluate training time and computation (feedfoward) time in GPU and TPU and also evaluate the feedfoward time in CPU. 

## Bibliography

References 
