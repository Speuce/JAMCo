# JAMCo
**The Job Application Management Console**

# Vision Statement
JAMCo's vision is to empower job seekers by providing a user-friendly platform for managing and tracking job applications, enabling them to stay organized and informed throughout the job search process. JAMCo is a web application to help people track job requirements, interview dates, and submitted cover letters, ultimately leading to successful career planning.

# Summary

JAMCo is designed to track your progress across all your open job applications. Its kanban board is designed to make job tracking a breeze. You can customize your board to include categories relevant to your field, such as jobs you wish to apply to in the future, pending pre-assessments, or scheduled interviews. Adding jobs to the job board is easy with our user-friendly forms. Signing up on JAMCo is near-instant with a Google login, and you can customize your profile and tracking options for any industry. You can also use the Friends page to add people you know on JAMCo, view their open applications, share relevant positions, and request cover letter reviews. You can even configure notifications to send you an email when a friend shares a job or requests a cover letter review.

# Target Market: Students

Searching for a job can be a busy and time-consuming process, particularly for students who are looking for internships or preparing for life after graduation. With all the responsibilities already on their plate, job-hunting can add to the burden. JAMCo simplifies this by putting all of the user’s job applications into one place. By putting all of the user’s job application information at their fingertips, JAMCo lets them worry less about juggling job listings and focus more on making great first impressions on future employers.


# Core Features

## Accounts

Users create personal accounts to access their job application console from any computer. Users can link their accounts with an external provider, and can personalize their experience and profile.

## Job Manager

Enables users to track information relevant to every job they apply for, or wish to apply for. Users can record the job requirements, necessary documents, dates and deadlines, and application status. 

## Friends

Users can connect with friends and other community members to share details about the requirements, challenges, and current status of their applications. 

## Notifications (Optional)

Users can set reminders for their upcoming deadlines to stay coordinated, and set notifications for friend activity to keep in touch. 

## Request Handling

The application will be able to handle a capacity of 100 users, and up to 1000 concurrent requests per minute.

# Tech

We are using Vue.js with Vite and Vuetify on the frontend, and the Django framework for Python on the backend. For our database, supported by the Django ORM, we are using PostgreSQL.

<img width="540" alt="Architecture diagram" src="https://user-images.githubusercontent.com/29902980/214203271-78edec4f-c423-4947-aa91-5e50b6684e0f.png">

# User Stories by Feature

### Accounts ([#2](https://github.com/Speuce/JAMCo/issues/2))

- Account Creation ([#18](https://github.com/Speuce/JAMCo/issues/18))
- Account Details & Personal Profile ([#19](https://github.com/Speuce/JAMCo/issues/19))
- Account Settings & Preferences ([#20](https://github.com/Speuce/JAMCo/issues/20))
- Account Login Options ([#21](https://github.com/Speuce/JAMCo/issues/21))

### Track A Job ([#3](https://github.com/Speuce/JAMCo/issues/3))

- Add Job With Basic Info ([#6](https://github.com/Speuce/JAMCo/issues/6))
- Job Tracking Kanban Board ([#7](https://github.com/Speuce/JAMCo/issues/7))
- Add Cover Letter Field ([#8](https://github.com/Speuce/JAMCo/issues/8))
- Add Related Deadlines ([#9](https://github.com/Speuce/JAMCo/issues/9))
- Edit Job Details ([#22](https://github.com/Speuce/JAMCo/issues/22))

### Friends ([#4](https://github.com/Speuce/JAMCo/issues/4))

- Add & Remove Friends ([#14](https://github.com/Speuce/JAMCo/issues/14))
- Friend Privacy Settings ([#15](https://github.com/Speuce/JAMCo/issues/15))
- Request Cover Letter Reviews ([#16](https://github.com/Speuce/JAMCo/issues/16))
- View Friends' Applications ([#17](https://github.com/Speuce/JAMCo/issues/17))

### Notifications ([#5](https://github.com/Speuce/JAMCo/issues/5)) (Optional)

- Friend Request Notifications ([#10](https://github.com/Speuce/JAMCo/issues/10))
- Deadline Notifications ([#11](https://github.com/Speuce/JAMCo/issues/11))
- Optionally Send Application Notifications To Friends ([#12](https://github.com/Speuce/JAMCo/issues/12))
- Optionally Recieve Application Notifications From Friends ([#13](https://github.com/Speuce/JAMCo/issues/13))

# Coding Style

## Frontend

We use the [Airbnb JavaScript Style Guide](https://airbnb.io/javascript/). Some rules from this style guide include:

- Use camelCase when naming objects, functions, and instances ([camelcase](https://eslint.org/docs/latest/rules/camelcase)); use PascalCase for constructors and classes ([new-cap](https://eslint.org/docs/latest/rules/new-cap))
- Use `const` for all variable declarations by default; use `let` instead of `var` if you must reassign references ([prefer-const](https://eslint.org/docs/latest/rules/prefer-const), [no-const-assign](https://eslint.org/docs/latest/rules/no-const-assign), [no-var](https://eslint.org/docs/latest/rules/no-var))
- Limit line length to 100 characters ([max-len](https://eslint.org/docs/latest/rules/max-len))
- Use literal syntax for object and array creation, i.e. `{}` and `[]` instead of `new Object()` and `new Array()` ([no-new-object](https://eslint.org/docs/latest/rules/no-new-object) and [no-array-constructor](https://eslint.org/docs/latest/rules/no-array-constructor))
- Require parentheses when mixing different arithmetic operators ([no-mixed-operators](https://eslint.org/docs/latest/rules/no-mixed-operators))

A list of all the rules can be found on the Airbnb style guide website (linked above) or on [the style guide's GitHub repository](https://github.com/airbnb/javascript). We use ESLint to generate error messages when code does not follow these guidelines. 

We also use [Prettier](https://www.npmjs.com/package/prettier) to enforce the following settings:

- Tab width of 2
- Trailing commas used whenever listing items across multiple lines, including function arguments
- No semicolons
- Single quotes for all strings, except those which contain apostrophes

Both ESLinst and Prettier are integrated into our continuous delivery system, which runs checks whenever code is pushed to make sure that it follows our style guidelines. The GitHub Action that does so can be found [here](https://github.com/Speuce/JAMCo/blob/master/.github/workflows/node.js.yml#L54).

## Backend

We use [Flake8](https://pypi.org/project/flake8/) and [Black](https://pypi.org/project/black/) to format our backend code.

Some of Black's formatting rules include:

- Use double quotes for strings unless doing so results in more backslash escapes than using single quotes
- Limit line length to 120 characters (configured via `python.formatting.blackArgs` in VSCode's `settings.json` file)
- Have no more than one empty line between lines of code inside functions, and no more than two empty lines between lines of code at the module level

A complete description of Black's code style can be found [here](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

Some of Flake8's formatting rules include:

- Use only spaces for indentation ([W191](https://www.flake8rules.com/rules/W191.html))
- Avoid deprecated syntax ([W601](https://www.flake8rules.com/rules/W601.html), [W602](https://www.flake8rules.com/rules/W602.html), [W603](https://www.flake8rules.com/rules/W603.html), [W604](https://www.flake8rules.com/rules/W604.html))
- Start comments with a single '#' followed by a space ([E262](https://www.flake8rules.com/rules/E262.html), [E265](https://www.flake8rules.com/rules/E265.html), [E266](https://www.flake8rules.com/rules/E266.html))
- Each line should contain at most one statement ([E701](https://www.flake8rules.com/rules/E701.html), [E702](https://www.flake8rules.com/rules/E702.html))

A complete list of Flake8's rules can be found [here](https://www.flake8rules.com/).

Similar to the frontend, we use Flake8 and Black with GitHub Actions to check that all pushed code does not trigger any of Pylint's warnings. The GitHub action that does so can be found [here](https://github.com/Speuce/JAMCo/blob/master/.github/workflows/backend_lint.yml).

While not automatically enforced, we also use the following additional formatting guidelines:

- Use snake_case for objects, functions, and instances
- Use PascalCase for classes
- Indent using 4 spaces
- Put two blank lines between module-level items (i.e. classes and functions) and one blank line between methods

