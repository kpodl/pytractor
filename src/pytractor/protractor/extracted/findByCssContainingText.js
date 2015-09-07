try { return (function (cssSelector, searchText, using) {
  using = using || document;

  var elements = using.querySelectorAll(cssSelector);
  var matches = [];
  for (var i = 0; i < elements.length; ++i) {
    var element = elements[i];
    var elementText = element.textContent || element.innerText || '';
    if (elementText.indexOf(searchText) > -1) {
      matches.push(element);
    }
  }
  return matches;
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }