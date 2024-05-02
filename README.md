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
