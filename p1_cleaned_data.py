import pandas as pd

# Load scraped CSV
df = pd.read_csv("leaders_for_wins.csv")

# Replace any '-' or blank strings with NA
df.replace("-", pd.NA, inplace=True)

# Identify invalid rows (missing Player or Wins or Year)
invalid_rows = df[df["Player"].isna() | df["Wins"].isna() | df["Year"].isna()]

# Save removed rows (just to keep track, if we didn't delete neeeded data)
invalid_rows.to_csv("leaders_for_wins_removed.csv", index=False)
print(f"Removed {len(invalid_rows)} invalid rows -> saved to leaders_for_wins_removed.csv")

# Keep only valid rows
df = df.dropna(subset=["Year", "Player", "Wins"])

# Convert Year and Wins to numeric, coercing errors to NaN (if cannot be converted to number)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Wins"] = pd.to_numeric(df["Wins"], errors="coerce")

# Filter to Year ≥ 1901 (AL is not active until 1901)
df = df[df["Year"] >= 1901]

# Strip whitespace from strings
for col in ["Player", "Team", "League"]:
    df[col] = df[col].astype(str).str.strip()

# Sort by Year then League
df = df.sort_values(by=["Year", "League"])

# Save cleaned file
df.to_csv("leaders_for_wins_cleaned.csv", index=False)
print(f"Cleaned data saved to leaders_for_wins_cleaned.csv with {len(df)} rows.")
