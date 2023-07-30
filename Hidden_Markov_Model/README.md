## Object classification using Hidden Markov Model (HMM)

### How to use
- Before starting set values in config.yaml file
```yaml
dataset_dir: "./dataset"
imgsz: 480              # dataset image size 480x480
n_train_samples_per_class: 800
n_test_samples_per_class: 200
n_state: 2              # number of classes (circle and square)
n_observations: 5       # number of points on contour of each shape
n_emission: 10          # each 180/10 = 18 degree in each bin
```

- To create circle and square images 
```python
python create_imageas.py
```

Sample images
<div align="center">
  <kbd style="width: 2px"><img src="./data/non_ideal_circle_0.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/non_ideal_circle_1.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/non_ideal_circle_2.png" height="240"></kbd>
</div>

<div align="center">
  <kbd style="width: 2px"><img src="./data/non_ideal_square_0.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/non_ideal_square_1.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/non_ideal_square_2.png" height="240"></kbd>

</div>

- To create dataset in npz format
- This script find n = n_observation points from object countour and create a dataset from points and label for each sample
```python
python create_dataset.py
```

<div align="center">
  <kbd style="width: 2px"><img src="./data/c0.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/c1.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/c2.png" height="240"></kbd>
</div>

<div align="center">
  <kbd style="width: 2px"><img src="./data/s0.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/s1.png" height="240"></kbd>
  <kbd style="width: 2px"><img src="./data/s2.png" height="240"></kbd>
</div>


- To train and test model
```python
python train.py
```


- To predict class of a given image used the saved HMM model
```python
python predict.py
python predict.py -i /path/to/image/
python predict.py -i dataset/test/circle/non_ideal_circle_51.png
```
