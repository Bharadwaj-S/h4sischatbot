import pandas as pd
import string
from fuzzywuzzy import fuzz

# violating_words = ["abuse","contravention","encroachment","infraction","infringement",
# 	"misdemeanor","negligence","offense","transgression","break","breaking","illegality",
# 	"misbehavior","nonobservance","rupture","trespass","wrong","transgressing","trespassing",
# 	"violating"]

df = pd.read_csv("Wage_theft_all_zipcodes_NYC.csv")
data = [row for row in df.iterrows()]
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
	"""
	Returns cleaned list of company names from DF
	"""
	names = set()
	for row in df:
		row = row[1]
		names.add(clean_text(row["trade_nm"]))
		names.add(clean_text(row["legal_name"]))
	return names

def fuzzy_match(str1, str2):
	str1 = clean_text(str1)
	str2 = clean_text(str2)
	return fuzz.token_set_ratio(str1, str2)

def find_names(text, df):
	"""
	Returns the rows in DF whose Trade Name or Legal Name matches TEXT at least 90%
	"""
	threshold = 90
	matches = []
	for row in df:
		row = row[1]
		score1 = fuzzy_match(row["trade_nm"], text)
		score2 = fuzzy_match(row["legal_name"], text)
		max_score = max(score1, score2)
		if (max_score > threshold):
			print(f"Name: {row['trade_nm']}, Score: {max_score}")
			matches.append(row)
	return matches


def chat(text):
	"""
	Takes in a company name and returns the rows in the database that best match the Trade Name or Legal Name
	"""
	return find_names(text, data)

def bw_amt(row):
	"""
	Returns BW ATP Amount (Total Backwages Agreed To Pay) from ROW
	"""
	return row["bw_atp_amt"]

def cmp_assd(row):
	"""
	Returns Total CMP (Civil Monetary Penalties) assessments from ROW
	"""
	return row["cmp_assd_cnt"]

def case_counts(row):
	"""
	Returns the Case Violation Count from ROW
	"""
	return row["case_violtn_cnt"]


# company_names = pregen_company_names(data)
# chat("Carma East")
