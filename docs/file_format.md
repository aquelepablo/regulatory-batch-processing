#File Format

##Header:
Pos 1 (01) Record Type = 'H'
Pos 2–9 (08) File Date = YYYYMMDD
Pos 10–19 (10) Sender ID = Alphanumeric
Pos 20-23 (04) File Sequence = Numeric | Sequencial File number
Pos 24-30 (07) Line Number = Numeric | Sequential line number as provided in the file (starting at 1)

##Detail:
Pos 1 (1) Record Type = 'D'
Pos 2–11 (10) Account Number = Numeric (1 validation number on mod10)
Pos 12–23 (12) Amount = Numeric (2 decimals implied)
Pos 24-30 (07) Line Number = Numeric

#Trailer:
Pos 1 (1) Record Type = 'T'
Pos 2–9 (8) Total Detail Records = Numeric
Pos 10–23 (14) Total Amount = Numeric (2 decimals implied)
Pos 24-30 (07) Line Number = Numeric

##Name Pattern
Sample file naming convention:
PAYMENTS*<SENDER>*<YYYYMMDD>\_<SEQUENCE>.dat
(Naming validation is out of scope for V1.)
i.e.: PAYMENTS_ACME_20250315_001.dat

Meaning:
PAYMENTS → business domain
ACME → sending institution
20250315 → file date
001 → daily sequence
.dat → batch extension
