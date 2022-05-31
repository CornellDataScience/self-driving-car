import React, { useState, useEffect} from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';

function createGraphData(ccno, altitude, lin_acc_z){
  return { ccno, altitude, lin_acc_z};
}

export default function Chart(props) {
  const theme = useTheme();

  const delta_alt = 1;
  let n = 30;
  // console.log(props.data);
  const [data_points, set_data] = useState(Array(n).fill(createGraphData(0,0,0)));

  const update_data = () => {
    let data_copy = data_points;
    data_copy.shift();
    // let alts_copy = alts.co();
    data_copy.push(createGraphData(props.ccno, props.altitude, props.lin_acc_z))
    set_data(data_copy);
    // console.log(data_points);
    // set_key(key + 1);
  }

  useEffect(() => update_data());

  return (
    <React.Fragment>
      <Title>CCNO vs Altitude and Linear Acceleration<sub>z</sub></Title>
      <ResponsiveContainer>
        <LineChart
          data={data_points}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="ccno" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary}
                yAxisId="left"
                type="number" 
                domain={[dataMin => (Math.floor(dataMin)-delta_alt), max => (Math.floor(max)+delta_alt)]}>
            <Label
              angle={270}
              position="left"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Altitude (ASL) (m)
            </Label>
          </YAxis>
          <YAxis yAxisId="right" orientation="right" type="number"
                 domain={[-12,12]} allowDataOverflow={true}>
            <Label
              angle={90}
              position="right"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Linear Acc. Z (m/s^2)
            </Label>
                 </YAxis>
          <Line yAxisId="left" type="monotone" dataKey="altitude" stroke={theme.palette.primary.main} dot={false} />
          <Line yAxisId="right" type="monotone" dataKey="lin_acc_z" stroke={theme.palette.secondary.main} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
