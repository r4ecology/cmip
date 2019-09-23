
import os
rootdir = '.'


# List of possible mirrors


import urllib2

url_list = [
						"http://esgf.nccs.nasa.gov",
#			"http://distrib-coffee.ipsl.jussieu.fr/",
		"http://esgf-node.llnl.gov", 	
			"http://esgf-node.ipsl.upmc.fr", 	
			"http://esg-dn1.nsc.liu.se", 
		"http://esgf-data.dkrz.de", 	
		#	"http://esgf.esrl.noaa.gov", 	
		#	"http://esgf-node.jpl.nasa.gov", 	
			"http://esgf-index1.ceda.ac.uk",
			"http://esg.pik-potsdam.de", 
			"http://esgf.nci.org.au"

			   ]



# identify the ensemble you want
ensemble = "r1i1p1"
cli_var = "chl"
# identify the range of years you want runs for
run_start = 1986
run_end = 2005
tracker = 1
for url in url_list:
	print url

	response = urllib2.urlopen(url + "/esg-search/wget?project=CMIP5&experiment=historical&experiment=rcp85&experiment=rcp60&experiment=rcp45&variable=" + cli_var + "&time_frequency=mon&limit=10000&distrib=FALSE")	
##	response = urllib2.urlopen(url + "/esg-search/wget?project=CMIP5&experiment=rcp85&experiment=historical&experiment=rcp45&experiment=rcp60&experiment=rcp26&variable=" + cli_var + "&time_frequency=mon&limit=9000&distrib=FALSE")	response = urllib2.urlopen(url + "/esg-search/wget?project=CMIP5&experiment=rcp85&experiment=historical&experiment=rcp45&experiment=rcp60&experiment=rcp26&variable=" + cli_var + "&time_frequency=mon&limit=9000&distrib=FALSE")
	print(url + "/esg-search/wget?project=CMIP5&experiment=rcp85&variable=" + cli_var + "&time_frequency=mon&limit=9000&distrib=FALSE")

	f = open("cmip5_wget.sh", "wb")
	f.write(response.read())
	f.close()

	change_level = 1
	g = open("thetao" + str(tracker) +".sh", "wb")
	tracker = tracker + 1

	f = open("cmip5_wget.sh")

	for line in f:

		if change_level == 2 and "dataset.file.url" in line:
			change_level = 3

		if change_level == 3:
			g.write(line)	
		if change_level == 2 and ensemble in line:
#		if change_level == 2:
			orig_line = line
			year_range = line[orig_line.index(".nc") -13:orig_line.index(".nc")]
			year_start = int(year_range[:4])
			print year_start
			year_end = int(year_range[7:11])
			print year_end
			print line
	# check if file exists
			if os.path.isfile(orig_line[1:orig_line.index(".nc")+3]) == False and cli_var in orig_line:
				print "working"
				if (year_start <= run_end and year_end >= run_start) or (year_end >= run_start and year_end <= run_end):
					g.write(line)

	# Now pull out the years

		if change_level == 1:
			g.write(line)
			if "download_files" in line:
				change_level = 2
			

print "finished"
