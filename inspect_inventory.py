
import pandas as pd

df = pd.read_csv("output/document_inventory.csv")

print("\nTotal documents:", len(df))

print("\n--- File types ---")
print(df["extension"].value_counts())

print("\n--- Largest folders by document count ---")
print(
    df.groupby("parent_folder")
      .size()
      .sort_values(ascending=False)
      .head(15)
)

print("\n--- Total storage occupied ---")
total_mb = df["file_size_bytes"].sum() / (1024 * 1024)
print(f"{total_mb:.2f} MB")

print("\n--- Missing files ---")
missing = df[~df["file_path"].apply(lambda p: __import__("os").path.exists(p))]
print("Missing:", len(missing))
