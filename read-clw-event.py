### Reads cloudwatch logs pushed by apache and prints in json
### depends on the subscription filter pattern
import json
import logging
import boto3
import gzip
import time
import urllib
import base64
from StringIO import StringIO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')


def lambda_handler(event, context):

    outEvent = str(event['awslogs']['data'])
    outEvent = gzip.GzipFile(fileobj=StringIO(outEvent.decode('base64','strict'))).read()
    print "Out Event -----------------"
    print outEvent

    cleanEvent = json.loads(outEvent)
    print "Printing cleanevent ------------------"
    print cleanEvent
    print "Printing extractedFields"
    print cleanEvent["logEvents"]["extractedFields"]

    #s=[]

    apache_bucket = "apache-access-logs-am"
    folderS3 = cleanEvent["logStream"]
    prefixS3 = 'apache_access'

    key = folderS3 + '/' + prefixS3 + str(int(time.time())) + ".log"

    tempFile = open('/tmp/file', 'w+')

    tempFile.write(str(cleanEvent))
    tempFile.close()


    tempFile = open('/tmp/file', 'r')

    a = tempFile.read()


    s3Results = s3.meta.client.upload_file(tempFile, apache_bucket, key)
    tempFile.close()
    print s3Results

    #for t in cleanEvent["logEvents"]:
    #    tmpFile.write()
        #p = { 'Data' : str(t['extractedFields']['request'])+','+str(t['extractedFields']['size'])+','+str(t['extractedFields']['ip'])+','+str(t['extractedFields']['client'])+','+str(t['extractedFields']['id'])+','+str(t['extractedFields']['user'])+','+str(t['extractedFields']['timestamp'])+','+str(t['extractedFields']['status'] }

    # s.insert(len(s),p)
    # bucket = 'events-am'
    # key = 'apache-events'
    #
    # return outEvent
