import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'rc-progress';
import { string } from 'prop-types';
import Spinner from 'react-svg-spinner';

const ProgressBarContainer = ({ authenticator, action }) => {
  const defaultData = {
    in_progress: true,
    tot: 0,
    counter: 0,
    message: '',
  };
  const [intervalId, setIntervalId] = useState();
  const [reindexStart, setReindexStart] = useState(false);
  const [data, setData] = useState(defaultData);

  const portalUrl = document.body
    ? document.body.getAttribute('data-portal-url') || ''
    : '';

  const doCancel = () => {
    window.location.href = `${portalUrl}/@@solrpush-conf`;
  };

  const doReindex = () => {
    setData(defaultData);
    setReindexStart(true);
    axios(`${portalUrl}/${action}`, {
      params: { _authenticator: authenticator },
    });
    const intervalId = setInterval(function() {
      axios(`${portalUrl}/reindex-progress`).then(result =>
        setData(result.data),
      );
    }, 5000);
    setIntervalId(intervalId);
  };

  const { tot, counter, in_progress, message } = data;
  if (reindexStart && !in_progress) {
    setReindexStart(false);
    clearInterval(intervalId);
  }
  const progress = tot === 0 ? 0 : Math.floor((counter * 100) / tot);
  console.log(data);
  return (
    <div className="maintenance-wrapper">
      <div className="formControls">
        <button onClick={doReindex} disabled={reindexStart}>
          Start {reindexStart ? <Spinner /> : ''}
        </button>{' '}
        <button onClick={doCancel} disabled={reindexStart}>
          Cancel
        </button>
      </div>
      <div className="status-bar">
        <Line
          percent={progress}
          strokeWidth="2"
          strokeLinecap="butt"
          strokeColor={progress === 100 ? '#008000' : '#007bb1'}
        />
        {message && <div className="status-message">{message}</div>}
        {tot > 0 ? (
          <div>
            {counter}/{tot} ({progress}%)
          </div>
        ) : (
          ''
        )}
      </div>
    </div>
  );
};

ProgressBarContainer.propTypes = {
  authenticator: string,
  action: string,
};

export default ProgressBarContainer;
