import React, { useContext, useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import AccountCircle from "@material-ui/icons/AccountCircle";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";
import { Redirect } from "react-router-dom";
import { SessionContext } from "./session";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  }
}));

const HomeAppBar = ({
  classes,
  handleMenu,
  logout,
  handleMenuClose,
  anchorEl,
  open
}) => (
  <AppBar position="static">
    <Toolbar>
      <IconButton
        edge="start"
        className={classes.menuButton}
        color="inherit"
        aria-label="menu"
      >
        <MenuIcon />
      </IconButton>
      <Typography variant="h6" className={classes.title}>
        Photos
      </Typography>
      <div>
        <IconButton
          aria-label="account of current user"
          aria-controls="menu-appbar"
          aria-haspopup="true"
          onClick={handleMenu}
          color="inherit"
        >
          <AccountCircle />
        </IconButton>
        <Menu
          id="menu-appbar"
          anchorEl={anchorEl}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right"
          }}
          keepMounted
          transformOrigin={{
            vertical: "top",
            horizontal: "right"
          }}
          open={open}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
          <MenuItem onClick={handleMenuClose}>My account</MenuItem>
          <MenuItem onClick={logout}>Logout</MenuItem>
        </Menu>
      </div>
    </Toolbar>
  </AppBar>
);

export const HomePage = () => {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const { clearSession } = useContext(SessionContext);

  const handleMenu = event => {
    console.log(`Handling menu with event ${event}`);
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    console.log("Closing menu");
    setAnchorEl(null);
  };
  return (
    <div className={classes.root}>
      <HomeAppBar
        classes={classes}
        anchorEl={anchorEl}
        handleMenu={handleMenu}
        handleMenuClose={handleClose}
        logout={() => {
          clearSession();
          handleClose();
        }}
        open={open}
      />
    </div>
  );
};

export function Home() {
  const { loggedIn } = useContext(SessionContext);
  useEffect(() => {
    console.log(`Rendering home page, logged in? ${loggedIn}`);
  });

  return loggedIn ? <HomePage /> : <Redirect to="/login" />;
}
