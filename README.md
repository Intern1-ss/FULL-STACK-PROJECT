# FULL-STACK-PROJECT

A comprehensive web-based application for managing academic operations in educational institutions. This system provides specialized portals for administrators, faculty members, and students with features tailored to their specific needs.
Table of Contents

Features
System Architecture
Database Structure
Installation
Configuration
Usage
API Documentation
Development Team

##Features
###Admin Portal

Dashboard with performance analytics
User management (students and faculty)
Course and subject management
Session management
Attendance monitoring
Leave application approval
Feedback management

##Faculty Portal

Personal dashboard with teaching load
Attendance management
Assessment management (CIE and ESE)
Leave application
Feedback submission

##Student Portal

Personal dashboard
Attendance viewer
Result viewer
Leave application
Feedback submission

##Integration Features

Google Sheets integration for data import/export
Bulk operations for courses, students, and marks
Support for Inter-Departmental (IDM) papers

##Database Structure
###Core Tables
Student Table
Stores comprehensive student information including:

Registration number
Personal details
Academic background
Current program and batch

##Faculty Table
Maintains faculty records with:

Faculty ID
Name and contact details
Department affiliation
Qualifications

##Department Table
Organizes departmental structure:

Department ID and name
Head of Department reference
Department description

##Paper (Subject) Table
Defines academic subjects with:

Paper code and title
Credit value
Assessment structure (CIE/ESE)
Department association
Inter-departmental status flag

##Junction Tables
The system uses several junction tables to handle many-to-many relationships:
Department Paper Access Table
Controls which departments can access which papers:

Access level control
Student quota management
Temporal access constraints

Faculty Paper Assignment Table
Manages teaching assignments:

Session-based assignments
Role definition
Workload tracking

Student Paper Enrollment Table
Tracks student enrollment in papers:

Enrollment type
Status tracking
Grade recording

Key Relationships

Papers can be owned by one department but accessed by multiple departments (IDM papers)
Faculty members can teach multiple papers across different sessions
Students can enroll in papers based on their department's access rights
