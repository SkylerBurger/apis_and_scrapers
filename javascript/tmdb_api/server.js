const express = require('express');
const app = express();

const dotenv = require('dotenv');
dotenv.config();

const superagent = require('superagent');

// Using cookie-parser to add tokens as cookies to my responses
// Allows my next route to snag a piece of information (tokens)
const cookieParser = require('cookie-parser');
const { json } = require('express');
app.use(cookieParser());

const TMDB = 'https://api.themoviedb.org/4';
const TMDB_APPROVE = 'https://www.themoviedb.org/auth/access?request_token=';


app.get('/request', (request, response) => {

  superagent.post(`${TMDB}/auth/request_token`)
    .set('content-type', 'application/json')
    .set('authorization', 'Bearer ' + process.env.TOKEN)
    .send({redirect_to: 'http://localhost:3000/approve'})
    .then( data => {
      const requestToken = data.body.request_token;
      console.log('REQUEST TOKEN:', requestToken);
      // Adding cookie
      response.cookie('request_token', requestToken);
      response.redirect(TMDB_APPROVE + requestToken);
    })
    .catch( err => console.error(err));

});

app.get('/approve', (request, response) => {
  const requestToken = request.cookies.request_token;
  // Removing cookie from the outgoing response
  response.clearCookie('request_token');

  superagent.post(`${TMDB}/auth/access_token`)
    .set('content-type', 'application/json')
    .set('authorization', 'Bearer ' + process.env.TOKEN)
    .send({request_token: requestToken})
    .then( data => {
      const accessToken = data.body.access_token;
      const accountID = data.body.account_id;
      console.log('ACCESS TOKEN', accessToken);
      // Adding cookie
      response.cookie('access_token', accessToken);
      response.cookie('account_id', accountID);
      response.redirect('http://localhost:3000/lists');
    })
    .catch( error => console.error(error));
});

app.get('/lists', (request, response) => {
  const accessToken = request.cookies.access_token;
  const accountID = request.cookies.account_id;
  // Removing cookie from the outgoing response
  // response.clearCookie('access_token');
  // response.clearCookie('account_id');
  let lists;
  const ids = [];
  superagent.get(`${TMDB}/account/${accountID}/lists`)
    .set('authorization', 'Bearer ' + accessToken)
    .then( data => {
      lists = JSON.parse(data.text)["results"];
    })
    .then(() => {
      // This forEach doesn't seem to play well with multiple async requests
      // Need to find a way to chain requests to send collected data when finished
      lists.forEach( list => {
        superagent.get(`${TMDB}/list/${list.id}`)
          .set('content-type', 'application/json')
          .set('authorization', 'Bearer ' + accessToken)
          .then( data => {
            jsonData = JSON.parse(data.text);
            console.log(jsonData.object_ids);
            ids.push(jsonData.object_ids)
            // for (const [key, value] of Object.entries(jsonData.object_ids)) {
            //   ids.push({key, value});
            // }
          })
      })
      console.log(ids); 
      response.send(ids);
    })
    // .then( () => {
    // })
    .catch( err => console.error(err));
  

});


const PORT = process.env.PORT;

app.listen(PORT, () => {
  console.log(`We listening on ${PORT} everyone!`);
});