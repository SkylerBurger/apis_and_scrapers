Lately at work our go to architecture for creating websites is to use a React frontend with a Django REST Framework (DRF) backend. The two are connected by API calls using axios in the frontend. Some Redux is used as well for storing global app state. This is our preferred method as it allows the frontend and backend to be completely decoupled. And as long as we define a list of endpoints and returned data to work with, the frontend and backend can be developed in parallel. This also allows us the option to easily create mobile apps for any of the projects in the future as they can just consume the backend API. On a side note, we’re currently looking at using React Native for future mobile app projects.

In the rest of this post, I’ll go through how to setup a React frontend and DRF backend project. Note I assume you’re already familiar with React, Redux, Django, DRF, npm etc. This isn’t a tutorial for them.

There isn’t much to do for the default backend outside of simply installing Django and DRF, and setting up the database. From the root of your project folder, create a virtualenv and install Django and DRF.

Now start a new Django project and Django app.

You should now setup your database and edit your project’s settings to use the database. Good documentation on how to do this for your particular DB can be found on Django’s website. Then you should configure DRF following the instructions on their website found here.

The next step you will most likely want to do is setup authentication in your API. If you wont require authentication (e.g. no user logins), you can skip this. My company’s React/Django template project currently uses plain token authentication as it’s the simplest to setup. I recommend this for those learning as well, but it’s not the best for production. These tokens never expire which poses quite a security risk if it’s ever leaked. Soon we’ll update the template project to use something like oauth, or expiring JWT tokens — as of yet it’s undecided. Documentation for configuring token authentication is here.

Once token authentication is configured, you will want to create a urls.py in your app (if you haven’t already), and use DRF’s token auth view. This endpoint at /auth lets users POST their username and password and get their auth token as a response. In the frontend, this token will get stored in the Redux store for further API calls.

And just to make sure it’s clear, your backend/urls.py file should now look like this

By doing this, we’re just making each app look after its own urls. Maybe in the future you will add more apps to the backend and it would get messy to add everything to backend/urls.py

You should now have a functioning backend DRF API with a single endpoint /auth that lets users get their auth token. Let’s setup a user and run the backend server for testing later.

Remember to run migrate for the first time to create your database. Then we’ll create a user for whom we can get an auth token for. With the server now running, you can test your /auth endpoint works quickly using curl

For the frontend, we used Facebook’s create-react-app as the starting point. So the first thing to do is install it and create a new project using it in the root of your project folder. We also eject the configuration as we need more control, and everyone on our team is fine with using webpack etc.

Next we want to install some additional dependencies.

Now instead of listing all the code used by our React template project, I’m just going to show the important parts that connect our frontend to our backend. Firstly create a redux store as we will want to save the user’s auth token for making more API calls in the future

And then setup the token reducer

And finally the actions (notice this is two files in one code block)

We now have an action we can dispatch to store the user’s token after logging in. So next lets look at how we login

This piece of code uses axios to post to our /auth backend and then dispatch the returned token to our redux store. Once this is done, we can now create an axios based API client using our stored token to make further API calls from elsewhere in our React components.

We reference the file ../config/Api in the last two code-blocks. Here’s what that file looks like — it’s simply a file to map constants to endpoints, making the code more readable and easier to modify later.

That’s all there is to it to connect our frontend to our backend. You can now try using the Auth.js login function to get the auth token for the user we created earlier. If you do, you can look at your browser’s dev tools to check the output from redux-logger to see the result of the setToken redux action.

