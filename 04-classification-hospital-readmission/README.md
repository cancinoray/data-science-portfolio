# 04 - Hospital Readmission Classification: Logistic Regression vs a Decision Tree

I predict **30-day readmission** for diabetic hospital encounters using the UCI "Diabetes 130-US
Hospitals" dataset. After excluding hospice/expired discharges and splitting by patient (not by row),
the positive rate is **11.4%**. A plain logistic regression gets **88.8% accuracy but catches only
2.5% of readmissions** — the accuracy paradox in one line. Re-weighting the classes lifts recall to
**54.3%** at **18.2% precision** (F1 0.273, ROC-AUC 0.667), and a depth-5 decision tree lands in the
same place (recall 56.6%, F1 0.268). Prior inpatient visits are the strongest signal (odds ratio
≈1.44 per prior admission). The honest conclusion: readmission is predictable only weakly from
administrative data, and the threshold should be chosen from the cost of a missed patient versus a
false alarm, not from accuracy.

## Dataset

- Source: UCI Machine Learning Repository, *Diabetes 130-US Hospitals for Years 1999–2008*
  ([dataset page](https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008))
- Files: `diabetic_data.csv` (101,766 encounters × 50 columns) and `IDS_mapping.csv` (code lookups)
- Licence: check the UCI dataset page. The CSVs are **not committed**; `data/` is git-ignored.
- How to download: download the ZIP from the UCI page and extract both CSVs into `data/`. The notebook
  expects `data/diabetic_data.csv`.

Notes:

- One row is one **encounter**, not one patient. There are 101,766 encounters for 71,518 patients, so
  a random row split would leak patient information. I use `GroupShuffleSplit` by `patient_nbr`.
- 2,423 encounters end in death or hospice and are removed; 99,343 remain.
- `weight` (96.9% missing), `medical_specialty` (49.1%), and `payer_code` (39.6%) are dropped.
- Age brackets are converted to midpoints; ICD-9 diagnosis codes are grouped into broad chapters;
  administrative IDs are treated as categorical.

## How to run

```bash
pip install -r ../requirements.txt
jupyter notebook notebook.ipynb
```

## Key results

Holdout: 19,802 encounters, 11.2% positive, zero patient overlap with training.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic (unweighted) | **0.888** | 0.491 | 0.025 | 0.047 | 0.665 | 0.219 |
| Logistic (balanced) | 0.676 | 0.182 | 0.543 | **0.273** | **0.667** | **0.219** |
| Decision tree (depth 5) | 0.654 | 0.176 | **0.566** | 0.268 | 0.652 | 0.199 |

- **Accuracy is a trap:** the unweighted logistic model is 88.8% accurate and catches 55 of 2,216
  readmissions. It is almost always predicting "no".
- **Threshold trade-off for the balanced logistic model:**

  | Threshold | Flagged share | Precision | Recall | F1 |
  |---|---|---|---|---|
  | 0.3 | 95.2% | 0.116 | 0.987 | 0.208 |
  | 0.4 | 64.9% | 0.140 | 0.813 | 0.239 |
  | 0.5 | 33.3% | 0.182 | 0.543 | 0.273 |
  | 0.6 | 15.0% | 0.232 | 0.311 | 0.266 |
  | 0.7 | 6.4% | 0.301 | 0.172 | 0.219 |

- **Prior inpatient visits dominate:** coefficient 0.364 (odds ratio 1.44 per prior admission),
  followed by number of diagnoses, emergency visits, age, and medication count.
- **The tree does not beat the linear model** in any meaningful way; the signal is mostly additive and
  the data is noisy.

## What the notebook covers

- The three-level target and why `<30` is the positive class.
- Cleaning: death/hospice exclusions, high-missing columns, age midpoints, ICD-9 grouping, ID handling.
- Patient-level leakage and `GroupShuffleSplit` with a zero-overlap check.
- EDA of readmission by age, prior inpatient visits, medications, and length of stay.
- The accuracy paradox, class weighting, and why predicted probabilities are not calibrated risks.
- Logistic regression vs decision tree; confusion matrices, ROC, PR curves, and threshold tables.
- Coefficient interpretation and tree feature importance.
- Limitations: observational data, label simplification, missing social determinants, old data,
  fairness, calibration, and no temporal validation.

## Skills shown

- Binary classification and class imbalance
- Patient-level splitting and leakage prevention
- Logistic regression, decision trees, class weights
- Accuracy vs precision/recall/F1/ROC-AUC/PR-AUC
- Threshold selection and clinical interpretation
- Communicating a weak-but-useful model honestly
