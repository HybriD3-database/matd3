Array.from(document.getElementsByClassName('expand-hide-button')).forEach(function(element) {
  element.addEventListener('click', function() {
    var target = document.getElementById(element.dataset.target.split('#')[1]);
    if (target.id.startsWith('atomic-coordinates-body-') && target.innerHTML === '') {
      var series_id = target.id.split('atomic-coordinates-body-')[1];
      $.getJSON('/materials/get-atomic-coordinates/' + series_id, function(data) {
        var table = document.createElement('table');
        table.className = 'table-atomic-coordinates';
        var fragment = document.createDocumentFragment();
        for (var i=0; i<data['vectors'].length; i++) {
          var tr = document.createElement('tr');
          var td = document.createElement('td');
          td.innerHTML = 'lattice_vector';
          td.style = 'text-align:left';
          tr.appendChild(td);
          for (var j=0; j<3; j++) {
            var td = document.createElement('td');
            td.innerHTML = data['vectors'][i][j];
            tr.appendChild(td);
          }
          fragment.appendChild(tr);
        }
        table.appendChild(fragment);
        target.append(table);
        if (data['coord-type'] == 'atom_frac') {
          var coord_type = 'atom_frac';
        } else {
          var coord_type = 'atom';
        }
        table = document.createElement('table');
        table.className = 'table-atomic-coordinates';
        for (var i=0; i<data['coordinates'].length; i++) {
          var tr = document.createElement('tr');
          var td = document.createElement('td');
          td.innerHTML = coord_type;
          tr.appendChild(td);
          for (var j=1; j<4; j++) {
            var td = document.createElement('td');
            td.innerHTML = data['coordinates'][i][j];
            tr.appendChild(td);
          }
          var td = document.createElement('td');
          td.style = 'text-align:left';
          td.innerHTML = data['coordinates'][i][0];
          tr.appendChild(td);
          fragment.appendChild(tr);
        }
        table.appendChild(fragment);
        target.append(table);
      });
    }
  });
});
