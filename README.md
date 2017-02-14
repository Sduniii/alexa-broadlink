# alexa-broadlink

Using python flask-ask with apache2 server, dynamic dns and for example lets encrypt. Or you can use it with ngrok.

With updated python-broadlink in broadlink folder. updated from https://github.com/mjg59/python-broadlink



https://developer.amazon.com/edw/home.html#/skills/list

# Example Use:
--------------
Invocation Name: the teawee

Intent Schema:
`{
  "intents": [
    {
      "intent": "ActionIntent",
      "slots": [
        {
          "name": "action",
          "type": "LIST_OF_ACTIONS"
        }]
    },
    {
      "intent": "DoubleActionIntent",
      "slots": [
        {
          "name": "action",
          "type": "LIST_OF_ACTIONS"
        },
        {
          "name": "number",
          "type": "AMAZON.NUMBER"
        }
      ]
    }
  ]
}
`

Custom Slots:
LIST_OF_ACTIONS with the commands

Sample Utterances:
`ActionIntent it should open {action}
ActionIntent open {action}
ActionIntent start {action}
ActionIntent {action}

DoubleActionIntent {number} {action}
DoubleActionIntent {action} {number}
DoubleActionIntent is should do {number} {action}
`
Say to the teawee ten louder -> increase the volume with 10
