#!/usr/bin/env python

import email
import smtplib
import subprocess
import sys

notify_name = 'Spam Submit'
notify_email = 'your@email.here'

msg = email.message_from_file(sys.stdin)
msg_from = msg['From']

if not msg.is_multipart():
	print 'exit out here'
	sys.exit(1)

parts = msg.get_payload()

results = []

for p in parts:
	record = {}

	if not p.get_content_type() == 'message/rfc822':
		continue

	subparts = p.get_payload()
	if not len(subparts) == 1:
		record['error'] = 'more subparts than expected'
		results.append(record)
		continue

	submsg = subparts[0]
	record['Subject'] = submsg['Subject']

	proc = subprocess.Popen(['/usr/bin/sa-learn', '--spam', '--no-sync'],
		stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd='/tmp/')

	result_stdout, result_stderr = proc.communicate(input=submsg.as_string())

	record['Result'] = result_stdout.strip()

	results.append(record)

# sync the database and journal after processing all in the collection
proc = subprocess.Popen(['/usr/bin/sa-learn', '--sync'],
	stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd='/tmp/')

headers = """From: %s <%s>
To: %s
Subject: Results from submission

Results are below!
""" % (notify_name, notify_email, msg_from)
output = ''
for i in results:
	keys = i.keys()
	keys.sort()

	for k in keys:
		output += '%10s: %s\n' % (k, i[k])

	output += "\n\n"

smtp = smtplib.SMTP('localhost')
smtp.sendmail(notify_email, msg_from, '%s%s' % (headers,output))

