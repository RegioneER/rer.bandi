import React from 'react';
import FiltersWrapper from './components/FiltersWrapper';

import './App.less';

const App = () => (
  <React.Fragment>
    <div className="search-results">RISULTATI</div>
    <FiltersWrapper></FiltersWrapper>
  </React.Fragment>
);

export default App;
