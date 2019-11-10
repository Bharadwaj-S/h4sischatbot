import pandas as pd
import string
from fuzzywuzzy import fuzz


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

def fuzzy_match(str1, str2):
	str1 = clean_text(str1)
	str2 = clean_text(str2)
	return fuzz.token_set_ratio(str1, str2)

def find_names(text, df, threshold=85):
	"""
	Returns the rows in DF whose Trade Name or Legal Name matches TEXT at least THRESHOLD%
	"""
	matches = []
	for row in df:
		row = row[1]
		score1 = fuzzy_match(row["trade_nm"], text)
		score2 = fuzzy_match(row["legal_name"], text)
		max_score = max(score1, score2)
		if (max_score > threshold):
			matches.append(row)
	return matches


def chat(text):
	"""
	Takes in a company name and returns the rows in the database that best match the Trade Name or Legal Name
	"""
	return find_names(text, data)

def bw_amt(row):
	"""
	Returns Total Backwages Agreed To Pay from ROW
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

def zipcode(row):
	"""
	Returns the zip code from ROW
	"""
	return row["zip_cd"]

def address(row):
	"""
	Returns the name and address from ROW
	"""
	name = str(row["trade_nm"])
	street = str(row["street_addr_1_txt"])
	city = str(row["cty_nm"])
	state = str(row["st_cd"])
	zipcode = str(row["zip_cd"])
	return name + ", " + street + ", " + city + ", " + state + " " + zipcode

def search_by_zip(companies, given_zip):
	"""
	Return the compaanies in COMPANIES that have zipcode GIVEN_ZIP
	"""
	results = []
	for company in companies:
		if zipcode(company) == given_zip:
			results.append(company)
	return results


def all_addresses(companies):
	"""
	Returns a numbered list of the addresses of each company in COMPANIES
	"""
	addresses = []
	for company in companies:
		addresses.append(address(company))
	return list(enumerate(addresses, 1))

def format_addresses(addresses):
	"""
	Formats the list of addresses for readability
	"""
	if not addresses:
		return "Sorry, we didn't find any results for that name. Please check for any typos."
	result = "\nHere are possible matches: \n"
	for address in addresses:
		result += str(address[0]) + ". " + str(address[1]) + "\n"
	result += "Please text back the number of the company you're interested in"
	return result

def final_response(row):
	"""
	Returns the relevant information about company from ROW
	"""
	c_name = str(row["trade_nm"])
	backwages = str(bw_amt(row))
	cmp_assessed = str(cmp_assd(row))
	case_cnt = str(case_counts(row))
	company_info = f"\n{c_name}: \nNumber of labor violations: {case_cnt} \nWages kept from employees: ${backwages} \nFines owed to government: ${cmp_assessed}"
	plug = "\nTo learn more visit www.documentedny.com"
	return company_info + plug
