import pandas as pd
import string
from fuzzywuzzy import fuzz

violating_words = ["abuse","contravention","encroachment","infraction","infringement",
	"misdemeanor","negligence","offense","transgression","break","breaking","illegality",
	"misbehavior","nonobservance","rupture","trespass","wrong","transgressing","trespassing",
	"violating"]

data = pd.read_csv("Wage_theft_all_zipcodes_NYC.csv")
data = [row for row in data.iterrows()]
printables = string.printable[:62]
printables += " "
printables = set(printables)

def clean_text(txt):
	if isinstance(txt, float):
		return ""
	txt = txt.lower()
	processed_text = ""
	for c in txt:
		if c in printables:
			processed_text += c
	return processed_text

def pregen_company_names(df):
	names = set()
	for row in df:
		row = row[1]
		names.add(clean_text(row["trade_nm"]))
		names.add(clean_text(row["legal_name"]))
	return names

def fuzzy_match(str1, str2):
	str1 = clean_text(str1)
	str2 = clean_text(str2)
	return fuzz.ratio(str1, str2)

def find_name(text, df):
	best_match = None
	best_score = 0
	for row in df:
		row = row[1]
		score1 = fuzzy_match(row["trade_nm"], text)
		score2 = fuzzy_match(row["legal_name"], text)
		max_score = max(score1, score2)
		if max_score > best_score:
			best_score = max_score
			best_match = row
	if best_score > 0.7:
		return best_match
	else:
		return None


def chat(text):
	return find_name(text, data)

def bw_amt(row):
	# cmp_cols = [("cmp_assd_amt" in col) for col in row.index]
	# cmp_amt = sum(row[cmp_cols])
	return row["bw_atp_amt"]

def cmp_assd(row):
	return row["cmp_assd_cnt"]

def case_counts(row):
	return row["case_violtn_cnt"]

company_names = pregen_company_names(data)

# chat("Carma East")