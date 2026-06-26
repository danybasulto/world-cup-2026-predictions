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
  
  # --- Actualizar puntos Elo ---
  elo_a = teams_dict[team_a]["elo"]
  elo_b = teams_dict[team_b]["elo"]

  # Calcular expectativa de victoria
  expect_a = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
  expect_b = 1 / (1 + 10 ** ((elo_a - elo_b) / 400))

  result = row["resultado"]

  if result == 1:
    # Gano el equipo A
    teams_dict[team_a]["last_matches"].append(3)
    teams_dict[team_b]["last_matches"].append(0)
  elif result == -1:
    # Gano el equipo B
    teams_dict[team_a]["last_matches"].append(0)
    teams_dict[team_b]["last_matches"].append(3)
  else:
    # Empate
    teams_dict[team_a]["last_matches"].append(1)
    teams_dict[team_b]["last_matches"].append(1)

  # Convertir el resultado al estandar de Elo (1, 0.5, 0)
  if result == 1:
      r_a, r_b = 1, 0
  elif result == -1:
      r_a, r_b = 0, 1
  else:
      r_a, r_b = 0.5, 0.5
  
  # Definir que tanto afecta un solo partido al historial
  K = 40 # Factor de peso
  
  # Calcular los nuevos valores de Elo
  new_elo_a = elo_a + K * (r_a - expect_a)
  new_elo_b = elo_b + K * (r_b - expect_b)
  
  # Guardar los nuevos valores actualizados
  teams_dict[team_a]["elo"] = new_elo_a
  teams_dict[team_b]["elo"] = new_elo_b

df = df.round({"elo_a": 2, "elo_b": 2, "forma_a": 2, "forma_b": 2})
df["ranking_a"] = df["ranking_a"].astype(int)
df["ranking_b"] = df["ranking_b"].astype(int)

df.to_csv("./csv/historic-matches-processed.csv", index=False)
print("Archivo guardado correctamente!")