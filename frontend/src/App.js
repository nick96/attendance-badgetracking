import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";

import {getSession, PrivateRoute} from "./utils"
import {Login} from "./login"
import {Home} from "./home";
import {Register} from "./register";
import Redirect from "react-router-dom/es/Redirect";

export default function App() {
    let apiUrl = "http://localhost:5000"
    return (
        <Router>
            <div style={{marginTop: "5%"}}>
                <Switch>
                    <Route path="/register" component={(props) => <Register {...props} apiUrl={apiUrl}/>}/>
                    <Route path="/login" component={(props) => getSession() ? <Redirect to="/"/> : <Login {...props} apiUrl={apiUrl}/>}/>
                    <PrivateRoute path="/" component={(props) => <Home {...props} apiUrl={apiUrl}/>}/>
                </Switch>
            </div>
        </Router>
    );
}

