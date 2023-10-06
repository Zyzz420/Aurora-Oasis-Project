import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Profiles from './Profiles';
import Dashboard from './Dashboard';
import Songs from './songs';

function main() {
  return (
    <Router>
      <Switch>
        <Route path="/profiles" component={Profiles} />
        <Route path="/profile/:user_id" component={Profiles} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/add_song" component={Songs} />
        <Route path="/delete_song/:song_id" component={Songs} />
      </Switch>
    </Router>
  );
}

export default main;
