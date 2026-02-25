# SL/VF Technical Take Home

> Build a state voter registration search tool

- [Evaluation](#evaluation)
- [What we are looking for](#what-we-are-looking-for)
- [Submitting your code](#submitting-your-code)
- [Questions](#questions)
- [Running the code](#running-the-code)

## Evaluation

1. Using the provided `voter_registration_deadlines.csv`, use the language and ORM framework of your choice to parse and store the info from `voter_registration_deadlines.csv` for each state into a SQL database (this is already done in the sample provided). _*Note: This is a sample of old data taken from various voter registration sites in 2018, and does not represent the current reality of these states. It should only be used for the purposes of this exercise.*_
2. Create a UI that displays the list of all the states and their voter information. The user should be able to filter and sort this table.
3. Create an API endpoint that will retrieve the data for this table from the backend DB.
4. Write tests to validate the API call(s).
5. Include a README (or edit this one if you choose to fork this repository) that describes the steps necessary for building and running the application as well as running the tests locally.

You may use any pattern or library that you find suitable to accomplish this assessment, however preference will be given to candidates that show they are able to use at least some of our technologies. Internally, we use Python and SQL Alchemy (SwingLeft) or NodeJS and Knex (VoteForward) backend and for the frontend we use React with Panda-UI and Chakra-UI for styling on the Next.Js framework.

Additionally, we have provided a sample hello-world framework which you may modify and use for this exercise. This sample already imports the voter data into a postgres DB, and sets up an API endpoint and frontend page for you to work from or use as an example.

You are welcome to use AI tools on your code test. If you do, please submit your _entire chat transcript_. The mechanism to do this will depend on which tool you use. If you use a command line tool such as Claude Code, you can store a transcript via the "script" command on Mac and Unix/Linux systems. You can also include a zip of ~/.claude/projects/code-test (or similar) if you prefer, but please ensure you do not send materials for any other projects.

Alternatively, you may submit an equivalent open-source code sample. If you do this, please only submit samples where you are the only contributor and sole author, or point us at specific commits where you were the sole author. As before, if you used AI to help generate the work, please give a detailed description of how it was used. If you choose to go with this route, please include as much detail as possible about which factors of your sample we should evaluate, and be prepared to discuss your code sample in the follow-up interview.

## What we are looking for

- Does it work? _*Note that you can "mock" an aspect of your solution rather than fully implement it, for example if a feature you want to demonstrate requires additional data. Just be clear in your submission notes what was mocked.*_
- Is the code clean and accessible to others?
- Does the code handle edge case conditions?

For the UX, we do not expect a fancy graphic design or style, but please make sure that the UI is clean and usable on both desktop and mobile web browsers.

## Submitting Your Code

The preferred way to submit your code is to create a fork of this repository, push your changes to the forked reposistory, and then grant access to your forked repository to your interviewer. Your interviewer is listed in the email you received inviting you to this technical interview.

Alternatively, you may submit the code in the form of a zip file and email it to your interviewer. If you do this, please be sure to include a README in your submission with full details on how to set up and run your code.

## Questions

If you have any questions, please reply to the invitation email you were sent for this technical interview.

## Running The Code

## Pre-reqs

You will need the following installed (I build this using Ubuntu 24.x, you may have slightly different ways to get some of these packages on other Operating Systems)

1. `postgresql`
    - Where the data goes, of course
    - `apt install postgresql`
2. `libpq-dev`
    - Needed to install the `psychopg2` driver for `Postgresql`, used by `SQLAlchemy`
    - `apt install libpq-dev`
3. `python3`, `python3-pip`, and `python3-venv`
    - You might already have this stuff, if so, great
    - `apt install python3 python3-pip python3-venv`
4. `node`, `npm`, and `pnpm`
    - For node and npm, you'll want to go to the Node website, the versions in `apt` are ancient (https://nodejs.org/en/download)
    - `pnpm` also comes from their site (https://pnpm.io/installation)
5. `postgresql` config
    - You'll need a Postgres User with permission to create/drop databases (and access anything they create)
    - By default, the `postgres` user can do this
    - You'll want to set up a password if you haven't already
        - `sudo -u postgres psql`
        - from the psql console: `ALTER USER postgres WITH PASSWPORD 'Password1!';`
        - You can set the password (or user if you create one) to whatever you want, the app can read from ENV vars

### Installation

1. pull down the repo.
2. `pnpm install --no-save`
3. `python3 -m venv .venv`
4. `source .venv/bin/activate`
5. `python3 -m pip install -r requirements.txt`
3. `python3 api/create_db.py`
    - If necessary, you can nuke the database entirely with `python3 api/drop_db.py`
4. `pnpm dev`
    - If you have different `postgresql` connection info than my defaults ([see: `api/engine.py`](../api/engine.py)), you can override them by using Environment Variables
    - e.g. `DB_USERNAME=hello DB_PASSWORD=world pnpm dev` instead to run the app
5. Browse to `http://localhost:3000`
    - Note that this site will also be served to the wider internet. There shouldn't be any problems there but its always worth remembering you do not want to use the Flask dev server for real production, and this app doesn't have any real security hardening applied


## Additional Notes from Jimmy

### Notes about the App

- Project setup took me some time, as I've never used NextJS before (and had to learn about Pages vs App routing to start) but once I got it working it was very slick. I haven't done SQLAlchemy in years but it seems like basically nothing has changed, so I got back into the interface without much trouble.
- There's a little more stuff in the DB and API sections that strictly needed; I tend to build `/:id` endpoints just out of habit if nothing else (if I haven't already set them up as a default in whatever blueprint or framework), so I tossed one up here before writing the frontend in case it was needed. It is not used by the frontend.
- Testing was focused more on the database level than the API level for this case, but I could also just swap all the tests to go through the Flask request harness instead of the SQLAlchemy stuff and basically test the same surface area plus a little more of the filtering logic. If I was going to work more on this, that would likely be my next task.
- I also didn't add any debouncing or duplicate request handling or race condition (on responses) handling to the actual `fetch` call from the frontend. This is also one of the next things I would do, and it's not like it's particularly complex with React to handle those functions. The frontend would be a lot more user friendly if it gave some indication like a spinning wheel when it's loading new data (both on initial load and on search/filter) and if it prevented you from sending a new search/sort while it was already waiting on an operation to return (or allowed it but handled in gracefully in whatever way is specified).
- The sorting and filtering should all work as expected. Note all filtering is case-sensitive; you could easily do case-insensitive by default if you wanted that instead. For this project, I opted for a very accepting API, so it will tend to just ignore requests with bad filter parameters (like filtering a date field on anything except a `yyyy-mm-dd` formatted value) rather than throw lots of errors. In real production settings, I tend toward strict schemas, and definitely stricter APIs than this one, but I still do believe you want to accept with as much variance as you possibly can, and send with as little variance (and as much adherence to specs) as you can.
- The sorting is a little fancier than a basic "equals" with sorts, but it's not over the top. I often tend toward data-heavy APIs with a similar set of filters like this available on as many fields as performance can support; the one notable missing filter is `LIKE` or `ILIKE`, which shouldn't be hard to add if needed.
- The UI is about as basic as it gets but it's using the Chakra built-in stuff so it looked usable on Mobile when I tested. I opted for a Table over using a Flexbox for everything mostly just in the interest of saving dev time, as I don't really build frontends from scratch very often and I didn't want to fiddle around with Flexbox settings for a while. For a real world application of course, I would probably lean towards Flexbox and would invest the time necessary for actual good mobile support.