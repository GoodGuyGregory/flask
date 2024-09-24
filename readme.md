# Flask Development

### Documentation 

[Flask Installation](https://flask.palletsprojects.com/en/3.0.x/installation/)  
[Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)  
[Flask Quickstart]()  



# Framework Terminalogy

## Blueprints

collections of code within modules that will del


## Views

these are sp

## Jinja Templating

Jinja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between {{ and }} is an expression that will be output to the final document. {% and %} denotes a control flow statement like if and for. Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.


## Running the Tutorial Application

```shell
# change directory into the flaskr project
flask --app flaskr run
```

## Installable Project

Making your project installable means that you can build a *wheel* file and install that in another environemnt