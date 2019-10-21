import React, {useState} from "react";
import {ErrorMessage, Field, Form, Formik} from "formik";
import {Link, Redirect} from "react-router-dom";
import Button from "@material-ui/core/Button";
import {TextField} from "formik-material-ui";

export function Register(apiUrl) {
    const [registered, setRegistered] = useState(0)
    return (registered ? <Redirect to="/login"/> : <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <Formik
            initialValues={{email: '', firstName: '', lastName: '', password: '', confirmPassword: ''}}
            validate={values => {
                let errors = {};
                if (!values.email) {
                    errors.email = 'Required';
                } else if (
                    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                ) {
                    errors.email = 'Invalid email address';
                }

                if (!values.firstName) {
                    errors.firstName = 'Required'
                }

                if (!values.lastName) {
                    errors.lastName = "Required"
                }

                if (!values.password) {
                    errors.password = "Required"
                }

                if (!values.confirmPassword) {
                    errors.confirmPassword = "Required"
                } else if (values.password !== values.confirmPassword) {
                    errors.confirmPassword = "Must be the same as password"
                }
                return errors;
            }}
            onSubmit={(values, {setSubmitting, setErrors}) => {
                setTimeout(() => {
                    console.log(JSON.stringify(values, null, 2));
                    console.log(apiUrl.apiUrl)
                    fetch(`${apiUrl.apiUrl}/user`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            email: values.email,
                            firstName: values.firstName,
                            lastName: values.lastName,
                            password: values.password
                        })
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
                            setRegistered(true)
                        })
                        .catch(resp => {
                            console.error(resp.statusText)
                            if (resp.status === 403) {
                                resp.json().then(json => {
                                    setErrors({general: json.message})
                                })
                            } else {
                                setErrors({general: "There was a problem registering. Please try again later"})
                            }
                        })
                    setSubmitting(false);
                }, 400);
            }}
        >
            {({isSubmitting, errors}) => (
                <div>
                    <Form>
                        <Field type="email" name="email" placeholder="Email" variant="outlined" component={TextField}
                               margin="normal"/>
                        <ErrorMessage name="email" component="div"/>
                        <br/>
                        <Field type="text" name="firstName" placeholder="First Name" variant="outlined"
                               component={TextField} margin="normal"/>
                        <ErrorMessage name="firstName" component="div"/>
                        <br/>
                        <Field type="text" name="lastName" placeholder="Last Name" variant="outlined"
                               component={TextField} margin="normal"/>
                        <ErrorMessage name="lastName" component="div"/>
                        <br/>
                        <Field type="password" name="password" placeholder="Password" variant="outlined"
                               component={TextField} margin="normal"/>
                        <ErrorMessage name="password" component="div"/>
                        <br/>
                        <Field type="password" name="confirmPassword" placeholder="Confirm Password" variant="outlined"
                               component={TextField} margin="normal" />
                        <ErrorMessage name="confirmPassword" component="div"/>
                        <br/>

                        <React.Fragment>
                            <Button type="submit" disabled={isSubmitting} variant="contained" margin="normal" fullWidth
                                    color="primary">
                                Submit
                            </Button>
                            <div style={{color: 'red'}}>{errors.general}</div>
                        </React.Fragment>
                    </Form>
                    <Link to="/login" style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>Sign
                        in</Link>
                </div>
            )}
        </Formik>
    </div>)
}
