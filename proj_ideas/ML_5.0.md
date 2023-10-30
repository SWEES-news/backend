# ML

### ML Research:
- 4 types of machine learning algorithms: Supervised, Semi-supervised, Unsupervised, Reinforcement
- Supervised learning = taught by example, labeled data
    - Types of analysis = Classification, Regression, Forecasting
        - Classification: In classification tasks, the machine learning program must draw a conclusion from observed values and determine to
    what category new observations belong
        - Regression: In regression tasks, the machine learning program must estimate – and understand – the relationships among variables. Regression analysis focuses on one dependent variable and a series of other changing variables – making it particularly useful for prediction and forecasting
        - Forecasting: the process of making predictions about the future based on the past and present data, and is commonly used to analyse trends.
- Semi-supervised learning = learns from labeled + unlabeled data
- Unsupervised learning = no labels, try to organize/group data based on similarities
    - Types of analysis = Clustering, Dimension Reduction
        - Clustering: Clustering involves grouping sets of similar data (based on defined criteria). It’s useful for segmenting data into several groups and performing analysis on each data set to find patterns.
        - Dimension reduction: Dimension reduction reduces the number of variables being considered to find the exact information required.
- Reinforcement learning = algorithm is provided with a set of actions, parameters, and end values; learns by rewarding desired behaviors and punishing undesired ones
- Popular ML algorithms:
    - Naïve Bayes Classifier Algorithm (Supervised Learning - Classification)
    - K Means Clustering Algorithm (Unsupervised Learning - Clustering)
    - Support Vector Machine Algorithm (Supervised Learning - Classification)
    - Linear Regression (Supervised Learning/Regression)
    - Logistic Regression (Supervised learning – Classification)
    - Artificial Neural Networks (Reinforcement Learning)
    - Decision Trees (Supervised Learning – Classification/Regression)
    - Random Forests (Supervised Learning – Classification/Regression)
    - Nearest Neighbours (Supervised Learning)



### Explanation:
One of the ways to decide which the bias of different news and articles is to base our approach on the frequencies of the different phrases and. This method also allows us to categorize different articles into different groups in future rather than just using binary classification. One initial problem that we faced with this method was that some wordings had same meanings but different intensities. So we had to add a measurement to specify the intencity(quality) into our taining. One of the suggestions was to categorize each word into three intensity level such as nutral, weak and strong. That way we can associate different weight for those. Another approach can be to come up with some weights by using a potential neural network. We are expecting to make more progress on gathwering data and agreeing on training models the coming week.