import React, { useContext } from 'react';
import { object } from 'prop-types';
import format from 'date-fns/format';
import isPast from 'date-fns/isPast';
import isAfter from 'date-fns/isAfter';
import isBefore from 'date-fns/isBefore';

import { TranslationsContext } from '../../TranslationsContext';

import './index.less';

const BandoItem = ({ data }) => {
  const getTranslationFor = useContext(TranslationsContext);
  const calculateState = ({
    scadenza_bando,
    chiusura_procedimento_bando,
  }) => {
    let state = 'open';
    const scadenzaDate = scadenza_bando.length
      ? new Date(scadenza_bando)
      : null;
    const chiusuraDate = chiusura_procedimento_bando.length
      ? new Date(chiusura_procedimento_bando)
      : null;
    if (scadenzaDate && isPast(scadenzaDate)) {
      if (isPast(chiusuraDate)) {
        state = 'closed';
      } else {
        state = 'inProgress';
      }
    } else {
      if (isPast(chiusuraDate)) {
        state = 'closed';
      }
    }
    return state;
  };

  const { effective, scadenza_bando } = data;
  const bandoState = calculateState(data);

  let effectiveDateItem = '';
  let scadenzaBandoItem = '';
  if (effective) {
    const effectiveDate = new Date(effective);
    if (isAfter(effectiveDate, new Date(1969, 11, 31))) {
      effectiveDateItem = (
        <p>
          <span className="labelTB">
            {getTranslationFor('bandi_published_on', '')}
          </span>
          :&nbsp;<span>{format(new Date(effective), 'dd/MM/yyyy')}</span>
        </p>
      );
    }
  }
  if (scadenza_bando) {
    const scadenzaDate = new Date(scadenza_bando);
    if (isBefore(scadenzaDate, new Date(2100, 11, 31))) {
      scadenzaBandoItem = (
        <p>
          <span className="labelTB">
            {getTranslationFor('bando_scadenza_partecipazione', '')}
          </span>
          :&nbsp;
          <span>{format(new Date(scadenza_bando), 'dd/MM/yyyy HH:mm')}</span>
        </p>
      );
    }
  }
  return (
    <div className="bando-result">
      <h3 className="bandoTitle contenttype-bando">
        <span className={`state-${bandoState} bandoStateClass`}>
          {getTranslationFor(
            `bandi_search_state_${bandoState.toLowerCase()}`,
            bandoState,
          )}
        </span>
        <a className={`state-${data.review_state}`} href={data['@id']}>
          <span>{data.title}</span>
        </a>
      </h3>
      <div className="bandoDetail">
        {data.description}
        <div className="bandoDates">
          {effectiveDateItem}
          {effectiveDateItem && scadenzaBandoItem ? (
            <span className="separator">|</span>
          ) : (
            ''
          )}
          {scadenzaBandoItem}
        </div>
      </div>
    </div>
  );
};

BandoItem.propTypes = {
  data: object,
};

export default BandoItem;
