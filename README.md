# Housing Price Prediction Project

## Project Overview

This project uses data from a housing website to predict property prices. We developed a robust pipeline for scraping housing data, filling in missing values by extracting details from unstructured house descriptions and predicting house prices. Our predictive models include Random Forest Regressor (RFR) and Support Vector Regression (SVR).

## Features

- **Data Scraping**: Collect housing data programmatically from targeted housing websites.
- **Data Enrichment**: Techniques to fill in null values by processing unstructured house descriptions.
- **Predictive Analysis**: Employ RFR and SVR to build models that predict house prices.

## Model Details

### Support Vector Regression (SVR)
- **Model Description**: Our project employs SVR for regression challenges. It is effective in capturing complex relationships in the data.
- **Parameters**: Default parameters of SVR are used. SVR in scikit-learn comes with several parameters like `C`, `epsilon`, and `kernel`. Since we did not specify these, the model uses the default settings, usually sufficient for a broad range of problems.

### Random Forest Regressor (RFR)
- **Model Description**: RandomForest is an ensemble learning method known for its high accuracy and ability to run efficiently on large databases. It works well for regression tasks.
- **Parameters**: We tuned the `n_estimators` parameter to 10. This parameter defines the number of trees in the forest. The default is typically 100, but we chose 10 for our model to balance complexity and performance.

### Model Comparison and Insights
Discuss here any comparison you made between the models, their performance, or any specific insights you gained (e.g., feature importance, model accuracy).

### Note
The parameters of these models, especially for RFR, can be further tuned using techniques like Grid Search or Random Search to potentially improve the model performance based on the specific characteristics of the dataset.

## Getting Started

Follow these instructions to set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Scikit-learn: 1.2.2
- Pandas: 1.5.3
- Numpy: 1.23.5

### Installation

To clone the repository:

```shell
git clone https://github.com/ThienNguyen27/HousePricePrediction.git
