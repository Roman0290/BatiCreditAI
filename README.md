# BatiCreditAI

## Credit Scoring and Loan Optimization System

### Overview

Bati Bank, a leading financial service provider, has partnered with an eCommerce company to introduce a **Buy-Now-Pay-Later** (BNPL) service. This project aims to build a robust **Credit Scoring Model** to assess customer creditworthiness, predict default probabilities, and optimize loan terms.

This repository contains all the components required to:
1. Define risk categories for users (high-risk or low-risk).
2. Select observable features as predictors of credit risk.
3. Develop a model to assign risk probabilities to new customers.
4. Generate credit scores based on risk probabilities.
5. Optimize loan amounts and durations.

---

### Features

1. **Credit Risk Categorization**  
   Proxy variables to classify customers as high-risk or low-risk.

2. **Feature Engineering**  
   Selection of key predictors with high correlation to credit risk.

3. **Risk Probability Model**  
   Machine learning models to estimate the likelihood of default for a customer.

4. **Credit Scoring**  
   Conversion of risk probabilities into standardized credit scores.

5. **Loan Optimization**  
   Prediction of the optimal loan amount and duration for customers.

---

### Technology Stack

- **Programming Language**: Python
- **Libraries & Frameworks**:
  - Scikit-learn
  - Pandas
  - NumPy
  - MLFlow (Model management and tracking)
  - CML (CI/CD for ML pipelines)
- **Deployment**: Dockerized MLOps pipeline
- **Data**: [Xente Challenge Dataset](https://www.kaggle.com)

---

### Data Description

The dataset contains transactional and customer data fields, such as:

| Field                | Description                                                   |
|----------------------|---------------------------------------------------------------|
| TransactionId        | Unique transaction identifier                                 |
| BatchId              | Batch number assigned to transactions                        |
| AccountId            | Customer’s account ID                                        |
| SubscriptionId       | Subscription associated with the customer                    |
| ProductId            | Product purchased                                            |
| ProductCategory      | Broader category of the product                              |
| ChannelId            | Platform used (Web, Android, iOS, etc.)                      |
| Amount               | Value of the transaction                                     |
| FraudResult          | Indicates fraud status (1 - Yes, 0 - No)                     |

---



---

### Installation

Follow these steps to set up the project locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/Roman0290/BatiCreditAI.git
   cd BatiCreditAI
