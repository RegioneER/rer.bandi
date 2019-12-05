import React, { useState, useContext } from 'react';
import { array, bool, object, func } from 'prop-types';
import FormFieldWrapper from '../FormFieldWrapper';
import { TranslationsContext } from '../../TranslationsContext';

import './index.less';

const checkIsMobile = () => window.innerWidth <= 991;

const FiltersWrapper = ({
  formParameters,
  queryParameters,
  isFetching,
  updateQueryParameters,
  resetQueryParameters,
}) => {
  const getTranslationFor = useContext(TranslationsContext);
  const [isMobile, setIsMobile] = useState(checkIsMobile());

  window.addEventListener('resize', () => {
    let checkedIfMobile = checkIsMobile();
    if (checkedIfMobile !== isMobile) setIsMobile(checkedIfMobile);
  });

  const filtersContent = isFetching ? (
    <div>Loading...</div>
  ) : (
    <React.Fragment>
      <h2 id="bandi-search-filters" className="refineSearch sr-only">
        {getTranslationFor('refine_search_label', 'Refine your search')}
      </h2>
      <a href="#bandi-search-results" className="sr-only">
        {getTranslationFor('go_to_search_results', 'Go to results')}
      </a>
      {isMobile && (
        <button
          className="btn btn-secondary collapse-btn collapsed"
          type="button"
          data-toggle="collapse"
          data-target="#filtersCollapse"
          aria-expanded="false"
          aria-controls="filtersCollapse"
        >
          {getTranslationFor('toggle_filters_label', 'Toggle filters')}{' '}
          <span
            className="glyphicon glyphicon-filter"
            aria-hidden="true"
          ></span>
        </button>
      )}
      <div
        className={`collapse ${isMobile ? '' : 'in'}`}
        id="filtersCollapse"
        aria-expanded={!isMobile}
      >
        {formParameters && formParameters.length
          ? formParameters.map(parameter => (
              <FormFieldWrapper
                parameter={parameter}
                key={parameter.id}
                value={queryParameters[parameter.id]}
                updateQueryParameters={updateQueryParameters}
              />
            ))
          : ''}
        <div className="reset-filters">
          <button onClick={resetQueryParameters} className="btn btn-secondary">
            {getTranslationFor('reset_filters_label', 'Reset all filters')}
          </button>
        </div>
      </div>
    </React.Fragment>
  );

  return (
    <div className="search-filter col-md-4 col-sm-12">{filtersContent}</div>
  );
};
FiltersWrapper.propTypes = {
  formParameters: array,
  queryParameters: object,
  isFetching: bool,
  updateQueryParameters: func,
  resetQueryParameters: func,
};

export default FiltersWrapper;
