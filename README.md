# Owensfield voting system

Polling software for web and mobile, used for voting and suggesting ideas regarding Owensfield.

Software will be:

- Completely free and open-source
- Voluntary
- Anonymous
- Easy to use
- Very hard to cheat

Software client is available <a href="https://owensfield.github.io/voting-system/#/">here</a> (currently still in development)

Data will be stored in publicly accessable database

## Challenges

To keep votes anonymous, the software only stores a <a href="https://en.wikipedia.org/wiki/Hash_function">hash</a> for verifying each user. The hash is created on the users device through a traditional `username`/`password` login system, `username`/`password` are not stored by the software.

Being `anonymous` means the data stored can be open, making it `hard to cheat` the system, but doing so creates some maintenance issues.

> Someone claims to have lost their login details, how would the admin know which was their old account to delete?

The easiest solution to this problem is deleting all user accounts every 12 months. If a user loses their details, they will not be able to vote until the time when all accounts are reset, and they can generate a fresh account. For most users the reset experience would just be having to login with their details again.

## Workflow

### Creation

Any user can suggest a poll. User fills out a form containing:

- Question `What material shall we use on the track?`
- Choices (up to 5) `Crushed stone £400, Pea gravel £800, etc, etc`
- How many votes are needed (default 40) `40`
- What the threshold is for consensus (default 70%) `65%`
- Closing date (default 14 days) `30 days`

### Approval

- 4/7 of the steering group need to approve a poll within 2 weeks
- Once approved the poll goes live

### Voting

- Users see a list of active polls in the app and can place their vote
- Users see a list of all completed polls and results

## User creation

New users are created by 4/7 steering group submitting a request.
