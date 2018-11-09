var searchProduct = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('q'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '/stock/search_tph/?q=%QUERY',
    remote: {
      url: '/stock/search_tph/?q=%QUERY',
      wildcard: '%QUERY'
    }
  });
  
  $('#search_product .typeahead').typeahead({
    //hint:true,
    //highlight: true,
    //autoselect: true,
    minLength:1,
    limit: 10,
  }, {
    name: 'searchProduct',
    displayKey: 'q',
    source: searchProduct,
    templates:{
      empty: 'Не має в базі',
    }
  });