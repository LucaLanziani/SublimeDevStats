# DevStats

## Gather stats about your develop activity

Built during a hackathon, this plugin is more an experiment than anything else.

It listens for every keystroke and records them with the timestamp and the filename you are writing in.
The aim is to use those data to generate some informative graphs about your development activity and give you a useful feedback on how __improve your coding skills__.

Using this information you will also know how much time you spend coding, how fast you type, how many deletions you do, in which project you spend more time, ect etc. And you can also __challenge your friends__ with this data.

It can also be used to monitor how much time you spend coding and it can __give you tips about your health__ (ie. you spent 40mins coding, don't you think it is time for a walk?)


### Configuration

Right now the plugin as its configuration is pretty basic, it just offers you a couple of senders, you need to specify which one you want to use and the endpoint where to send the data.

#### Senders

   * http (send the data as a JSON via a POST to the endpoint)
   * file (append the data to the given file. __The plugin will not create the file for you__)

