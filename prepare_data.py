from collections import deque
import math
import pandas as pd

df = pd.read_csv("./csv/historic-matches.csv")

# Diccionario para guardar las actualizaciones
teams_dict = {}

# Recorrer cada partido
for idx, row in df.iterrows():
  team_a = row["equipo_a"]
  team_b = row["equipo_b"]

  if pd.isna(row["elo_a"]):
    df.at[idx, "ranking_a"] = teams_dict[team_a]["ranking"]
    df.at[idx, "elo_a"] = teams_dict[team_a]["elo"]
    df.at[idx, "ranking_b"] = teams_dict[team_b]["ranking"]
    df.at[idx, "elo_b"] = teams_dict[team_b]["elo"]
  else:
    teams_dict[team_a] = {
      "ranking": row["ranking_a"],
      "elo": row["elo_a"],
      "last_matches": deque(maxlen=5)
    }
    teams_dict[team_b] = {
      "ranking": row["ranking_b"],
      "elo": row["elo_b"],
      "last_matches": deque(maxlen=5)
    }
  
  # --- Actualizar la forma de los equipos ---
  list_a = teams_dict[team_a]["last_matches"]
  list_b = teams_dict[team_b]["last_matches"]

  if len(list_a) > 0:
      df.at[idx, "forma_a"] = sum(list_a) / len(list_a)
  else:
      df.at[idx, "forma_a"] = 1 # valor por defecto
  
  if len(list_b) > 0:
      df.at[idx, "forma_b"] = sum(list_b) / len(list_b)
  else:
      df.at[idx, "forma_b"] = 1 # valor por defecto