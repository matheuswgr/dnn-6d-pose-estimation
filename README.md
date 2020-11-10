# 6D Pose Estimation Based on Deep Learning

## Introduction (Pivoto)  

The objective of this project is to develop a computationally efficient machine learning model for semantic segmentation based object 6D pose estimation from RGB images. 

## Theme / Scope / Motivation (Wagner)

Supervised learning, regression, semantic segmentation, input data=rgb images,
Contextualization of the problem = computer vision, focusing on intelligent manipulation robots and/or navigation in unstructured environments

## Related Work (Lobo)

Talk a little about the state of the art

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

Cloud TPU. (training time and computation (feedfoward) time)
GPU for benchmark. (training time and computation (feedfoward) time)
CPU (computation (feedfoward time))

## Bibliography

References 
