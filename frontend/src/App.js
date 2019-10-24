import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";

import {getSession, PrivateRoute} from "./utils"
import {Login} from "./login"
import {Home} from "./home";
import {Register} from "./register";
import {Client} from "./Client";

export default function App() {
    let client = new Client(process.env.REACT_APP_API_URL || "http://localhost:5000")
    return (
        <Router>
                <Switch>
                    <Route path="/register" component={(props) => <Register {...props} client={client}/>}/>
                    <Route path="/login" component={(props) => getSession() ? <Redirect to="/"/> : <Login {...props} client={client}/>}/>
                    <PrivateRoute path="/" component={(props) => <Home {...props} client={client}/>}/>
                </Switch>
        </Router>
    );
}

