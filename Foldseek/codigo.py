import json
import pandas as pd
import numpy as np

json_path = "Foldseek_2026_06_22_08_04_46.json"

with open(json_path, "r") as f:
    data = json.load(f)

rows = []

for block in data:
    for result in block.get("results", []):
        db = result.get("db")
        alignments = result.get("alignments", {})

        all_alignments = []

        if isinstance(alignments, dict):
            for key, value in alignments.items():
                if isinstance(value, list):
                    all_alignments.extend(value)

        for aln in all_alignments:
            if aln.get("taxName") == "Homo sapiens" or aln.get("taxId") == 9606:

                accessions = []
                for h in aln.get("href", []):
                    if isinstance(h, dict):
                        accessions.append(f"{h.get('label')}:{h.get('accession')}")

                rows.append({
                    "database": db,
                    "target": aln.get("target"),
                    "description": aln.get("description"),
                    "accessions": "; ".join(accessions),
                    "prob": float(aln.get("prob", np.nan)),
                    "evalue": float(aln.get("eval", np.nan)),
                    "score": float(aln.get("score", np.nan)),
                    "seqId": float(aln.get("seqId", np.nan)),
                    "alnLength": int(aln.get("alnLength", 0)),
                    "qStart": aln.get("qStartPos"),
                    "qEnd": aln.get("qEndPos"),
                    "targetStart": aln.get("dbStartPos"),
                    "targetEnd": aln.get("dbEndPos"),
                    "queryLength": aln.get("qLen"),
                    "targetLength": aln.get("dbLen")
                })

df = pd.DataFrame(rows)

df = df.sort_values(
    by=["prob", "score", "alnLength"],
    ascending=[False, False, False]
)

df.to_csv("foldseek_human_candidates_preliminar.csv", index=False)

df