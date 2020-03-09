How to interact with the API
=================

The API implemented within this project is a Rest-API for which the [Django Rest Framework](https://www.django-rest-framework.org/) was used. This is how it generally works:

The client sends a question to the server. The server returns an answer with an id. The client sends a new question but also includes the id of the last answer. This could look like this:

### 1) Simple Conversation
The client sends a messeages to the chatbot via POST to ```/api/v1/chatbot/``` with the following fields:

* message: your user input, eg. 'my question'
* in_response_to: the id of the chatbot's previous reponse (here null, as this is the first message) 

```
{
    message: "my question", 
    in_response_to: null
}
```

which will result in the following reponse:

* id: the id of the chatbot's reponse message
* message: the message you sent in your POST request
* reply: the chatbot's reply
* conclusion: if there is an conclusion, it means that the chatbot conversation has finished and within the next POST the ```in_response_to``` should be set to ```null``` in order to start an new conservation (see example below).
* forward: if forward is set, this means that the chatbot has been configured in a way, to jump to a different conversation. So instead if setting the ```in_response_to``` to the ```id``` , you should set it to the ```id``` from within the ```forward``` reply (see example below)

```
{
    "id":89,
    "message":"my question",
    "reply":"This is conversation alpha!",
    "conclusion":"",
    "forward":{}
}
```

your next POST to the API would look like this:

```
{
    message: "my next question", 
    in_response_to: 89
}
```



### 2) Conversation with Conclusion
if the API replies with an reponse where the ```conclusion``` is set you have start a new conservation. 

e.g. the API's response looks like that:
```
{
    "id":90,
    "message":"my question",
    "reply":"This is one in conversation alpha!",
    "conclusion":"This is all I can tell you. Do you have more questions? If yes, how can I help you?",
    "forward":{}
}
```

your next POST should have ```in_response_to``` set to ```null``` the look like that:
```
{
    message: "my next question", 
    in_response_to: null
}
```

### 2) Conversation, that needs to be forwared
if the API replies with an reponse where the ```forward``` is set you have to change the id of your ```in_response_to```.

e.g. the API's response looks like that:
```
{
    "id":96,
    "message":"yes",
    "reply":"",
    "conclusion":"",
    "forward":
        {
            "id":89,
            "reply":"This is conversation alpha!",
            "conclusion":""
        }
}
```

instead of setting ```in_response_to``` to ```96``` you should set to the ```id``` in ```forward```, like that:

```
{
    message: "my next question", 
    in_response_to: 89
}
```


