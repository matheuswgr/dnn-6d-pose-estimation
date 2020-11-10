# 6D Pose Estimation Based on Deep Learning

## Introduction  

Object detection has always been an important problem in computer vision. This problem, like many others, witnesses a large shift due to the advent of deep learning. With focus on intelligent manipulation robots applications, the objective of this project is to develop a computationally efficient machine learning model for semantic segmentation based object 6D pose estimation from RGB images.  

## Theme / Scope / Motivation

This project is motivated by the aplication of computer vision to problems in intelligent robots for manipulation tasks and autonomous navigation in unstructured enviroments, where a machine must be able to classify and localize objects based on images in order to make decisions. With this applications in mind, this project aims to develop a supervised learning regression model coupled with a semantic segmentation pre-processing stage that is capable of determining the position and orientation of an object with respect to the camera from an RGB image and understand which techniques could be used to upscale the computational efficiency of the realization of such task.

## Related Work

There are plenty of publications about the subject with numerous approaches. For examples, some networks developed for the task are PoseNet, PoseCNN and PVNet. All of them use CNNs in their architecture (first introduced by PoseNet).

However, the way that the network reaches to a final 6D pose value varies in each net. PoseNet directly regress a 6D camera pose from a single RGB image, PoseCNN localizes the object in the 2D image and predicts their depths to obtain the full pose while PVNet uses a keypoint-based method. These are only some examples of nets.
The PVNet that was published in 2018 has reached the impressive 86.27% accuracy using average 3D distance of model points (ADD) metrics with a modification to consider symmetric objects (ADD-S) in LINEMOD dataset.


## Goals

The goal of the project is to apply algorithms that could upscale the training speed and the computational (feedfoward) speed of the model by a factor greater than one, using a GPU, a TPU or even a CPU, but keeping the accuracy drop smaller than 1%.

## Methodology 
With our dataset, the first part will consist of training a convolutional network for semantic labeling (encoder and decoder) and evaluate its metrics. After that, the plan is to use this network together with a regression model for the pose estimation and, again, evaluate its metrics. With the benchmark of our process defined, the goal is to apply each technique of compuational time optmization separately, determinining the sensibility and calibration of hyperparameters and evaluating its metrics. Finally, after refining the whole process, we will apply all of the techniques together and assess the final results.

## Tools

The tools that will be used in this project are tensorflow, keras, google colab, the linemod dataset and the linemod occluded dataset.

## Hardware Specs 

Cloud TPU and GPU provided in Google Colab will be used. The goal is evaluate training time and computation (feedfoward) time in GPU and TPU and also evaluate the feedfoward time in CPU. 
