# fashion-product-category-classification
Use text and image to classify unlabelled fashion catalog data

## Goal
Classify the fashion products by category. Add a “category” field to each product in the
product_data.json file as output.
Note:
● You are expected to spend no more than 3-4 hours on this challenge.
● You can use the language of your choice.
● You can use any technology available on the internet.

## Deliverables
Upload the following to Github:
- Code with README file
- Classification results for all 1000 fashion products added to the input json file
- Answers to the following questions:
- Why are you designing the solution in this way?
- What are the aspects that you considered when designing?
- What are the cases your solution covers, how are they covered and why are they
important?
- What are the cases your solution does not cover and what are the ways you can
extend your current solution for them?

### Why are you designing the solution in this way?
The biggest constraint of this project was to get a working solution with the most coverage and accuracy possible in a very short amount of time (3-4 hours). Given the constraints, I chose to use simple, yet quality models to make use of text and image for predicting class. Quick iteration and debugging was done in notebooks. I also focused on minimizing boiler plate code and fit most of the code into small utility functions that would implement the functionality needed.

### What are the aspects that you considered when designing?
I wanted to make use of both text and image to get the best classification performance, but didn't have a lot of time to iterate due to the time constraints. A huge constraint was the fact that the data was unlabelled. Some quick observations of the data helped me to see that simple token matching could actually provide reasonable coverage with good accuracy (~15%-20% coverage). For the image side, I felt that we would need some ML model to help process the image features. I was very lucky to find an already labelled dataset that ended up translating fairly well to the product images in this dataset. Some more of my thought process is documented in the notes below.

### What are the cases your solution covers, how are they covered and why are they important?
The current solution will provide a prediction for every item in our json data, however the coverage is not truly 100%. The text model was not able to predict on all descriptions and the image model I used did not predict all of the labels that we cared about. My solution does a great job finding products with explicit text description of the item and using that data to predict class. It also predicts very well for image labels covered, however most of the image data we trained the model with was using an image of the item itself, whereas some of our product images contain a person and other articles along with the fashion item of interest.

### What are the cases your solution does not cover and what are the ways you can extend your current solution for them?
As mentioned above, we need to improve the coverage for our model. The first thing would be to ensure we can predict all classes from an image. The best way to do this would be to human-label some of our data and train an image model much like I did in the notebook. For text, if we have human-labelled data, we can use text embedding or other features to input to a predictive model as well. An ideal model would have a text embedding and an image embedding that we feed into a network trained on our human-labelled product data. This would have 100% coverage and most likely would work well to predict even new items that were added to the catalog.

### Some of my brainstorming notes
Scoping:
The first thing I noticed right away is that the data is unlabelled. Procuring clean, labelled data is the initial bottleneck to solving the problem, so I can think of a few options:
Unsupervised clustering - cluster the dataset using some combination of text and image attributes or embedding. Then map each cluster to a tag
Might be hard to tune and also what if there is class imbalance as in the real world. I think it will be very tricky to map cluster to label
Manually Label - I could fairly quickly manually label the dataset, although I do not have any tools to quickly do this and may need to flip through urls. It would take some time and probably prohibitive to label all 1000 data points since I only have a few hours.
Find a labelled dataset or, even better, pretrained model - this method would be fastest if I can find a dataset with similar labels. "labelled fashion categories datset" google search came up with something promising: https://medium.com/data-science-insider/clothing-dataset-5b72cd7c3f1f. I think this approach will be best given the time constraint.
Cons - we don't know how the dataset will translate since most of the labelled data is of a cropped item, whereas our dataset has a lot of full-outfit images.
Rules-based - looking at the text data, it looks like we could probably do some quick, simple term-matching

Goal:
Next thing to consider is how good do we want the classification to be? No thresholds were given and we would also need to manually label the dataset to get a set of metrics (accuracy, precision, recall, etc.) to evaluate our model. I'm going to assume we're looking for a working solution that is able to classify some of these items, but no benchmarks to beat, we are going 0->1. Depending on how things go, we can either label some randomly sampled data as a test set, or just eye ball the predictions since the problem does not specify.

High-level Model
Check for rules-based text token matching (might cover 10-20% of examples based on my quick glance)
If can't use token matching, use image classifier
Write result to json


