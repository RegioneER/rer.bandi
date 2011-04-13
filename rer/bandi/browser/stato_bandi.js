/*jslint browser: true */
/*global alert, window */


jQuery(function($) {

"use strict";


function iso_date_string(date) {
    var y = date.getFullYear(),
        m = date.getMonth()+1,
        d = date.getDate();

    return y + '-' + (m<10?'0'+m:m) + '-' + (d<10?'0'+d:d);
}



$('#stato_bandi')
    .change(function(ev) {
                var today = iso_date_string(new Date()),
                    $form = $(this).closest('form');

                $('input[name^=getScadenza_bando],input[name^=getChiusura_procedimento]', $form).remove();

                switch ($('option:selected', this).attr('value')) {
                    case 'aperti':
                        $form.append(
                            $('<input type="text" name="getScadenza_bando">').attr('value', today),
                            $('<input type="text" name="getScadenza_bando_usage" value="range:min">')
                            );
                        break;
                    case 'in_corso':
                        $form.append(
                            $('<input type="text" name="getScadenza_bando">').attr('value', today),
                            $('<input type="text" name="getScadenza_bando_usage" value="range:max">'),
                            $('<input type="text" name="getChiusura_procedimento_bando">').attr('value', today),
                            $('<input type="text" name="getChiusura_procedimento_bando_usage" value="range:min">')
                            );
                        break;
                    case 'conclusi':
                        $form.append(
                            $('<input type="text" name="getChiusura_procedimento_bando">').attr('value', today),
                            $('<input type="text" name="getChiusura_procedimento_bando_usage" value="range:max">')
                            );
                        break;
                    default:
                        // tutti
                        break;
                }
        })
    .change();

});



