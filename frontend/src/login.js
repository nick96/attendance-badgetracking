import {ErrorMessage, Field, Form, Formik} from "formik";
import React, {useState} from "react";
import {Link, Redirect} from "react-router-dom";
import {TextField} from 'formik-material-ui'

import {getSession, setSession} from "./utils";
import Button from "@material-ui/core/Button";
import {useSnackbar} from "notistack";

export function Login(apiUrl) {
    const { enqueueSnackbar } = useSnackbar()
    const [loggedIn, setLoggedIn] = useState(0)
    return (loggedIn ? <Redirect to="/"/> : <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <Formik
            initialValues={{email: '', password: ''}}
            validate={values => {
                let errors = {};
                if (!values.email) {
                    errors.email = 'Required';
                } else if (
                    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                ) {
                    errors.email = 'Invalid email address';
                }
                return errors;
            }}
            onSubmit={(values, {setSubmitting, setErrors}) => {
                setTimeout(() => {
                    console.log(JSON.stringify(values, null, 2));
                    console.log(apiUrl)
                    fetch(`${apiUrl.apiUrl}/login`, {
                        method: 'POST',
                        mode: "cors",
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(values)
                    })
                        .then(resp => {
                            if (resp.ok) {
                                return resp.json()
                            } else {
                                throw resp
                            }
                        })
                        .then(json => {
                            console.log(json)
                            setSession(json.token)
                            setLoggedIn(true)
                            enqueueSnackbar("Logged in successfully",  {
                                    variant: 'success',
                                    anchorOrigin: {
                                        vertical: 'top',
                                        horizontal: 'center',
                                    }
                                })
                        })
                        .catch(resp => {
                            console.error(resp.statusText)
                            if (resp.status === 403) {
                                setErrors({general: "Email or password was incorrect`"})
                            } else {
                                setErrors({general: "There was a problem logging in. Please try again later"})
                            }
                        })
                    setSubmitting(false);
                }, 400);
            }}
        >
            {({isSubmitting, errors}) => (
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
                            <Button type="submit" disabled={isSubmitting} variant="contained" margin="normal"
                                    color="primary" fullWidth>
                                Submit
                            </Button>
                            <div style={{color: 'red'}}>{errors.general}</div>
                        </React.Fragment>
                    </Form>
                    <Link to="/register" style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>Sign up</Link>
                </div>
            )}
        </Formik>
    </div>)
}