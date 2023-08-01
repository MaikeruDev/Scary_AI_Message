import win32evtlog
import requests
import openai
import pyttsx3
import os
import time

def get_recent_events(log_type, num_events=50):
    events = []
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    handle = win32evtlog.OpenEventLog(None, log_type)

    total_events = win32evtlog.GetNumberOfEventLogRecords(handle)
    num_events = min(num_events, total_events)

    while num_events > 0:
        events_batch = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events_batch:
            break

        for event in events_batch:
            event_record = {
                'RecordNumber': event.RecordNumber,
                'TimeGenerated': event.TimeGenerated.Format(),
                'SourceName': event.SourceName,
                'EventCategory': event.EventCategory,
                'EventType': event.EventType,
                'StringInsertions': event.StringInserts,
            }
            events.append(event_record)
            num_events -= 1

    win32evtlog.CloseEventLog(handle)
    return events

def get_completion(prompt, model="gpt-3.5-turbo-16k"):  
    messages = [{"role": "user", "content": "create a message that would be scary to hear at night played on your pc. do not add any headers like 'Subject:' or things in brackets. i want the raw text only"},
                {"role": "system", "content": "I see you, lurking in the darkness... You can't escape me. I know every move you make, every breath you take. Don't bother looking around; I'm already inside your home. You thought you were alone, but I'm here, always watching, always waiting. You can turn off the lights, but you can't hide from me. Fear is my ally, and I feed on your terror. Sleep with one eye open, for I will haunt your dreams and turn them into nightmares. There's no escape from the darkness that surrounds you. You're mine now, forever."},
                {"role": "user", "content": "based on this, tell me what the user did in 1 sentence:  {'RecordNumber': 72356, 'TimeGenerated': 'Tue Aug  1 09:54:01 2023', 'SourceName': 'MsiInstaller', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('\\\\schaan-srv21\\DIP\\Apl\\All_in_One_Installer_Custom\\TeamViewer\\TeamViewer.msi', '6216', '(NULL)', '(NULL)', '(NULL)', '(NULL)', '')}, {'RecordNumber': 72355, 'TimeGenerated': 'Tue Aug  1 09:54:01 2023', 'SourceName': 'MsiInstaller', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('TeamViewer', '15.36.9.0', '1033', '0', 'TeamViewer', '(NULL)', '')}, {'RecordNumber': 72354, 'TimeGenerated': 'Tue Aug  1 09:54:01 2023', 'SourceName': 'MsiInstaller', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('Product: TeamViewer -- Installation completed successfully.', '(NULL)', '(NULL)', '(NULL)', '(NULL)', '(NULL)', '')}, {'RecordNumber': 72353, 'TimeGenerated': 'Tue Aug  1 09:53:51 2023', 'SourceName': 'Microsoft-Windows-RestartManager', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('0', '2023-08-01T07:53:51.5425607Z')}, {'RecordNumber': 72352, 'TimeGenerated': 'Tue Aug  1 09:53:48 2023', 'SourceName': 'MsiInstaller', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('\\\\schaan-srv21\\DIP\\Apl\\All_in_One_Installer_Custom\\TeamViewer\\TeamViewer.msi', '6216', '(NULL)', '(NULL)', '(NULL)', '(NULL)', '')}, {'RecordNumber': 72351, 'TimeGenerated': 'Tue Aug  1 09:53:42 2023', 'SourceName': 'Windows Error Reporting', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('1385739111955007330', '5', 'StoreAgentScanForUpdatesFailure0', 'Not available', '0', 'Update;', '8024500c', '19045', '3208', 'Windows.Desktop', '', '', '', '', '', '\r\n\\\\?\\C:\\ProgramData\\Microsoft\\Windows\\WER\\Temp\\WER1704.tmp.WERInternalMetadata.xml', '\\\\?\\C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportArchive\\NonCritical_Update;_482058dea074c1b7a21fdac1aa1da1f6d23674b8_00000000_03f99d14-11fe-40e1-83e6-7b715ef4ff27', '', '0', '03f99d14-11fe-40e1-83e6-7b715ef4ff27', '268435456', '77745b6c92d0e262b33b22615f718762', '0')}, {'RecordNumber': 72350, 'TimeGenerated': 'Tue Aug  1 09:53:40 2023', 'SourceName': 'Windows Error Reporting', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('', '0', 'StoreAgentScanForUpdatesFailure0', 'Not available', '0', 'Update;', '8024500c', '19045', '3208', 'Windows.Desktop', '', '', '', '', '', '', '\\\\?\\C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue\\NonCritical_Update;_482058dea074c1b7a21fdac1aa1da1f6d23674b8_00000000_03f99d14-11fe-40e1-83e6-7b715ef4ff27', '', '0', '03f99d14-11fe-40e1-83e6-7b715ef4ff27', '4', '', '0')}, {'RecordNumber': 72349, 'TimeGenerated': 'Tue Aug  1 09:53:30 2023', 'SourceName': 'Software Protection Platform Service', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('2123-07-08T07:53:30Z', 'RulesEngine')}, {'RecordNumber': 72348, 'TimeGenerated': 'Tue Aug  1 09:53:14 2023', 'SourceName': 'Microsoft-Windows-RestartManager', 'EventCategory': 0, 'EventType': 4, 'StringInsertions': ('0', '2023-08-01T07:53:10.7945875Z')}"},
                {"role": "system", "content": "Based on the provided information, it appears that the user successfully completed the installation of TeamViewer version 15.36.9.0 on their system on August 1, 2023, at 09:54:01, as indicated by the relevant event logs."},
                {"role": "user", "content": "create another scary message but implement the following user actions to make it more scary. Write as 'I' (e.g: 'I saw that you installed program x'). Also add something similar like: 'Please listen very carefully as this is not a joke. I genuinely know what you have been up to and i can prove it.'. but not exactly this sentence, this is just an example. DO NOT USE THE EXACT SAME SENTENCE! Try to read the most popular moves from the activity like installing teamviewer or playing a game etc. not just accessing files. Also don't read out file paths  as it's too long. This is important, do not write or read file paths!!! NO FILE PATHS! Here is the user activity:" + prompt}] 
    response = openai.ChatCompletion.create( 
    model=model, 
    messages=messages, 
    temperature=0, 
    )

    return response.choices[0].message["content"]

def make_text_scary(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Setting properties for a creepy voice
    engine.setProperty('rate', 150)      # Adjust speech rate (default is 200)
    engine.setProperty('volume', 0.7)    # Adjust volume (default is 1.0)
    engine.setProperty('pitch', 50)      # Adjust pitch (default is 50)

    # Say the text
    engine.say(text)

    # Wait for the speech to complete
    engine.runAndWait()

if __name__ == "__main__":
    log_type = "Application"
    num_events_to_fetch = 50
    
    events = get_recent_events(log_type, num_events_to_fetch) 

    openai.api_key = 'YOUR_API_KEY'
     
    response = get_completion(str(events)) 

    f = open("C:\\Users\\" + str(os.getlogin()) + "\\Desktop\\youre_hacked.txt", "w")

    f.write("Hello " + str(os.getlogin()) + response)

    f.close()
    
    make_text_scary("Hello " + str(os.getlogin()) + response)  
