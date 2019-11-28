import React from 'react';
import ReactPaginate from 'react-paginate';

const PaginationContainer = ({
  updateQueryParameters,
  translations,
  totalResults,
  pageSize,
  currentPage,
}) => {
  const handlePageChange = data => {
    if (currentPage !== data.selected) {
      updateQueryParameters({ b_start: data.selected * pageSize });
    }
  };

  if (totalResults && totalResults > pageSize) {
    return (
      <div className="navigation">
        {' '}
        <ReactPaginate
          initialPage={currentPage}
          previousLabel={translations ? translations.previous_label : '<'}
          nextLabel={translations ? translations.next_label : '>'}
          breakLabel={'...'}
          breakClassName={'break-me'}
          pageCount={Math.ceil(totalResults / pageSize)}
          onPageChange={handlePageChange}
          containerClassName={'pagination'}
          subContainerClassName={'pages pagination'}
          activeClassName={'active'}
        />
      </div>
    );
  } else {
    return '';
  }
};

export default PaginationContainer;
