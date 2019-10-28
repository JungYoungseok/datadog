from datadog import initialize, api
import time
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

options = {
    'api_key': '$API_KEY',
    'app_key': '$APP_KEY'
}

SYSTEM_LOAD='{"viz": "timeseries", "requests": [{"q": "avg:system.load.1{*}", "conditional_formats": [], "type": "line"}, {"q": "avg:system.load.5{*}", "type": "line"}, {"q": "avg:system.load.15{*}", "type": "line"}], "events": [{"q": "hosts:* ", "tags_execution": "and"}]}'

CPU_USER_USAGE='{"viz": "timeseries", "requests": [{ "q": "avg:system.cpu.user{*} by {host}", "type": "line", "style": {"palette": "cool","type": "solid","width": "thin"},"aggregator": "avg","conditional_formats": []}], "autoscale": true}'

MEMORY_FREE='{"viz": "timeseries", "requests": [{"q": "avg:system.mem.free{*} by {host}", "conditional_formats": [], "type": "line"}], "events": [{"q": "hosts:* ", "tags_execution": "and"}]}'

initialize(**options)

def getGraphURL(graph_definition, start_time, end_time):
    result = api.Graph.create(graph_def=graph_definition, start=start_time, end=end_time)
    return result["snapshot_url"]

def buildReport(start, end):
    system_log_graph=getGraphURL(SYSTEM_LOAD, start, end)
    cpu_usage_graph=getGraphURL(CPU_USER_USAGE, start, end)
    memory_free_graph=getGraphURL(MEMORY_FREE, start, end)
 
    textbody = """\
    <html>
      <body>
        <h2># Here's the 24hours report</h2>
        <p>
        <b>1. SYSTEM_LOAD</b><br>
        <img src="%s"><br>
        <b>2. CPU_USER_USAGE</b><br>
        <img src="%s"><br>
        <b>3. MEMORY_FREE</b><br>
        <img src="%s"><br>
        </p>

        More information can be found from <a href="https://app.datadoghq.com/dashboard/tpx-zcd-ept/hostmonitoringtemplate?from_ts=1572239532051&to_ts=1572243132051&live=true&tile_size=m">here</a>
      </body>
    </html>
    """

    email_report=textbody % (system_log_graph, cpu_usage_graph, memory_free_graph)
    print (email_report)
    return email_report

def sendEmail(subject, content, receiver_email):
    # This code requires https://devanswers.co/allow-less-secure-apps-access-gmail-account/
    sender_email = "yourSMTPEnabled@gmail.com"
    password = "********"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message.attach(MIMEText(content, "html"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

end = int(time.time())
start = end - (60 * 60 * 24)
subject = "This is an example of daily report"
receiver_email = ['email1@testblah.com','email2@testblah.com']

report_content = buildReport(start, end)
sendEmail(subject, report_content, receiver_email)
