# Keystroke authentication #
Authenticates a user based on his keystroke patterns on a keyboard.

Collaborators: Pourush Sood (@pourushsood), Kaustav Brahma (@15EC10026), Rajdeep Biswas (@rajdeepiitkgp), Manan Khaneja (@manankhaneja)

The data is provided as hold times for individual keys, and latencies between any and all pairs of consecutive key presses. Hold time is the time between pressing the key down and releasing it. Latency is the time between pressing two keys down successively.

These two quantities are treated as features. So there could be a maximum of 26+26x26 features. There could be less if the user does not use some pairs of letters consecutively (for latencies) or does not use some letters at all (for hold times). 

We obtain 100% accuracy for some users with a one-class svm., and above 70% for all users.

# Folders #


## File concatenation ##

* *concat.py* - Concatenates the raw data from all weeks for each roll number

## ExtractRawFeatures ##

* *hold.py* - Contains code to extract raw features (hold times and latencies) from raw data.

## common_subset ##

This folder contains code for finding the common subset of all available hold times and latencies, so that a common feature vector can be built for all users.

* *common_feature_subset.py* - finds the common subset of all available features (hold times and latencies)

## VectorGenerate ##

* *vector_generate.py* - Generates the feature vectors for all users and stores them as pickle files.

## classification ##

This folder contains code for training multiple one class SVMs for authentication of the data of each user

* *svm.py* - implements one class svm using Radial Basis Function (RBF) of one user and then classifies over other data. This is implemented using Five fold cross validation. Results are plotted.

* *svm_3Dplot.py* - Same as above but generates 3D plots

## tests ##

* average_accuracy
* average_precision
* average_recall
* 3dplot


# How to use this repository #

1. Prepare the raw data and keep them in the format specified in ./File concatenation/concat.py. Run concat.py. It will produce a folder 'output' which contains data from all weeks concatenated into one file per roll number.
2. Keep hold.py (from ExtractRawFeatures) in the same folder as 'output'. Run hold.py. It will generate hold times and latencies.
3. Keep ./common_subset/common_subset.py in the same folder as 'output'. Run common_subset.py. It will create a file 'common_feat.txt' containing the set of features (Hold times or latencies) common to all users.
4. Keep vector_generate.py in the same folder as output. Run it, to generate a n  256 x m feature vectors (n users, 256 vectors, m features from common_feat.txt) which will each be stored as separate pickles in the folder 'pickled_vectors'.
5. Keep classification/svm.py in the parent directory of pickled_vectors. It will generate results and plots inside the folder 'tests' OR Run svm_3D to see 3D plots of accuracy vs nu and gamma inside 'tests'

# To change parameters or view more results #

You can change parameters nu and gamma inside svm.py (you have to modify/comment/uncomment lines 19,20,23,24,70,71,79,78).

You can view the effect of changing the kernel by modifying line 24 of svm.py. (change the outer loop for gamma accordingly as gamma will no longer be required)

You can view more results by changing accuracy to precision/recall/sensitivity/error in line 66 of svm.py. Change graph titles accordingly.
