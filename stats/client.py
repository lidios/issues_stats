#!/usr/bin/python
# -*- coding: utf-8 -*
# @Lidio
# Program used to get github issues statistics


# Interessing TAGs
#TODO to parametrize
tags_to_sumarize_hours = ['Impediment', 'inc: Reativo' , 'inc: Proativo', 'Meeting', 'Deploy']
tags_to_print = ['Impediment', 'inc: Reativo' , 'inc: Proativo', 'Meeting', 'Deploy', 'Task']
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
inc_reativos={}
inc_proativos={}

from github import Github

import os
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Script used to generate a WebOps Sprint Report''', epilog="""All that's well, ends well.""")
parser.add_argument('--user', help='User to login on GitHub', required=True)
parser.add_argument('--passwd', help='Password to login on GitHub', required=True)
#parser.add_argument('--milestone', type=int, help='Milestone to be Analized, sepparated by comma', required=True)
parser.add_argument('--milestones', help='Milestone to be Analized', required=True)
args=parser.parse_args()

user = args.user
passwd = args.passwd
#milestone = args.milestone
milestones = args.milestones.split(',')
useragent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"
reativo = "inc: Reativo"
proativo = "inc: Proativo"


#TODO change it to oauth
g = Github( login_or_token=user, password=passwd, user_agent=useragent )

org = g.get_organization(organization_name)
repo = org.get_repo(repository_name)
#Default sort is due date and direction desc
#ms = repo.get_milestones('closed');

issues_time_dict = {}

for milestone in milestones:
	milestone = int(milestone)
	ms = repo.get_milestone(milestone)
	if ms is not None:
		# get last closed milestone
		#m = ms[0];
		m = ms
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
				if l.name == reativo:
				  inc_labels_name = ""
				  for l1 in  issue.labels:
				    if l1.name != reativo and l1.name != proativo:
				  	  dict_key_inc(inc_reativos, l1.name)

				if l.name == proativo:
				  inc_labels_name = ""
				  for l1 in  issue.labels:
				    if l1.name != reativo and l1.name != proativo:
				  	  dict_key_inc(inc_proativos, l1.name)

	   		if should_process_time:
	   			total_issue_time = 0
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
							total_issue_time += float(t)
					else:
						# ugly way to process minutes
						pattern = re.compile('TG#(.*)M');
						times = pattern.findall(c.body.split('\n')[0])
						if len(times)>0:
							for t in times:
								dict_key_inc(label_times, label_key, float(t)/60)
								total_issue_time += float(t)/60
								#print label_key+ " - " + issue.title +"("+str(issue.number)+  ") spent " + str(float(t)/60) +  " hours to be solved"

				dict_key_inc(issues_time_dict, issue.title, total_issue_time)

print "=========== Milestone(s) Statistics ==========="				
print "\n........... Task Summary ...........\n"
for k in label_list.keys():
	if k in tags_to_print:
	  number_of_issues = label_list.get(k)
	  print "* " + k + " - " + str(number_of_issues);

print "\n........... Incidentes Reativos e Proativos ..........."
print "* Reativos"
for k in inc_reativos.keys():
	r = inc_reativos.get(k)
	print "  * " + k + " - " + str(r);
print "* Proativos"
for k in inc_proativos.keys():
	p = inc_proativos.get(k)
	print "  * " + k + " - " + str(p);

print "\n........... Time Spent ...........\n"
for k in label_times.keys():
	total_time = label_times.get(k)
	print "* " + k + " - " + str(total_time) + " hours";

print "\n........... $$ Spent ...........\n"
for k in label_times.keys():
	total_time = label_times.get(k)
	print "* " + k + " - R$ " + str(int(total_time)*average_hour_price);

print "\n........... Top time consuming issues ...........\n"
import operator
sorted_by_time_issues = sorted(issues_time_dict.iteritems(), key=operator.itemgetter(1), reverse = True)
for k in sorted_by_time_issues:
	print "%s H - %s " % (k[1], k[0])

print "========================================="				
