# Data Provenance

## Source

- **Publisher:** California Geologic Energy Management Division (CalGEM), California Department of Conservation
- **Request page:** <https://filerequest.conservation.ca.gov/?q=production_injection_data>

## How the data was obtained

1. On the CalGEM File Request page, I selected the files from the list of available production and injection data.
2. I submitted the request with my email address.
3. CalGEM replied by email with a link to download the requested files.

Download links from CalGEM's email (access tokens removed):

```
https://docftppub.blob.core.windows.net/temp/202106220024/2020CaliforniaOilAndGasWellQuarterlyProduction.xls
https://docftppub.blob.core.windows.net/temp/202106031401/2021CaliforniaOilAndGasWells.xls
```

- The links were valid from 2026-10-28 06:32 UTC until 2026-11-11 07:32 UTC. After they expire, the files have to be requested again.
- The folder names suggest when CalGEM published each version: `202106220024` → 2021-06-22 for the quarterly production file, and `202106031401` → 2021-06-03 for the well list.

Recorded: 2026-10-27

## Files

| File | Size | Contents |
|---|---|---|
| `2020CaliforniaOilAndGasWellQuarterlyProduction.xls` | 23.4 MB | Quarterly produced water by well and pool (form OG110Q), 2020 Q1–Q3. 307,922 rows. |
| `2021CaliforniaOilAndGasWells.xls` | 41.3 MB | Well list by well and pool: lease, field, location, operator, and status. 221,945 rows. |

## Notes

- Both files are comma-separated text (CSV) even though their extension is `.xls`.
- The files are as received from CalGEM and have not been modified.
