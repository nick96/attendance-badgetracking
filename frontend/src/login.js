import {ErrorMessage, Field, Form, Formik} from "formik";
import React, {useState} from "react";
import {Link, Redirect} from "react-router-dom";
import {TextField} from 'formik-material-ui'

import {setSession} from "./utils";
import Button from "@material-ui/core/Button";
import type {Credentials} from "./Client";
import * as Yup from "yup"

const LoginFormSchema = Yup.object().shape({
    email: Yup.string().email("Email is not valid").required("Email is required"),
    password: Yup.string().required("Password is required")
})

function LoginForm({onSubmit}) {
    return (<Formik
        initialValues={{email: '', password: ''}}
        validationSchema={LoginFormSchema}
        onSubmit={onSubmit}
        render={props => (
            <div>
                <Form>
                    <Field type="email" name="email" placeholder="Email" component={TextField} variant="outlined"
                           margin="normal" fullWidth/>
                    <ErrorMessage name="email" component="div"/>
                    <br/>
                    <Field type="password" name="password" placeholder="Password" component={TextField}
                           variant="outlined" margin="normal" fullWidth/>
                    <ErrorMessage name="password" component="div"/>
                    <br/>
                    <React.Fragment>
                        <Button type="submit" disabled={props.isSubmitting} variant="contained" margin="normal"
                                color="primary" fullWidth>
                            Submit
                        </Button>
                        <div style={{color: 'red'}}>{props.errors.general}</div>
                    </React.Fragment>
                </Form>
                <Link to="/register" style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    Sign up
                </Link>
            </div>
        )}
    >

    </Formik>)
}

export function Login({client}) {
    const [loggedIn, setLoggedIn] = useState(0)
    const onSubmit = (values, {setSubmitting, setErrors}) => {
        setTimeout(() => {
            client.loginUser((values: Credentials))
                .then(token => {
                    setSession(token)
                    setLoggedIn(true)
                })
                .catch(err => setErrors({general: err.message}))
                .finally(() => setSubmitting(false))
        }, 400);
    }
    return (loggedIn ? <Redirect to="/"/> : (
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
            <LoginForm onSubmit={onSubmit}/>
        </div>))
}