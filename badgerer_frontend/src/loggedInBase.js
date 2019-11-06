import { makeStyles } from "@material-ui/core";
import SwipeableDrawer from "@material-ui/core/SwipeableDrawer";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import SettingsIcon from "@material-ui/core/SvgIcon/SvgIcon";
import React, { useContext, useState } from "react";
import AppBar from "@material-ui/core/AppBar/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import { SessionContext } from "./session";
import LockIcon from "@material-ui/icons/Lock";
import MenuIcon from "@material-ui/icons/Menu";
import { Redirect } from "react-router-dom";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  },
  list: {
    width: 250
  }
}));

const LoggedInDrawer = ({
  classes,
  open,
  onOpen,
  onClose,
  handleHome,
  handleAttendance,
  handleBadgetracking,
  handleGroups,
  handlePlans,
  handleSettings,
  handleLogout
}) => (
  <SwipeableDrawer open={open} onClose={onClose} onOpen={onOpen}>
    <div
      className={classes.list}
      role="presentation"
      onClick={onClose}
      onKeyDown={onClose}
    >
      <List>
        <ListItem button key="home" onClick={handleHome}>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button key="attendance" onClick={handleAttendance}>
          <ListItemText primary="Attendance" />
        </ListItem>
        <ListItem button key="badgetracking" onClick={handleBadgetracking}>
          <ListItemText primary="Badge Tracking" />
        </ListItem>
        <ListItem button key="groups" onClick={handleGroups}>
          <ListItemText primary="Groups" />
        </ListItem>
        <ListItem button key="Plans" onClick={handlePlans}>
          <ListItemText primary="Plans" />
        </ListItem>
      </List>
      <Divider />
      <ListItem button key="settings" onClick={handleSettings}>
        <ListItemIcon>
          <SettingsIcon />
        </ListItemIcon>
        <ListItemText primary="Settings" />
      </ListItem>
      <ListItem button key="logout" onClick={handleLogout}>
        <ListItemIcon>
          <LockIcon />
        </ListItemIcon>
        <ListItemText primary="Logout" />
      </ListItem>
    </div>
  </SwipeableDrawer>
);

const LoggedInAppBar = ({ classes, title, logout, setRedirect }) => {
  const [navDrawerOpen, setNavDrawerOpen] = useState(false);

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="menu"
            onClick={() => setNavDrawerOpen(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            {title}
          </Typography>
        </Toolbar>
      </AppBar>
      <LoggedInDrawer
        classes={classes}
        open={navDrawerOpen}
        onOpen={() => setNavDrawerOpen(true)}
        onClose={() => setNavDrawerOpen(false)}
        handleHome={() => {
          setNavDrawerOpen(false);
          setRedirect("home");
        }}
        handleAttendance={() => {
          console.log("Redirecting to attendance");
          setNavDrawerOpen(false);
          setRedirect("attendance");
        }}
        handleBadgetracking={() => {
          console.log("Redirecting to badge tracking");
          setNavDrawerOpen(false);
          setRedirect("badgetracking");
        }}
        handleGroups={() => {
          setNavDrawerOpen(false);
          setRedirect("groups");
        }}
        handlePlans={() => {
          setNavDrawerOpen(false);
          setRedirect("plans");
        }}
        handleSettings={() => {
          setNavDrawerOpen(false);
          setRedirect("settings");
        }}
        handleLogout={() => {
          setNavDrawerOpen(false);
          logout();
        }}
      />
    </div>
  );
};

export const LoggedInBasePage = ({ title, ...props }) => {
  const classes = useStyles();
  const { clearSession } = useContext(SessionContext);
  const [state, setState] = useState({ redirectLocation: "" });

  if (state.redirectLocation) {
    console.log(`Redirection to ${state.redirectLocation}`);
    return <Redirect to={`/${state.redirectLocation}`} />;
  }
  return (
    <div className={classes.root}>
      <LoggedInAppBar
        title={title}
        classes={classes}
        logout={() => {
          clearSession();
        }}
        setRedirect={location => {
          console.log(`Setting redirect to ${location}`);
          setState({ ...state, redirectLocation: location });
        }}
      />
      {props.children}
    </div>
  );
};
