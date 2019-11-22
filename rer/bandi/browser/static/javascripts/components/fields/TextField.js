import React, { useState, useEffect } from 'react';
import { string, shape, func } from 'prop-types';

const TextField = ({ parameter, value = '', updateQueryParameters }) => {
  const [data, setData] = useState({ text: '', timeout: 0 });
  const delaySearchSubmit = targetValue => {
    if (data.timeout) {
      clearInterval(data.timeout);
    }
    const timeout = setTimeout(() => {
      updateQueryParameters({
        [parameter.id]: targetValue,
      });
    }, 1000);
    setData({ text: targetValue, timeout });
  };

  useEffect(() => {
    setData({ text: value, timeout: 0 });
  }, [value]);
  return (
    <label>
      <span>{parameter.label}</span>
      {parameter.help ? <p className="discreet">{parameter.help}</p> : ''}
      <input
        name={parameter.id}
        type="text"
        value={data.text}
        onChange={e => delaySearchSubmit(e.target.value)}
      />
    </label>
  );
};

TextField.propTypes = {
  parameter: shape({
    id: string,
  }),
  value: string,
  updateQueryParameters: func,
};

export default TextField;
