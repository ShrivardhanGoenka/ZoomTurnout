# ZoomTurnout

ZoomTurnout is a tool which can be used to take attendance during Zoom meetings and generate reports after it ends.
The live version of the website is available [here](https://www.zoomturnout.com)

## Overview

This web application is made using the Django framework. It uses HTML, CSS, Bootstrap 5, JavaScript and JQuery for the frontend. SQLite is used for the database. All the data is kept encrypted using the Django encryption system.
A feature of zoom called webhooks is used to retrieve data from the meetings. The webhooks are available for free on the Zoom Marketplace platform. All users need to configure their Zoom accounts in order to set up the webhooks.
The webhooks send a notification to the application whenever a client starts a meeting, ends a meeting and whenever participants join and leave the meeting. An authentication token is also sent with this data in a JSON Post request format. This ensures security.

There are two main features of the application namely the 'Current Meeting' feature and 'Report Logs' feature. 

* Current Meetings: This gives users the option to check the participants who are currently present in the meeting. It also presents a list of participants who had joined the meeting but are currently not in the meeting.
Users can take attendance by using a file uploaded previously(discussed later).

* Report Logs: These reports are generated after a meeting has finished. It allows participants to view a complete report of all the participants. It displays all the participants who had joined the meeting along with:
  * Time when the participant first joined the meeting.
  * Time when the participant last left the meeting
  * Total Duration spent by the participant in the meeting.
  * The number of times the participant left the meeting.

  A flagged section is also available. Using the metrics uploaded by the user, the report will flag participants who were late to the meeting, left the meeting early, and spent very less time in the meeting.
  An attendance section is also available which is very similar to that of Current Meeting
  
There is also a profile section available where the user can update certain options which are unique to his/her accoount. They are:

* Files: The user can upload lists of students in the form of an excel sheet. The user can then select any of these files to take attendance in the above features.
* Metrics: The user can select certain values which determine whether a participant is late, left early, or did not spend enough time in the meeting. This is used for the flagged section of the report logs feature.
* Verification token: The user can change their Verification tokenor authentication token(mentioned above).

## Python Libraries

The following libraries were used to make this project:
* Python 3.7
* Django - 2.2
* django-bootstrap3
* django-bootstrap5
* openpyxl
* pandas

## Usage

To run this project locally, all of the above libraries need to be downloaded using the 'pip install' command in the terminal/ cmd.
Some fields are left empty due to security reasons, and thus, they need to be filled as without them, the application may not run. They are the Django Security Key and my Email SMTP details. Both of these details are available on the settings.py file in the Main folder.
To run this project the following command needs to be entered in cmd/ terminal. The path should be in the top level directory and all the packages must be installed and the virtual environment(if used) should be activated

```bash 
python manage.py runserver
```
More information about using custom ports and IPs can be found on the [Django documentation](https://docs.djangoproject.com/en/3.2/intro/tutorial01/#the-development-server)

## LICENCE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



Source: [MIT Licence](https://choosealicense.com/licenses/mit/)

Disclaimer: This website has been created and is maintained solely by Shrivardhan Goenka. The word 'zoom' in the name of the website is not related to the comapny Zoom([website](https://www.zoom.us)) in any way. 
