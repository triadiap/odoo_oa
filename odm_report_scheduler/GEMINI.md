# Project Overview

This project is an Odoo module named "Document Monitoring". Its main purpose is to automate the process of document and report housekeeping. It allows users to configure various types of documents, set up reporting periods (daily, weekly, monthly, etc.), and assign ownership to different users. The module automatically sends email notifications to the responsible users when a report is due. It also keeps a log of all sent emails and their status.

## Main Technologies

*   **Odoo Framework:** The module is built using the Odoo framework (version 14.0).
*   **Python:** The backend logic is written in Python.
*   **XML:** The views and data are defined using XML.
*   **PostgreSQL:** Odoo uses PostgreSQL as its database.

## Architecture

The module follows the standard Odoo architecture, with the following key components:

*   **Models:** The data models are defined in the `models` directory. The main models are:
    *   `odm.document.configuration`: Configures the document reports, including scheduling, ownership, and email notifications.
    *   `oa.reporting.type`: Defines the types of reports.
    *   `docmon.mail.server`: Configures the SMTP server for sending emails.
    *   `odm.report.submission`: Represents a single report submission.
    *   `odm.document.mail.log`: Logs the status of sent emails.
*   **Views:** The user interface is defined in the `views` directory using XML files.
*   **Controllers:** The web controllers are defined in the `controllers` directory. The main controller is `PrintController`, which is responsible for printing PDF reports.
*   **Security:** The access rights and groups are defined in the `security` directory.

# Building and Running

This is an Odoo module, so it needs to be installed in an Odoo instance to run.

## Installation

1.  Copy the `odm_report_scheduler` directory to the `addons` directory of your Odoo instance.
2.  Restart the Odoo server.
3.  Go to the "Apps" menu in Odoo, search for "Document Monitoring", and click "Install".

## Running

Once the module is installed, you can access its features through the "Document Monitoring" menu in Odoo.

# Development Conventions

*   The code follows the standard Odoo development guidelines.
*   The module uses the `mail` and `web` modules for email and web functionality.
*   The module has a clear separation of concerns between models, views, and controllers.
