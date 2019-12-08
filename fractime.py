#!/usr/bin/env python3
import os
import sys
import re
from optparse import OptionParser
from time import localtime, strftime
from fractions import Fraction

# map numbers to words
wordmap_plural_en = {
	60: "sixtieths",
	30: "thirtieths",
	20: "twentieths",
	15: "fifteenths",
	12: "twelfths",
	10: "tenths",
	6: "sixths",
	5: "fifths",
	4: "quarters",
	3: "thirds"
}

wordmap_singular_en = {
	60: "sixtieth",
	30: "thirtieth",
	20: "twentieth",
	15: "fifteenth",
	12: "twelfth",
	10: "tenth",
	6: "sixth",
	5: "fifth",
	4: "quarter",
	3: "third",
	2: "half"
}

wordmap_de = {
	60: "sechzigstel",
	30: "dreißigstel",
	20: "zwanzigstel",
	15: "fünfzentel",
	12: "zwölftel",
	10: "zehntel",
	6: "sechstel",
	5: "fünftel",
	4: "viertel",
	3: "drittel",
	2: "halb"
}

# 1–12 for the hours and then only the numbers that are relatively prime to 60
wordmap_digits_en = {
	1: "one",
	2: "two",
	3: "three",
	4: "four",
	5: "five",
	6: "six",
	7: "seven",
	8: "eight",
	9: "nine",
	10: "ten",
	11: "eleven",
	12: "twelve",
	13: "thirteen",
	14: "fourteen",
	17: "seventeen",
	19: "nineteen",
	23: "twenty-three",
	29: "twenty-nine",
	31: "thirty-one",
	37: "thirty-seven",
	41: "fourty-one",
	43: "fourty-three",
	47: "fourty-seven",
	49: "fourty-nine",
	53: "fifty-three",
	59: "fifty-nine"
}

wordmap_digits_de = {
	1: "ein",
	2: "zwei",
	3: "drei",
	4: "vier",
	5: "fünf",
	6: "sechs",
	7: "sieben",
	8: "acht",
	9: "neun",
	10: "zehn",
	11: "elf",
	12: "zwölf",
	13: "dreizehn",
	14: "vierzehn",
	17: "siebzehn",
	19: "neunzehn",
	23: "dreiundzwanzig",
	29: "neunundzwanzig",
	31: "einunddreißig",
	37: "siebenunddreißig",
	41: "einundvierzig",
	43: "dreundvierzig",
	47: "siebenundvierzig",
	49: "neunundvierzig",
	53: "dreiundfünfzig",
	59: "neunundfünfzig"
}

def print_time(minute, hour):
	print(Fraction(minute,60), 1 if hour == 12 else hour+1)

def print_time_words(minute, hour, lang):
	# determine the fraction of the hour that's passed
	frac = Fraction(minute,60)

	# natural languages, amirite?
	if lang == "de":
		next_hour = 'eins' if hour == 0 or hour == 12 else wordmap_digits_de[hour+1]

		numerator = wordmap_digits_de[frac.numerator]
		denominator = wordmap_de[frac.denominator]

		if frac.numerator == 1:
			print(denominator, next_hour)
			sys.exit(0)

		print(numerator, denominator, next_hour)
	elif lang == "en":
		next_hour = 'one' if hour == 0 or hour == 12 else wordmap_digits_en[hour+1]
		if frac.numerator == 1:
			if frac.denominator == 2:   # half, not one-half
				print("half", next_hour)
				sys.exit(0)
			numerator = wordmap_digits_en[frac.numerator]
			denominator = wordmap_singular_en[frac.denominator]
		else:
			numerator = wordmap_digits_en[frac.numerator]
			denominator = wordmap_plural_en[frac.denominator]

		print(numerator, "-", denominator, " ", next_hour, sep="")

def main():
	# parse command line options
	parser = OptionParser()
	## pull lang from env, unless specified
	parser.set_defaults(lang=os.environ['LANG'][:2])
	parser.set_defaults(fmt="words")
	parser.add_option("-l", "--lang", dest="lang", help="valid options: 'de', 'en'")
	parser.add_option("-f", "--fmt", "--format", "-o", "--out", "--output", dest="fmt", help="valid options: 'w', 'words', 'Wörter', 'n', 'numbers', 'Ziffern', 'b', 'both', 'beides'")

	(options, args) = parser.parse_args()

	if options.lang != "de":  # we only support german and english
		options.lang = "en"

	# call localtime() just once and store the values
	cur_time = strftime("%H:%M", localtime())
	real_hour = int(cur_time.split(':')[0])
	minute    = int(cur_time.split(':')[1])

	# for testing – if a valid time was given on the command line, override the real time
	valid_time = re.compile(r"^[0-2]?[0-9]:[0-5][0-9]$")
	for arg in args:
		if valid_time.match(arg):
			real_hour = int(arg.split(':')[0])
			minute    = int(arg.split(':')[1])

	# show the digital clock – real or imagined, depending on command line input
	print("%02u:%02u" % (real_hour, minute))

	# this kind of nonsense only really makes sense when speaking in 12-hour format,
	# so limit the hour value to the first twelve before printing anything out
	hour = 12 if real_hour == 12 else real_hour % 12

	# edge case top of the hour, just print it out
	if minute == 0:
		# corner cases: 12:00 and 00:00
		if hour == 12:
			if options.lang == "de":
				print("Mittag")
				sys.exit(0)
			if options.lang == "en":
				print("12 Noon")
				sys.exit(0)
		if hour == 0:
			if options.lang == "de":
				print("Mitternacht")
				sys.exit(0)
			if options.lang == "en":
				print("12 Midnight")
				sys.exit(0)

		if options.lang == "de":
			print(str(hour), "Uhr")
			sys.exit(0)
		if options.lang == "en":
			print(str(hour), "o'clock")
			sys.exit(0)

	if options.fmt in ['n', 'numbers', 'Ziffern', 'ziffern']:
		print_time(minute, hour)
	elif options.fmt in ['w', 'words', 'Wörter', 'wörter']:
		print_time_words(minute, hour, options.lang)
	elif options.fmt in ['b', 'both', 'beides']:
		print_time(minute, hour)
		print_time_words(minute, hour, options.lang)
	else:
		print_time_words(minute, hour, options.lang)

if __name__ == "__main__":
    main()
