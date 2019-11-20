import React, { useContext } from 'react';
import { array, bool, object, func } from 'prop-types';
import FormFieldWrapper from '../FormFieldWrapper';
import { TranslationsContext } from '../../TranslationsContext';

import './index.less';

const FiltersWrapper = ({
  formParameters,
  queryParameters,
  isFetching,
  updateQueryParameters,
}) => {
  const getTranslationFor = useContext(TranslationsContext);

  const filtersContent = isFetching ? (
    <div>Loading...</div>
  ) : (
    <React.Fragment>
      <h2 className="refineSearch">
        {getTranslationFor('refine_search_label', 'Refine your search')}
      </h2>
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
    </React.Fragment>
  );

  return (
    <div className="search-filter col-lg-5 col-md-6 col-sm-12">
      {filtersContent}
    </div>
  );
};
FiltersWrapper.propTypes = {
  formParameters: array,
  queryParameters: object,
  isFetching: bool,
  updateQueryParameters: func,
};

export default FiltersWrapper;
