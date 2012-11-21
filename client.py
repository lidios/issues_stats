#!/usr/bin/python
# -*- coding: utf-8 -*
# @Lidio
# Program used to get github issues statistics


# Interessing TAGs
#TODO to parametrize
tags_to_sumarize_hours = ['Impediment', 'Incident', 'Meeting', 'Deploy'];
repository_name = "webops"
organization_name = "sambatech"
# Average hour price in real
average_hour_price = 110

#TODO
# qual é o padrao da tag td para issues?

def dict_key_inc(_dict_, _key_,_inc_value_=1):
     """Increment an entry on the dict for the given key"""
     if _key_ is not None:
         # is the first time?
         if not _dict_.has_key(_key_):
             _dict_[_key_]=_inc_value_
         else:
             _dict_[_key_]+=_inc_value_

# output variables
label_list={}
label_times={}

from github import Github

#TODO change it to oauth
g = Github( "", "" )

org = g.get_organization(organization_name)
repo = org.get_repo(repository_name)
#Default sort is due date and direction desc
ms = repo.get_milestones('closed');
if ms is not None:
	# get last closed milestone
	m = ms[0];
	print "Processing Issues to milestone "+ m.title 
	#list issues
	for issue in repo.get_issues(m, 'closed'):
		should_process_time = False;
		label_key = None
		for l in  issue.labels:
			# count label ocurrences
			dict_key_inc(label_list, l.name)
			# check if should sumarize hours
			# there is a limitation of use:
			# for an given issue, only should exist one tag that accept hour count
			if l.name in tags_to_sumarize_hours:
				should_process_time = True
				label_key = l.name;
   		if should_process_time:
   			#print label_key + " " + str(issue.number)
   			should_process_time = False
			for c in issue.get_comments():
				import re
				#TODO find a better regex to get all cases
				pattern = re.compile('TG#(.*)H');
				# LIMITATION: the TG# must be in the first line of the comment
				# It's due to a problem of issues coments through email after register hours, it duplicates de registers
				times = pattern.findall(c.body.split('\n')[0])
				if len(times)>0:								
					for t in times:
						dict_key_inc(label_times, label_key, float(t))
						#print label_key+ " - " + issue.title +"("+str(issue.number)+  ") spent " + t +  " hours to be solved" 					
				else:
					# ugly way to process minutes
					pattern = re.compile('TG#(.*)M');
					times = pattern.findall(c.body.split('\n')[0])
					if len(times)>0:
						for t in times:
							dict_key_inc(label_times, label_key, float(t)/60)
							#print label_key+ " - " + issue.title +"("+str(issue.number)+  ") spent " + str(float(t)/60) +  " hours to be solved" 					

print "=========== Sprint Statistics ==========="				
print "\n........... Task Summary ...........\n"
for k in label_list.keys():
	number_of_issues = label_list.get(k)
	print "* " + k + " - " + str(number_of_issues);

print "\n........... Time Spent ...........\n"
for k in label_times.keys():
	total_time = label_times.get(k)
	print "* " + k + " - " + str(total_time) + " hours";

print "\n........... $$ Spent ...........\n"
for k in label_times.keys():
	total_time = label_times.get(k)
	print "* " + k + " - R$ " + str(int(total_time)*average_hour_price);

print "========================================="				