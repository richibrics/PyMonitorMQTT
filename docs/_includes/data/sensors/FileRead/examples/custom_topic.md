### Content of a file with specified topic

This configuration sends to the specified custom topic the content of the plex.txt file in the ‘C:/Users/PC’ folder

```
- FileRead:
    custom_topics:
      - myfile/content
    contents:
      filename: "C:\Users\PC\plex.txt"
```