### Configure your command

There are two ways to select the command to run

#### Set command in the configuration file

If you set the command in the configuration file, you don't have to specify any whitelist because the command can't be edited from the network.
The message you send to the topic to trigger the command won't be read and if you specify a command there won't be considered.

To run multiple commands, each one specified in the configuration file, you have to consider using a custom_topic.

##### Example

Here you have 2 commands:
- the first will be triggered with a message to "mycommand/topic/number1" and will run "echo Ready > file.txt"
- the second will be triggered with a message to "mycommand/topic2" and will run "mkdir Try"

*extract of configuration.yaml*
```
    commands:
      - Terminal:
          custom_topics:
            - mycommand/topic/number1
          contents:
            command: "echo Ready > file.txt"
      - Terminal:
          custom_topics:
            - mycommand/topic2
          contents:
            command: "mkdir Try"

```

If you don't set a command in the configuration file, the Monitor will look for the command in the message payload:

#### Run command specified via message

Maybe you prefer sending the command with the message. For security reason, you have to specify in the configuration file which command can be run.

To use this feature:
- add the whitelist key in the contents section of the Terminal Command in the yaml
- put the whitelist mode you want:
  - String: 'deny': don't run any command
  - String: 'allow': run every command you receive (you should only use this for debugging)
  - List of String: here you can put a list of rules (specified via filename wildcards) to allow only commands that verify at least one condition from this list

#### Examples

#### Whitelist 

Allow commands that start with "google-chrome" and with "vlc"

*extract of configuration.yaml*
```
    commands:
      - Terminal:
          custom_topics:
            - mywhitelistedcommands
          contents:
            whitelist: 
              - google-chrome*
              - vlc*

```

**First message**

This message asks to run `google-chrome www.youtube.com` and this command will be run


*message payload*
```
{
    "command": "google-chrome www.youtube.com"
}
```


**Second message**

This message asks to run `shutdown now` and this command won't be run


*message payload*
```
{
    "command": "shutdown now"
}
```


#### Allow 
Allow every command you receive

*extract of configuration.yaml*
```
    commands:
      - Terminal:
          custom_topics:
            - myallowedcommands
          contents:
            whitelist: allow

```

#### Deny 
Deny every command you receive

*extract of configuration.yaml*
```
    commands:
      - Terminal:
          custom_topics:
            - mydeniedcommands
          contents:
            whitelist: deny

```



