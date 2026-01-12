Python script to organize folders
# To Run
The enviroment variable GROQ_API_KEY needs to be set to a valid groq api key, (either through bash or through .env) after which, you can run
``` bash
python pyOrganize.py path [instructions]
```
Where
* **path** is the location of the folder to sort relative to the current script
* **instructions** is any additional context or instructions for categories.
 
Possible features to implement
* Option for certain files to not be sorted
* Allow for creation of subfolders
* Better way to manage api key
* Option to use other models
* Backups to reverse effects in case sorting was undesirable or a preview of where files go
