## Quantum Dice

You want to play a dice game with someone remote.  Who has the dice?  If they do, how can you trust them to honestly tell you the outcome?

We use quantum entanglement (or at least Wifi) to link the dice, so that either one can be rolled and the other shows the same value.

This project works on the Raspberry Pi with the Sense Hat, managed by [resin.io][resin-link].

To get this project up and running, you will need to signup for a resin.io account [here][signup-page] and set up a device, have a look at the [Getting Started tutorial][gettingStarted-link]. Once you are set up with resin.io, you will need to clone this repo locally:
```
$ git clone git@github.com:matt-williams/quantum-dice.git
```
Then add your resin.io application's remote:
```
$ git remote add resin username@git.resin.io:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push resin master
```

[resin-link]:https://resin.io/
[signup-page]:https://dashboard.resin.io/signup
[gettingStarted-link]:http://docs.resin.io/#/pages/installing/gettingStarted.md
