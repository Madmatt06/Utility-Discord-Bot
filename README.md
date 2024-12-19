# Utility-Discord-Bot
A simple bot with weird commands <br />
<sub><sub><sub>???????</sub></sub></sub> <br />
All commands which are centralized around a specific feature are separated in to their own folder.
For example, the nick locking features has its own folder in the cog folder where the files for all the commands related to it,
the guild class file, and the nick user class file is stored. 
The formatting is still a mess right now but hopefully I will get that fixed soon.

## Currently implemented features

### Cat command
Gets a random cat picture from a free api I found

### Bad Joke Command
Gets a random joke from a free api I found

### Cattp
Picks a random HTTP code from a list and returns an image associated with the code cat themed from a free "api"
(Not sure if it should be considered an api)

### Ping
**Pong**

### Say
Allows the user to control what the bot says.
This one needs its permissions looked over.
It seems super wrong to give the server admins permissions to it but not the bot owner. (See Issue #4)

### Sync Tree
Updates the list of bot commands.
It should only be used when updating the bot with a new command.
I'm planning to move this command to the console if I can figure that out.