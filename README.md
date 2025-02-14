# Harmonization

## Introduction

This code implements the entire harmonization process for the PERMEPSY project.

## Description of Files and Folders

- **input_db:** This folder contains the list of datasets that need to be harmonized.
- **aggregation:** This folder includes the names of the attributes to be harmonized from each dataset.
- **harmonization:** This folder contains the Python packages that implement the harmonization rules for each variable in every dataset.
- **variables:** This folder holds the variables that are to be harmonized.
- **Create_Metadata.ipynb:** This notebook extracts variables from each dataset to generate a new dataset. It includes the variables from the "variables" folder and retrieves the rows from each dataset using the names listed in the "aggregation" folder for each dataset and variable.
- **Harmonize.ipynb:** This notebook processes the aggregated dataset by checking value ranges, recalculating scores, homogenizing values, and deriving variables related to depression, quality of life, and completion.
