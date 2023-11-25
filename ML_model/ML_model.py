import pandas as pd
from fpgrowth_py import fpgrowth
import os
import datetime

df = pd.read_csv(os.getenv("DATASET_PATH"))

df_playlists = df.groupby("pid").agg(lambda x: list(set(x)))["track_name"]
playlists = [p for p in df_playlists]

freqItemSet, rules = fpgrowth(playlists, minSupRatio=0.1, minConf=0.1)

playlists_and_pids = df_playlists.to_dict()
new_rules = []
for rule in rules:
  new_rule = rule
  new_rule.append([])
  for pid, songs in playlists_and_pids.items():
    if rule[1].issubset(set(songs)):
      new_rule[3].append(int(pid))
  new_rules.append(new_rule)

class Model:
  def __init__(self, rules, freqItemSet, version):
    self.rules = rules
    self.freqItemSet = freqItemSet
    self.model_date = datetime.datetime.now()
    self.version = version
  def predict(self, songs):
    most_freq_pids = {}
    for rule in self.rules:
      if rule[0].issubset(set(songs)):
        for pid in rule[3]:
          if most_freq_pids.get(pid):
            most_freq_pids[pid]+=1
          else:
            most_freq_pids[pid]=1
    recommendation = sorted(most_freq_pids.items(), key=lambda item: item[1], reverse=True)
    recommendation = [x[0] for x in recommendation]
    return recommendation

import dill

model = Model(new_rules, freqItemSet, os.getenv("MODEL_VERSION"))

with open(os.getenv("MODEL_PATH"),  'wb') as file:
  dill.dump(model, file)