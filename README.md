# Owensfeild voting system

Polling software for web and mobile, used for voting and suggesting ideas regarding Owensfield.

Software will be:

- Completely voluntary
- Anonymous
- Easy to use
- Impossible to cheat

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

## Technicalities

To keep votes anonymous, the software uses public-key cryptography (<a href="https://en.wikipedia.org/wiki/Schnorr_signature">schnorr</a> signature scheme). Each user has a private key and public key. The private key can be used to create poll and vote. The public key can be used to verify the created poll/vote has been submitted by a legitimate user. New users are created by 4/7 steering group submitting a request.
