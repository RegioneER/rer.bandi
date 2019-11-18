import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FiltersWrapper from './components/FiltersWrapper';
import ResultsWrapper from './components/ResultsWrapper';
import TranslationsWrapper from './TranslationsContext';
import queryString from 'query-string';

import './App.less';

const App = () => {
  const [isFetching, setFetching] = useState(false);
  const [formParameters, setFormParameters] = useState([]);
  const [queryParameters, setQueryParameters] = useState({
    b_start: 0,
    b_size: 20,
  });

  const portalUrl = document.body
    ? document.body.getAttribute('data-portal-url') || ''
    : '';
  useEffect(() => {
    setFetching(true);
    axios({
      method: 'GET',
      headers: {
        'content-type': 'application/json',
        Accept: 'application/json',
      },
      url: `${portalUrl}/@search_parameters`,
    }).then(({ status, statusText, data }) => {
      if (status !== 200) {
        console.error(statusText);
      } else {
        setFormParameters(data);
        setFetching(false);
        initializeQueryParameters(data);
      }
    });
  }, []);

  const initializeQueryParameters = parameters => {
    const queryString = new URLSearchParams(window.location.search);
    const newParameters = parameters.reduce((accumulator, parameter) => {
      switch (parameter.type) {
        case 'text':
          accumulator[parameter.id] = queryString.get(parameter.id) || '';
          break;
        default:
          if (!queryString.get(parameter.id)) {
            //  empty
            accumulator[parameter.id] = [];
          } else {
            accumulator[parameter.id] = queryString.getAll(parameter.id);
          }
          break;
      }

      return accumulator;
    }, {});
    setQueryParameters({ ...queryParameters, ...newParameters });
  };

  const updateQueryParameters = parameter => {
    const newQueryParameters = { ...queryParameters, ...parameter };
    setQueryParameters(newQueryParameters);
    history.pushState(
      { id: 'search_bandi_new' },
      'Search Bandi',
      `${portalUrl}/search_bandi_new?${queryString.stringify(
        newQueryParameters,
      )}`,
    );
  };
  return (
    <TranslationsWrapper>
      <FiltersWrapper
        updateQueryParameters={updateQueryParameters}
        formParameters={formParameters}
        queryParameters={queryParameters}
        isFetching={isFetching}
      ></FiltersWrapper>
      <ResultsWrapper
        queryParameters={queryParameters}
        updateQueryParameters={updateQueryParameters}
      ></ResultsWrapper>
    </TranslationsWrapper>
  );
};
export default App;
