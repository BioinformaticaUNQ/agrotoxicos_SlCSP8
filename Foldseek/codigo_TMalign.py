import json
import pandas as pd
import numpy as np

json_path = "Foldseek_2026_06_22_08_21_17.json"

with open(json_path, "r") as f:
    data = json.load(f)

rows = []

for block in data:
    mode = block.get("mode")

    for result in block.get("results", []):
        database = result.get("db")
        alignments = result.get("alignments", {})

        for key, value in alignments.items():
            if isinstance(value, list):
                for aln in value:
                    if aln.get("taxName") == "Homo sapiens" or aln.get("taxId") == 9606:

                        q_len = int(aln.get("qLen", 0))
                        aln_len = int(aln.get("alnLength", 0))

                        rows.append({
                            "database": database,
                            "mode": mode,
                            "target": aln.get("target"),
                            "description": aln.get("description"),
                            "taxName": aln.get("taxName"),
                            "prob": float(aln.get("prob", np.nan)),
                            "evalue": float(aln.get("eval", np.nan)),
                            "score": float(aln.get("score", np.nan)),
                            "seqId": float(aln.get("seqId", np.nan)),
                            "alnLength": aln_len,
                            "queryLength": q_len,
                            "queryCoverage": aln_len / q_len if q_len > 0 else np.nan,
                            "gapsopened": int(aln.get("gapsopened", 0)),
                            "qStart": aln.get("qStartPos"),
                            "qEnd": aln.get("qEndPos"),
                            "targetStart": aln.get("dbStartPos"),
                            "targetEnd": aln.get("dbEndPos"),
                            "href": aln.get("href")
                        })

df = pd.DataFrame(rows)
# Orden recomendado:
# mayor score, mayor probabilidad, mayor largo alineado, menor e-value
df_ranked = df.sort_values(
    by=["score", "prob", "alnLength", "evalue"],
    ascending=[False, False, False, True]
)

df_ranked.to_csv("mejores_alineamientos_foldseek_tmalign.csv", index=False)

df_ranked