import datetime
import matplotlib.pyplot as plt
import numpy as np

class Money:

	@staticmethod
	def dte_to_jd(year, month, day):

		if (month == 1) or (month == 2):
			yearp = year - 1
			monthp = month + 12
		else:
			yearp = year
			monthp = month

		if ((year < 1582) or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day < 15)):
			B = 0
		else:
			A = np.trunc(yearp / 100.)
			B = 2 - A + np.trunc(A / 4.)

		if yearp < 0:
			C = np.trunc((365.25 * yearp) - 0.75)
		else:
			C = np.trunc(365.25 * yearp)

		D = np.trunc(30.6001 * (monthp + 1))

		jd = B + C + D + day + 1720994.5

		return jd

	@staticmethod
	def get_avg(chk_list, svg_list, tot_list):

		chk_array = np.asarray(chk_list)
		svg_array = np.asarray(svg_list)
		tot_array = np.asarray(tot_list)

		chk_avg = np.mean(chk_array)
		svg_avg = np.mean(svg_array)
		tot_avg = np.mean(tot_array)

		return chk_avg, svg_avg, tot_avg

	@staticmethod
	def get_cat():

		file = open('cat.txt', 'r')

		cat_list = []

		for ln in file:
			ln = ln.split()
			cat_list.append(ln[0])

		return cat_list