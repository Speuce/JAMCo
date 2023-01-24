# JAMCo
## The Job Application Management Console

# Project Summary and Vision
JAMCo's vision is to empower job seekers by providing a user-friendly platform for managing and tracking job applications, enabling them to stay organized and informed throughout the job search process. JAMCo is a web application to help people track job requirements, interview dates, and submitted cover letters, ultimately leading to successful career planning.

# Core Features

## Accounts

Users create personal accounts to access their job application console from any computer. Users can link their accounts with an external provider, and can personalize their experience and profile.

## Job Manager

Enables users to track information relevant to every job they apply for or wish to apply for. Users can record the job requirements, needed documents, dates and deadlines, and application status. 

## Friends

Users can connect with friends and other community members to share details about the requirements, challenges, and current status of their applications. 

## Notifications

Users can set reminders for their upcoming deadlines to stay coordinated, and set notifications for friend activity to keep in touch. 

## Request Handling

The application will be able to handle a capacity of 100 users, and up to 1000 concurrent requests per minute.

# Tech

We are using Vue.js with Vite and Vuetify on the frontend, and the Django framework for Python on the backend. For our database, supported by the Django ORM, we are using PostgreSQL.

<img width="540" alt="Architecture diagram" src="https://user-images.githubusercontent.com/29902980/214203271-78edec4f-c423-4947-aa91-5e50b6684e0f.png">

# User Stories by Feature

### Notifications:

- Friend Request Notifications ([#10](https://github.com/Speuce/JAMCo/issues/10))
- Deadline Notifications ([#11](https://github.com/Speuce/JAMCo/issues/11))
- Optionally Send Application Notifications To Friends ([#12](https://github.com/Speuce/JAMCo/issues/12))
- Optionally Recieve Application Notifications From Friends ([#13](https://github.com/Speuce/JAMCo/issues/13))

### Friends

- Add & Remove Friends ([#14](https://github.com/Speuce/JAMCo/issues/14))
- Friend Privacy Settings ([#15](https://github.com/Speuce/JAMCo/issues/15))
- Request Cover Letter Reviews ([#16](https://github.com/Speuce/JAMCo/issues/16))
- View Friends' Applications ([#17](https://github.com/Speuce/JAMCo/issues/17))

### Track A Job

- Add Job With Basic Info ([#6](https://github.com/Speuce/JAMCo/issues/6))
- Job Tracking Kanban Board ([#7](https://github.com/Speuce/JAMCo/issues/7))
- Add Cover Letter Field ([#8](https://github.com/Speuce/JAMCo/issues/8))
- Add Related Deadlines ([#9](https://github.com/Speuce/JAMCo/issues/9))
- Edit Job Details ([#22](https://github.com/Speuce/JAMCo/issues/22))

### Accounts

- Account Creation ([#18](https://github.com/Speuce/JAMCo/issues/18))
- Account Details & Personal Profile ([#19](https://github.com/Speuce/JAMCo/issues/19))
- Account Settings & Preferences ([#20](https://github.com/Speuce/JAMCo/issues/20))
- Account Login Options ([#21](https://github.com/Speuce/JAMCo/issues/21))
