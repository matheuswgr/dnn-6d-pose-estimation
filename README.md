# 6D Pose Estimation Based on Deep Learning

## Introduction (Pivoto)  

The objective of this project is to develop a computationally efficient machine learning model for semantic segmentation based object 6D pose estimation from RGB images. 

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
