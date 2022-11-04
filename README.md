Codeplate is a simple template generator that allows you to write the template in the language of the file that you want instead of template language like handlebars. Pretty simple and close to many template generators but the key is being able to write the templates in the same language allowing to make use of eslint rules and intellisense and also as you might see in a demonstration the format for running the templates and creating them is much cleaner and more manageable imo.



It also allows you to group templates together into json objects called 'Platters" very easily with some config settings to quickly generate a common pattern of files like a README, test, and js file. This sounds similar to the approach we use in plop with the biggest difference being how easy it is to make these "Platters". One rather small (literally a few lines) json object verses keeping up with plop generator code and having to add new prompts and track where the stored data is going within that.



And the 3rd feature that i think is honestly the biggest and will help mostly those that plan our their epics and tickets is somethings called "Plans". Which is basically another json object that uses the key/value system to create massive amounts of code. It takes the structure of the json object and translates it to a directory/file relationship where every nested objects is a new directory and anything that isn't a nested object is the contents of the folder. The awesome thing is these values could be Templates OR Platters allowing a few lines in an object to create dozens of file (or as many as you want). The reason i think this is awesome is because if you take something like a new feature, this allows you to plan it out visually and at the same it allows you to just run the Plan when you're done and all the work you put in automatically generates the whole structure of the new feature.

