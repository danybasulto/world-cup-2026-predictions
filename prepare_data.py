from collections import deque
import math
import pandas as pd

df = pd.read_csv("./csv/historic-matches.csv")

teams_dict = {}

# Recorrer cada partido
for idx, row in df.iterrows():
  team_a = row["equipo_a"]
  team_b = row["equipo_b"]

  if pd.isna(row["elo_a"]):
    # Si la fila esta vacia
    pass
  else:
    # Si la fila ya tiene datos
    pass