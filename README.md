## Presentation
https://docs.google.com/presentation/d/1rcWersLc4nN7tr7lw4NHN6AKu2R4-OzdC094A8HIf4s/edit?usp=sharing

## About the Project
#Project Title: EmailButler

#Team Name: Capybara

#Team Members' Name & Email:

Leo Truong leo.truong@sjsu.edu

Hayden Tu hayden.tu@sjsu.edu

Alex Wong alex.wong02@sjsu.edu

#Problem/Issue: As we use our email more and more, associating ourselves with different individuals and businesses, there's likely instances where we'd wished we can set automated rules to regulate our busy inbox for convenience. Although gmail does have spam detection and blocking by users, there are other filters and requests that yield great benefit. For instance, it's preferable to have an option to automatically filter, archive, or delete email messages that are old and outdated. Speaking of old emails, sometimes we may purchase from online stores where we receive our receipts through our inbox, and it may be more convenient to find them, whether it'd to retrieve it to collect a warranty or return an item, through automating archiving receipts with personalized labeling.

#Functionality: With a variety of preset rules, the user can mix and combine different presets with specifications to accommodate an automative process for regulating both incoming messages and old messages in their inbox. Users may added exceptions to the rule taking effect under certain conditions while adhering to its functionality for the rest of the cases. For instance, user can choose a rule to delete emails after 90 days, and can added an exception for emails they've personally viewed (perhaps due to witheld importance) or kept labeled.

#Application should cover: Web scraping / GUI programming

#Assumptions: User use Gmail

#High-level description:

1) GUI will allow user to set rules, automations, exceptions, view changes the program makes, and takes in confirmation.
2) GUI will provide the details for the program to retrieve the information to access the user's inbox.
3) Code will web scrap using the user's provided information and presets to make changes directly on their account and logging changes made online back to the GUI for the user to view the history.
4) General outline of creating presets include: a premade list of rules, exceptions, and limited specifications for user to choose from and create. The application will save any presets the user decides to create for future usage.
5) Executing these presets, the code will filter, archive, delete, or label the necessary changes of each preset the user has saved.
6) When user enters the GUI, they can click a button 'optimize' to start the process of making changes to the user's inbox, following the given presets saved within the application. The program will return feedback via the GUI to the user when operations are complete.

### Built with
* CustomTkinter [https://customtkinter.tomschimansky.com/](https://customtkinter.tomschimansky.com/)
* Pillow [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/)
* Gmail API [https://developers.google.com/gmail/api/guides](https://developers.google.com/gmail/api/guides)

## Getting Started

### Prerequisites
1. Clone the repo
  ```sh
  git clone https://github.com/BigOlSheesh/EmailButler.git
  ```
2. Setting up OAuth 2.0 Client IDs
    - Create a Google Cloud Project at [https://console.cloud.google.com/](https://console.cloud.google.com/)
      
        ![Untitledvideo-MadewithClipchamp1-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/8b124a90-6bf9-4a7a-8f9b-f34464207972)
    
    - Create OAuth Page

        ![e-MadewithClipchamp-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/ef2d991b-c176-4b36-88d4-8fed530172cc)
   
    - Publish App
  
        ![2024-05-0400-43-12-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/24bf49ca-e374-4d4e-b167-b0c266395ee3)

    - Create OAuth Account
      
        ![f-MadewithClipchamp-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/66a9bb9d-ef6b-46ee-b0d0-ba41b83dd6f0)

    - Download Client File Json

        ![2024-05-0400-32-23-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/f8da0e6a-d21b-454a-a2ab-c2fca08913d5)

    - Enable Gmail API

        ![p-MadewithClipchamp-ezgif com-video-to-gif-converter](https://github.com/BigOlSheesh/ZenMail/assets/104650216/ae6c035a-3be4-40cc-bcb0-6225b80f9152)

2. Rename Client File Json to client_secret.json
3. Move client_secret.json to the directory where this project is located

### Installation
Install the necessary modules with pip:
  ```sh
  pip install customtkinter
  ```
  ```sh
  pip install pillow
  ```
  ```sh
  pip install --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2
  ```

## Snapshot

![image](https://github.com/BigOlSheesh/EmailButler/assets/104650216/197cd30a-924a-41e2-8fa1-e5f91d767694)

## Usage
This Python application assists users in the process of automated deletion of emails. The GUI is built with Tkinter, Custom Tkinter, and Pillow. It utilizes Gmail API to accomplish the deletion of emails.
