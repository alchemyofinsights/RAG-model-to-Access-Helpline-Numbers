import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel("../data/helplines.xlsx")

engine = create_engine("sqlite:///database.db")
df.to_sql("helplines", engine, index=False, if_exists="replace")

print("✅ Excel ingested into SQLite")
