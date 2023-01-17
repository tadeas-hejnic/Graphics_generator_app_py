# App for generating info graphics for web and social networks
Author: Tadeáš Hejnic

## App description
This app will be used for generating invites, web banners and Instagram stories for sport club Handball Úvaly. Data about matches are downloaded from API server of Czech Handball Association.

### App purpose
While creating these images using photoshop pre-created layouts is easy to make a mistake and that's one of the main reasons why was this app created. The second reason is to save time and deliver images faster.

### Features
1. When I make match invites, I use different players to everyone appears similarly often on the invite. Beacause the app has its own database that stores this data, I don't have to care about it anymore.
2. Issues as to long name of the team, invalid data type of downloaded logo or bad resolution is managed via dialog window on the right side of the main window.
3. Be aware of missing these letters: č, ď, ě, ň, ř, š, ť, ž, ů, in font used in invite image. They are replaced with letters without hook and if any of these is used in created image, you will get a warning in dialog window.

## Run the app
### to install
For running the app is necessary to install Unidecode library. "pip install Unidecode"

### run
To run the app via CLI go to "app/" and type "python main.py". In few seconds will be opened the main window and further use is really intuitive. All issues should be displayed in dialog window on the right side of the window. Before launch will be checked if all important files exists to avoid problems during generating images.

### tests
To run tests via CLI go to "app/" and by simple command "pytest" run all tests.
