import React, {useState} from "react";
import Button from "@material-ui/core/Button";
import {logOut} from "./utils";
import {Redirect} from "react-router-dom";

export function Home() {
    const [loggedOut, setLoggedOut] = useState(0)
    return (loggedOut ? <Redirect to="/login"/> : <div>
        <h2>Home</h2>
        <Button onClick={() => {
            logOut()
            setLoggedOut(true)
        }} variant="contained" margin="normal" color="primary">
            Logout
        </Button>
    </div>)
}