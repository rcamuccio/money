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

	@staticmethod
	def get_ref_jd(year):

		ref_jd = []

		for month in range(1, 13):
			jd = date_to_jd(year, month, 1)
			ref_jd.append(jd)

		return ref_jd

	@staticmethod
	def mke_plt(year, eod_jd_list, checking_list, savings_list, total_list):

		plt.figure(figsize=(10,10))

		plt.plot(eod_jd_list, total_list, color='blue', label='Total')
		plt.plot(eod_jd_list, checking_list, color='green', label='Checking')
		plt.plot(eod_jd_list, savings_list, color='red', label='Savings')

		checking_avg, savings_avg, total_avg = calculate_mean(checking_list, savings_list, total_list)

		plt.axhline(y=total_avg, xmin=0, xmax=eod_jd_list[-1], linestyle='dotted', color='blue')
		plt.axhline(y=checking_avg, xmin=0, xmax=eod_jd_list[-1], linestyle='dotted', color='green')
		plt.axhline(y=savings_avg, xmin=0, xmax=eod_jd_list[-1], linestyle='dotted', color='red')

		ref_jd_list = reference_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title(str(year) + ' Balance')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')
		plt.legend()

		plt.savefig(str(year) + '.png', dpi=400)

		return

	@staticmethod
	def get_data(nme, cat):

		file = open(nme, 'r')

		eod_list = []
		chk_list = []
		svg_list = []
		tot_list = []

		cat_tot = 0

		dte_fmt = '%Y-%m-%d'

		for ln in file:
			ln = ln.split()

			if ln[0] == 'Account':
				pass

			elif ln[3] == 'n/a':
				pass

			else:
				eod = ln[1]
				eod_dt = datetime.datetime.strptime(eod, dte_fmt)
				eod_jd = Money.dte_to_jd(eod_dt.year, eod_dt.month, eod_dt.day)
				eod_jd = float(eod_jd)
				eod_list.append(eod_jd)

				chk = ln[4]
				chk = float(chk)
				chk_list.append(chk)

				svg = ln[5]
				svg = float(svg)
				svg_list.append(svg)

				tot = ln[6]
				tot = float(tot)
				tot_list.append(tot)

				if ln[7] == cat:
					amt = ln[2]
					amt = float(amt)
					amt = abs(amt)
					cat_tot += amt

		return eod_list, chk_list, svg_list, tot_list, cat_tot

if __name__ == '__main__':

	year = 2025
	category = 'Food'
	filename = str(year) + '.txt'

	eod_list, chk_list, svg_list, tot_list, cat_tot = Money.get_data(filename, category)

	Money.mke_plt(year, eod_list, chk_list, svg_list, tot_list)