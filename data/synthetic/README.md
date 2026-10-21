# Synthetic café data

The authoritative, reproducible seed is `backend/services/seed.py`. It creates fictional Kopi & Co., three demo identities, four inventory items and two milk offers when the business is absent. Existing data is not overwritten at restart.

| Item | Quantity | Daily usage | Threshold | Proposed order |
|---|---:|---:|---:|---:|
| Fresh milk (litres) | 18 | 12 | 3 days | 60 |
| Coffee beans (kg) | 16 | 2 | 3 days | 10 |
| Oat milk (litres) | 24 | 4 | 3 days | 24 |
| Takeaway cups (units) | 500 | 80 | 3 days | 500 |

Supplier A: RM9.50/litre, 4 days. Supplier B: RM11/litre, 1 day. Both are fictional established suppliers. Only milk has quotations in this MVP. No real customers, employees, businesses or purchases are represented.

Money is stored as integer sen. Quantities and rules use Decimal. Seed code and this documentation are original project material under Apache-2.0. Runtime databases are ignored by Git.
