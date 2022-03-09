import React, { useState, useEffect, useRef} from 'react';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles({
  depositContext: {
    flex: 1,
  },
});

function mm_num_to_string(mode){
  let names = [
    "Warm-Up",
    "Initialization",
    "Standby",
    "Detumble",
    "Belly-flop",
    "Landed"
  ]
  return names[mode]
}
export default function StateDisplay(props) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <Title>State</Title>
      <Typography component="p" variant="h4">
        CCNO: {props.ccno}
      </Typography>
      <Typography component="p" variant="h4">
        Mode: {mm_num_to_string(props.mm_mode)}
      </Typography>
      <Typography component="p" variant="h4">
        AGL (m): {(props.agl).toFixed(3)}
      </Typography>
      <Typography component="p" variant="h4">
        Alt (m): {(props.altitude).toFixed(3)}
      </Typography>
      {/* <Typography color="textSecondary" className={classes.depositContext}>
        on 15 March, 2019
      </Typography> */}
    </React.Fragment>
  );
}
