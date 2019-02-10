# self-driving-car

Training model is based on an Actor-Critic model which was first introduced by DeepMind for its GO game. It not only takes much lesser training time but also produce highly efficient model which can interact with environment and predict best possible action. It is also well defined in Aurélien Géron's "Hands on scikit learn and tensorflow" book

The images feed to network has below details.

![alt text](https://github.com/gadginir/self-driving-car/blob/master/diagrams/dia1.png)

The car track look like 

![alt text](https://github.com/gadginir/self-driving-car/blob/master/diagrams/track.png)


Whenever Red block(car) go out of the white boundry(track), it will get -100 points, game ends and begin from start position. 
Whole track is divided into 12 parts (Each Quarter is divided into 3 parts) and once Car crosses every part of track, it gets double point from last part (20 Points when cross first part) and accordingly keep collecting points. Motive is to encourage Car to move forward in right direction to collect more points than earlier step and keep progressing to finish line where he get additional 500 points.
