import pandas as pd
import re

# Load the Excel file
df = pd.read_excel("cleaned_data.xlsx")


# Function to extract unit from serving size
def extract_unit(serving_size):
    if isinstance(serving_size, str):
        match = re.match(r"\d*\.?\d+\s*(\D+)", serving_size.strip())
        if match:
            return match.group(1).strip().lower()
    return "unknown"  # If regex fails, assume unknown unit


# Apply function to extract units
df["ExtractedUnit"] = df["servingsize"].apply(extract_unit)

# Count occurrences of units excluding 'g' and 'ml'
unit_counts = df["ExtractedUnit"].value_counts()
non_g_ml_units = unit_counts.drop(labels=["g", "ml", "grams"], errors="ignore")

# Display results
total = 0

for unit, count in non_g_ml_units.items():
    print(f"{unit}: {count}")
    total += count

print(total)
# print(non_g_ml_units)
