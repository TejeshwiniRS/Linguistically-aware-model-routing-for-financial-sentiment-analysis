# Linguistically-aware-model-routing-for-financial-sentiment-analysis

**Team:** TrustTheTokens  
**Authors:** Tejeshwini Ramesh Subasri, Hema Poojitha Chandu, Samantha Ballesteros  
## Project Webpage

🔗 [View Project Webpage](https://samantha-ballesteros.github.io/csci5541-linguistically-aware-model-router-site/)

## Overview
Financial institutions require compute cost-efficient sentiment analysis systems to process large volumes of earnings calls, financial disclosures, and market news. While LLMs achieve strong predictive performance on financial sentiment tasks, their computational and monetary costs make full-scale deployment impractical. Smaller transformer models are significantly more efficient, but exhibit systematic failures on linguistically complex financial text. 
**The core problem is to design a deployment-aware financial sentiment classification framework that selectively routes inputs between fine-tuned small and large models to balance accuracy, latency, and computational cost.**

The main research question is:

> Can linguistic features and small-model uncertainty signals be used to decide when financial text should be routed to a larger model?

## Approach

The system uses the following pipeline:

1. Combine and preprocess financial sentiment datasets.
2. Fine-tune a small model for financial sentiment classification.
3. Fine-tune a large model for the same task.
4. Extract linguistic features from each sentence:
   - Character count
   - Token count
   - Sentence depth
   - Clause count
   - Hedging terms
   - Negation terms
   - Passive voice count
   - Flesch reading ease
   - Flesch-Kincaid grade
   - Financial entity count
   - Complexity score
5. Extract uncertainty signals from the small model:
   - Confidence
   - Entropy
   - Margin
6. Train router models to decide whether to keep the small-model prediction or escalate to the large model.
7. Compare routing performance against small-only, large-only, and oracle baselines.

## Models Used

### Small Model

- **TinyBERT-4L-312D**
- Used as the low-cost primary model.
- Handles most inputs unless the router predicts that escalation is needed.

### Large Model

- **RoBERTa-large**
- Used as the higher-capacity fallback model.
- Applied only to routed/escalated examples.

### Router Models

Several lightweight router classifiers were tested, including:

- Logistic Regression
- Random Forest
- Gradient Boosting
- SVM
- MLP

The best-performing routing strategy **Logistic Regression** was selected based on accuracy, cost, and large-model usage.

## Dataset

The project uses two Hugging Face financial sentiment datasets:

1. `financial-tweets-sentiment`
2. `financial_phrasebank`

The final dataset is processed into a three-class sentiment classification task:

- Positive
- Negative
- Neutral

A 70/15/15 split is used for training, validation, and testing.

## Repository Structure

```text
.
├── data/
│   ├── combined_data/
│   └── processed_data/
│
├── models/
│   ├── README.md
│   └── upload_to_hf.py
│
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   ├── 02_small_model_baseline.ipynb
│   ├── 03_large_model_baseline.ipynb
│   ├── 04_large_model_finetuned.ipynb
│   ├── 05_router.ipynb
│   └── 06_router_baselines
│
├── Output/
│   ├── baseline_outputs/
│   ├── eda_figures/
│   ├── model_outputs/
│   └── router_outputs/
│
├── .gitignore
└── README.md
```
### Requirements

Install the main dependencies using:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn transformers datasets torch spacy textstat
```
### How to run
Run the notebooks in the following order:
```bash
1. notebooks/01_data_cleaning_eda.ipynb
2. notebooks/02_small_model_baseline.ipynb
3. notebooks/03_large_model_baseline.ipynb
4. notebooks/04_large_model_finetuned.ipynb
5. notebooks/05_router.ipynb
```
The outputs are saved under the **Output/** directory.


